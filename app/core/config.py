from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    GENAI_API_KEY: str = ""
    OPENAI_KEY: str = ""
    # Database
    DATABASE_URL: str = ""
    # Pinecone
    PINECONE_API_KEY: str = ""
    PINECONE_ENV: str = ""
    PINECONE_INDEX: str = ""
    EMBEDDING_MODEL: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()