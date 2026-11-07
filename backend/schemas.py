from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


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