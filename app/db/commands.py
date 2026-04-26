from app.db.database import async_session

# store the fields of id, text, chunk_number into the database
async def store_chunks(chunks, path_to_document):
    async with async_session() as session:
        from app.db.models import ChunkModel
        objects = []

        for chunk in chunks:
            obj = ChunkModel(
                # id=chunk["chunk_id"],
                text=chunk["text"],
                document_id=path_to_document.split('/')[-1].split('.')[0],
                page_number=chunk["page_number"],
                chunk_number=chunk["chunk_number"]
            )
            objects.append(obj)

        session.add_all(objects)
        await session.commit()

# fetch all chunks from the database with that document_id
async def fetch_chunks(document_id: str = None):
    async with async_session() as session:
        from app.db.models import ChunkModel
        from sqlalchemy.future import select
        query = select(ChunkModel)
        if document_id:
            query = query.where(ChunkModel.document_id == document_id)
        result = await session.execute(query)
        return result.scalars().all()

# fetch chunks from the database by a list of chunk IDs
async def fetch_chunks_by_ids(chunk_ids: list[int]):
    async with async_session() as session:
        from app.db.models import ChunkModel
        from sqlalchemy.future import select
        query = select(ChunkModel).where(ChunkModel.id.in_(chunk_ids))
        result = await session.execute(query)
        return result.scalars().all() # returns orm objects
