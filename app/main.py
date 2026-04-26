from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File, Form

from app.db.database import engine
from sqlmodel import SQLModel
from app.db.commands import fetch_chunks, store_chunks
from app.ingestion.ingest_chunks import embed_chunks, create_chunks_from_pdf
from app.pinecone_client.client import upsert_to_pinecone, index
from app.embedding.embedder import embed_text
from app.db.models import QueryRequest
from app.agent.llm import generate_response

# Initialize DB automatically on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing Database...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database Ready.")
    yield
    # Shutdown logic...

app = FastAPI(title="RAG Backend Services", lifespan=lifespan)


@app.post("/ingest-document")
async def ingest_document_endpoint(
    file: UploadFile = File(...),
    document_id: str = Form(...),
    strategy: str = Form("paragraph"),
    chunk_size: int = Form(100),
    overlap: int = Form(20)
):
    """
    Combined flow for ingesting a PDF:
    Chunks -> Inserts into SQL -> Extracted IDs -> Embeds -> Upserts to Pinecone
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        file_bytes = await file.read()

        chunks = create_chunks_from_pdf(
            file_bytes, 
            strategy=strategy, 
            chunk_size=chunk_size, 
            overlap=overlap
        )
        
        await store_chunks(chunks, document_id)
        
        stored_chunks = await fetch_chunks(document_id=document_id)
        
        chunk_dicts = [
            {
                "chunk_id": chunk.id,
                "text": chunk.text,
                "document_id": chunk.document_id,
                "chunk_number": chunk.chunk_number
            }
            for chunk in stored_chunks
        ]

        print(f"Embedding {len(chunk_dicts)} chunks...")
        embedded_chunks = embed_chunks(chunk_dicts)
        
        print("Upserting to vector database...")
        await upsert_to_pinecone(embedded_chunks)
        
        return {
            "status": "success", 
            "message": f"Successfully ingested {len(stored_chunks)} chunks for document {document_id}."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/query-document")
async def query_endpoint(req: QueryRequest):
    try:
        # Step 1: Embed query
        embedded_query = embed_text(req.query)

        # Step 2: Query Pinecone
        response = index.query(
            vector=embedded_query,
            top_k=req.top_k,
            include_metadata=True,
            filter={"document_id": req.document_id} if req.document_id else "Resume_Prashant"
        )

        matches = response.get("matches", [])
        if not matches:
            return {
                "status": "success",
                "response_text": "No relevant information found."
            }

        # Step 3: Extract text directly from metadata (🔥 KEY CHANGE)
        MAX_CHARS = 4000
        context_parts = []
        current_len = 0

        for match in matches:
            metadata = match.get("metadata", {})
            text = metadata.get("text")

            if not text:
                continue  # skip bad entries

            if current_len + len(text) > MAX_CHARS:
                break

            context_parts.append(text)
            current_len += len(text)

        # Safety check
        if not context_parts:
            return {
                "status": "success",
                "response_text": "Relevant data found but no usable text context."
            }

        llm_input_text = "\n".join(context_parts)

        # Step 4: Generate response
        response_text = generate_response(llm_input_text, req.query)

        return {
            "status": "success",
            "llm_input_text": llm_input_text,
            "response_text": response_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)