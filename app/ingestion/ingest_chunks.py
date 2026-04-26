from .chunk_pdf import extract_text_from_pdf
from app.embedding.embedder import embed_text

def create_chunks_from_pdf(
    file_bytes: bytes, 
    strategy: str, 
    chunk_size: int = 500, 
    overlap: int = 50
) -> list[dict]:
    """
    Returns as 
    {
        "chunk_id": int,
        "text": str,
        "page_number": int,
        "chunk_number": int
    }
    """
    pages = extract_text_from_pdf(file_bytes)
    chunks = []
    chunk_id = 0
    chunk_number = 1

    if strategy == "word":
        for page_number, page in enumerate(pages):
            start = 0
            while start < len(page):
                end = start + chunk_size
                chunk_text = page[start:end]
                chunks.append({
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                    "page_number": page_number,
                    "chunk_number": chunk_number
                })
                chunk_number += 1
                chunk_id += 1
                start += chunk_size - overlap  # move by chunk_size minus overlap

    elif strategy == "paragraph":
        for page_number, page in enumerate(pages):
            paragraphs = [p.strip() for p in page.split('\n') if p.strip()]
            for para in paragraphs:
                start = 0
                while start < len(para):
                    end = start + chunk_size
                    chunk_text = para[start:end]
                    chunks.append({
                        "chunk_id": chunk_id,
                        "text": chunk_text,
                        "page_number": page_number,
                        "chunk_number": chunk_number
                    })
                    chunk_number += 1
                    chunk_id += 1
                    start += chunk_size - overlap  # overlap step


    return chunks

def embed_chunks(chunks: list[dict]) -> list[dict]:

    '''' 
        Returns in type
        {
            "chunk_id": int,
            "text": str,
            "page_number": int,
            "chunk_number": int,
            "embedding": list[float]
        }
    '''
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_text(texts)
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding
    return chunks

# Example usage:
if __name__ == "__main__":
    chunks = create_chunks_from_pdf("E:/RAG/chunking/ingestion/sample.pdf", strategy="word", chunk_size=100, overlap=20)
    embedded_chunks = embed_chunks(chunks)
    for chunk in embedded_chunks:
        print(chunk)