from datetime import datetime, timezone
from unittest.mock import MagicMock
import pytest

from services import retrieval
from schemas import ChunkRead

def test_retrieve_chunks_embeds_and_searches(monkeypatch):
    # embed_texts and the pgvector search are tested elsewhere; here we isolate
    # the orchestration by mocking them (embedding call + the DB boundary).
    fake_embed = MagicMock(return_value=[[0.1, 0.2, 0.3]])
    monkeypatch.setattr(retrieval, "embed_texts", fake_embed)

    hits = [
        ChunkRead(
            id=1,
            document_id=7,
            chunk_index=0,
            content="closest chunk",
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        ),
    ]
    fake_search = MagicMock(return_value=hits)
    monkeypatch.setattr(retrieval.crud, "search_similar_chunks", fake_search)

    db = MagicMock()
    result = retrieval.retrieve_chunks(db, "what happend?", k=3)

    fake_embed.assert_called_once_with(["what happend?"])
    fake_search.assert_called_once_with(db, [0.1, 0.2, 0.3], 3)
    assert result is hits

def test_retrieve_chunks_rejects_empty_query(monkeypatch):
    # Blank query -> refuse before any embedding call or DB search happens.
    fake_embed = MagicMock()
    monkeypatch.setattr(retrieval, "embed_texts", fake_embed)
    fake_search = MagicMock()
    monkeypatch.setattr(retrieval.crud, "search_similar_chunks", fake_search)

    db = MagicMock()
    with pytest.raises(ValueError):
        retrieval.retrieve_chunks(db, "   ")

    fake_embed.assert_not_called()
    fake_search.assert_not_called()