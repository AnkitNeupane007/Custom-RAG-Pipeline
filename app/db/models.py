from sqlalchemy import Column, func
from sqlmodel import SQLModel, Field, Integer
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from pydantic import BaseModel


class ChunkModel(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, autoincrement=True)
    )
    text: str = Field(nullable=False)
    document_id: str = Field(nullable=False)
    page_number: int = Field(nullable=False)
    chunk_number: int = Field(nullable=False)
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

class QueryRequest(BaseModel):
    query: str
    top_k: int = 10
    document_id: str | None = None


class DocumentIngestRequest(BaseModel):
    path_to_document: str
    document_id: str
    strategy: str = "paragraph"
    chunk_size: int = 100
    overlap: int = 20