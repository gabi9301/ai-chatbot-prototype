from datetime import datetime, timezone
from types import SimpleNamespace

from unittest.mock import MagicMock
from schemas import ChunkRead

from services import generation
from i18n import t

MODEL = "claude-haiku-5-5"
FAKE_TEXT = "This is a fake answer for the test."

def _create_fake_answer():
    return SimpleNamespace(
        id="msg_fake_1",
        type="message",
        role="assistant",
        model=MODEL,
        content=[
            SimpleNamespace(
                type="text",
                text=FAKE_TEXT
            )
        ]
    )
    

def test_answer_question_with_context(monkeypatch):
    hits = [
            ChunkRead(
                id=1,
                document_id=1,
                chunk_index=0,
                content="chunk_1",
                created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            ),
            ChunkRead(
                id=2,
                document_id=1,
                chunk_index=1,
                content="chunk_2",
                created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            ),
        ]
    fake_chunks = MagicMock(return_value=hits)
    monkeypatch.setattr(generation, "retrieve_chunks",fake_chunks)

    fake_answer = MagicMock(return_value=_create_fake_answer())
    monkeypatch.setattr(generation.client.messages, "create", fake_answer) 

    db = MagicMock()
    result = generation.answer_question(db, "What is happening?", "en")
    fake_chunks.assert_called_once()
    fake_answer.assert_called_once()
    assert result == FAKE_TEXT

def test_answer_question_without_context(monkeypatch):
    hits = []
    empty_chunks = MagicMock(return_value=hits)
    monkeypatch.setattr(generation, "retrieve_chunks", empty_chunks)

    fake_answer = MagicMock(return_value=_create_fake_answer())
    monkeypatch.setattr(generation.client.messages, "create", fake_answer)

    db = MagicMock()
    result = generation.answer_question(db, "What is happening?", "en")

    fake_answer.assert_not_called()
    assert result == t("en", "no_context_for_rag")


