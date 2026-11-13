from unittest.mock import MagicMock

from services import embedding

def test_embed_texts_empty_returns_empty():
    # Empty imput short-circuits: the API must not be called at all.
    assert embedding.embed_texts([]) == []

def test_embed_texts_returns_one_vector_per_input(monkeypatch):
    fake_result = MagicMock()
    fake_result.embeddings=[[0.1, 0.2], [0.3, 0.4]]
    fake_embed = MagicMock(return_value=fake_result)
    monkeypatch.setattr(embedding._client, "embed", fake_embed)

    vectors = embedding.embed_texts(["hello", "world"])

    assert vectors == [[0.1, 0.2], [0.3, 0.4]]
    fake_embed.assert_called_once_with(
        ["hello", "world"], model=embedding.EMBEDDING_MODEL
    )