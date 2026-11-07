from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from models import Conversation, Message

def create_conversation(db: Session, title: str | None, language: str) -> Conversation:
    conversation = Conversation(title=title, language=language)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_conversation(db: Session, conversation_id: int) -> Conversation | None:
    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.deleted_at.is_(None),
    )
    return db.scalars(stmt).first()

def add_message(db: Session, conversation_id: int, role: str, content: str) -> Message:
    message = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_messages(db: Session, conversation_id: int) -> list[Message]:
    stmt = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    return list(db.scalars(stmt).all())

def list_conversations(db: Session) -> list[Conversation]:
    stmt = (
        select(Conversation)
        .where(Conversation.deleted_at.is_(None))
        .order_by(Conversation.created_at.desc())
    )
    return list(db.scalars(stmt).all())

def soft_delete_conversation(db: Session, conversation_id: int) -> Conversation | None:
    conversation = get_conversation(db, conversation_id)
    if conversation is None:
        return None
    conversation.deleted_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(conversation)
    return conversation