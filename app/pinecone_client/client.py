from pinecone import Pinecone
from app.core.config import settings

pc = Pinecone(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENV)
index = pc.Index(settings.PINECONE_INDEX)

async def upsert_to_pinecone(embedded_chunks):
    vectors = []

    for chunk in embedded_chunks:
        embedding = chunk["embedding"]
        if not isinstance(embedding, list):
            embedding = embedding.tolist()

        vectors.append({
            "id": str(chunk["chunk_id"]), 
            "values": embedding,
            "metadata": {
                "text": chunk["text"],  
                "document_id": chunk.get("document_id"),
                "chunk_number": chunk.get("chunk_number")
            }
        })

    import asyncio
    await asyncio.to_thread(index.upsert, vectors=vectors)


if __name__ == "__main__":
    from embedding.embedder import embed_text
    from pinecone_client.client import query_pinecone

    query= "Ankit Neupane is a software engineer at Microsoft."
    embedded_query = embed_text(query)

    response = index.query(
    vector=embedded_query,      # single query vector
    top_k=5,
    include_metadata=True
)