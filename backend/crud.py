from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from models import Conversation, Message
from schemas import ConversationRead, MessageRead

# --- For internal use : the only place where orm models are directly handled ---

def _get_conversation_model(db: Session, conversation_id: int) -> Conversation | None:
    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.deleted_at.is_(None),
    )
    return db.scalars(stmt).first()

# --- Public repository API: only return DTO ---

def create_conversation(db: Session, title: str | None, language: str) -> ConversationRead:
    conversation = Conversation(title=title, language=language)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return ConversationRead.model_validate(conversation)

def get_conversation(db: Session, conversation_id: int) -> ConversationRead | None:
    conversation = _get_conversation_model(db, conversation_id)
    if conversation is None:
        return None
    return ConversationRead.model_validate(conversation)

def add_message(db: Session, conversation_id: int, role: str, content: str) -> MessageRead:
    message = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return MessageRead.model_validate(message)

def get_messages(db: Session, conversation_id: int) -> list[MessageRead]:
    stmt = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = db.scalars(stmt).all()
    return [MessageRead.model_validate(m) for m in messages]

def list_conversations(db: Session) -> list[ConversationRead]:
    stmt = (
        select(Conversation)
        .where(Conversation.deleted_at.is_(None))
        .order_by(Conversation.created_at.desc())
    )
    conversations = db.scalars(stmt).all()
    return [ConversationRead.model_validate(c) for c in conversations]

def soft_delete_conversation(db: Session, conversation_id: int) -> ConversationRead | None:
    conversation = _get_conversation_model(db, conversation_id)
    if conversation is None:
        return None
    conversation.deleted_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(conversation)
    return ConversationRead.model_validate(conversation)