from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None
    language: str = "en"


class ChatResponse(BaseModel):
    reply: str
    conversation_id: int


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role: str
    content: str
    created_at: datetime


class ConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str | None
    language: str
    created_at: datetime


class ConversationDetail(ConversationRead):
    messages: list[MessageRead] = []

class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    source: str | None
    content: str
    created_at: datetime

class ChunkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    document_id: int
    chunk_index: int
    content: str
    created_at: datetime

class IngestRequest(BaseModel):
    content: str
    source: str | None = None
    language: str = "en"

class AskRequest(BaseModel):
    query: str
    language: str = "en"
    k: int = 5

class AskResponse(BaseModel):
    answer: str