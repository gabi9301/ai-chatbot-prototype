import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from services import ingest
from schemas import DocumentRead

def test_ingest_document_chunks_embeds_and_stores(monkeypatch):
    # chunk_text and embed_texts are tested elsewhere; here we isolate the
    # orchestration by mocking them, plus the crud call (the DB boundary).
    monkeypatch.setattr(ingest, "chunk_text", lambda content: ["chunk one", "chunk two"])
    fake_embed = MagicMock(return_value=[[0.1, 0.2], [0.3, 0.4]])
    monkeypatch.setattr(ingest, "embed_texts", fake_embed)

    stored = DocumentRead(
        id=1,
        source="notes.txt",
        content="full text",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    fake_create = MagicMock(return_value=stored)
    monkeypatch.setattr(ingest.crud, "create_document_with_chunks", fake_create)

    db = MagicMock()
    result = ingest.ingest_document(db, "full text", source="notes.txt")

    # chuhnks produced by chunk_text are handed to embed_texts
    fake_embed.assert_called_once_with(["chunk one", "chunk two"])
    # source, content, chunks, and embeddings are wired into cruid in order
    fake_create.assert_called_once_with(
        db,
        "notes.txt",
        "full text",
        ["chunk one", "chunk two"],
        [[0.1, 0.2], [0.3, 0.4]],
    )
    # the DTO from crud is returned unchanged
    assert result is stored

def test_ingest_document_rejects_empty_content(monkeypatch):
    # No chunks -> refuse before any embedding call or DB write happens.
    monkeypatch.setattr(ingest, "chunk_text", lambda content: [])
    fake_embed = MagicMock()
    monkeypatch.setattr(ingest, "embed_texts", fake_embed)
    fake_create = MagicMock()
    monkeypatch.setattr(ingest.crud, "create_document_with_chunks", fake_create)

    db = MagicMock()
    with pytest.raises(ValueError):
        ingest.ingest_document(db, "   ")

    fake_embed.assert_not_called()
    fake_create.assert_not_called()