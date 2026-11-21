from fastapi.testclient import TestClient
from unittest.mock import MagicMock, ANY
import anthropic
import json
import httpx
from main import app
from database import get_db
from i18n import t
from routers import rag

def _fake_db():
    yield MagicMock()

app.dependency_overrides[get_db] = _fake_db
client = TestClient(app)


EVENTS = [
    {"type": "delta", "text": "This "},
    {"type": "delta", "text": "is "},
    {"type": "delta", "text": "a fake answer."},
    {"type": "done"},
]

def test_ask_returns_answer(monkeypatch):
    fake_answer = MagicMock(return_value="This is my answer.")
    monkeypatch.setattr(rag, "answer_question", fake_answer)

    response = client.post("/ask", json={"query": "What is your answer?", "language": "en", "k": 3})
    assert response.status_code == 200
    assert response.json() == {"answer": "This is my answer."}
    fake_answer.assert_called_once()

def test_ask_uses_default_language_and_k(monkeypatch):
    fake_answer = MagicMock(return_value="This is my answer.")
    monkeypatch.setattr(rag, "answer_question", fake_answer)
    client.post("/ask", json={"query": "What is your answer?"})
    fake_answer.assert_called_once_with(ANY, "What is your answer?", "en", 5)

def test_ask_requires_query():
    response = client.post("/ask", json={})
    assert response.status_code == 422

def test_ask_stream(monkeypatch):
    monkeypatch.setattr(rag, "stream_answer", MagicMock(return_value=EVENTS))
    response = client.post("/ask/stream", json={"query":"What is your stream answer?", "language":"en", "k" : 3})
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    assert "data" in response.text
    expected = "".join(f"data: {json.dumps(e)}\n\n" for e in EVENTS)
    assert response.text == expected

def test_ask_stream_error(monkeypatch):
    def _raise(*args, **kwargs):
        raise anthropic.APIError(
            "boom", request=httpx.Request("POST", "http://test"), # type: ignore[arg-type]
            body=None,
        )
    monkeypatch.setattr(rag, "stream_answer", _raise)
    response = client.post("/ask/stream", json={"query":"What is your stream answer?", "language":"en", "k" : 3})
    error = {"type": "error", "detail": t("en", "ai_unavailable")}
    assert response.text == f"data: {json.dumps(error)}\n\n"