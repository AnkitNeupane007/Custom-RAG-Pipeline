from sentence_transformers import SentenceTransformer
# from app.core.config import settings
# import openai 

model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

def embed_text(text: str) -> list[float]:
    embedding = model.encode(text)
    return embedding.tolist()

# client= openai.Client(api_key=settings.OPENAI_KEY)
