from sqlalchemy.orm import Session

import crud
from schemas import ChunkRead
from services.embedding import embed_texts

def retrieve_chunks(db: Session, query: str, k: int = 5) -> list[ChunkRead]:
    """Find the chunks most semantically similar to a query.

    The query is embedded with the same model used for the stored chunks,
    then compared against them by vector similarity to return the closest
    matches.

    Args:
        db: Database session.
        query: The natural-language text to search for.
        k: The maximum number of chunks to return.

    Returns:
        The top-k most similar chunks as ChunkRead DTOS, closest first.
    """
    if not query.strip():
        raise ValueError("Cannot retrieve against an empty query")
    embedding = embed_texts([query])[0]
    return crud.search_similar_chunks(db, embedding, k)