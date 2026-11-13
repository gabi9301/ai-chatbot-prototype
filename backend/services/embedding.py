from collections.abc import Sequence

import voyageai

EMBEDDING_MODEL = "voyage-3.5"
EMBEDDING_DIM = 1024

_client = voyageai.Client() # pyright: ignore[reportPrivateImportUsage]

def embed_texts(texts: list[str]) -> Sequence[Sequence[float]]:
    """Embed a batch of texts with Voyage.

    Args:
        texts: The texts to embed, one vector produced per item.

    Returns:
        A list of embedding vectors, each EMBEDDING_DIM floats long,
        aligned wtih the input order. Empty if texts is empty.
    """ 
    if not texts:
        return []
    result = _client.embed(texts, model=EMBEDDING_MODEL)
    return result.embeddings

