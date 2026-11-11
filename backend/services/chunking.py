def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:

    """Split text into overlapping chunks for embedding.

    Args:
        text: The source text to split.
        chunk_size: Maximum number of characters per chunk.
        overlap: Number of characters carried over from the end of the previous chunk into the text, so context isn't lost at the boundary between chunks.

    Returns:
        A list of text chunks. Empty if the text is blank.
    """
    
    if chunk_size <= 0 :
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    text = text.strip()
    if not text:
        return []
    chunks : list[str] = []
    start = 0
    step = chunk_size - overlap
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += step
    return chunks
