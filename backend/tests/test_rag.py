from fastapi.testclient import TestClient
from unittest.mock import MagicMock, ANY
from main import app
from database import get_db
from routers import rag

from schemas import AskResponse

def _fake_db():
    yield MagicMock()

app.dependency_overrides[get_db] = _fake_db
client = TestClient(app)

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