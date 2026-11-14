from sqlalchemy.orm import Session

import crud
from schemas import DocumentRead
from services.chunking import chunk_text
from services.embedding import embed_texts

def ingest_document(db: Session, content: str, source: str | None = None) -> DocumentRead:
    """Chunk, embed, and store a document in one pass.

    The document text is split into overlapping chunks, each chunk is
    embedded, and the document and its chunks are persisted together.

    Args:
        db: Database session.
        content: The raw document text to ingest.
        source: Optional origin of the document(e.g. a filename or URL).

    Returns:
        The stored document as a DocumentRead DTO.

    Raises:
        ValueError: If the content has no chunkable text.
    """
    chunks = chunk_text(content)
    if not chunks:
        raise ValueError("Cannot ingest a document with no chunkable content.")
    embeddings = embed_texts(chunks)
    return crud.create_document_with_chunks(db, source, content, chunks, embeddings)