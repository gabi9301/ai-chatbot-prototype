import anthropic
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import crud
from anthropic.types import MessageParam

load_dotenv()

client = anthropic.Anthropic()

def _to_message_param(role: str, content: str) -> MessageParam:
    if role == "user":
        return {"role": "user", "content": content}
    if role == "assistant":
        return {"role": "assistant", "content": content}
    raise ValueError(f"Unexpected message role: {role}")

MODEL = "claude-haiku-5-5"
SYSTEM_PROMPT = "You are a friendly and helpful assistant. Keep yourt answers clear and consice."

def get_reply(
    db: Session,
    message: str,
    conversation_id: int | None,
    language: str,
) -> tuple[str, int]:
    # 1. Load the existing thread's history, or start empty for a new one.
    if conversation_id is None:
        conversation = None
        history = []
    else:
        conversation = crud.get_conversation(db, conversation_id)
        if conversation is None:
            raise ValueError("Conversation not found")
        history = [
            _to_message_param(m.role, m.content)
            for m in crud.get_messages(db, conversation.id)
        ]
    # 2. Add the new user turn, then ask Claude.
    history.append({"role" : "user", "content" : message})
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=history,
    )
    reply = next((block.text for block in response.content if block.type == "text"), "")

    # 3. Only after success: create the thread if needed, then persist both turns.
    if conversation is None:
        conversation = crud.create_conversation(db, title=None, language=language)
    crud.add_message(db, conversation.id, role="user", content=message)
    crud.add_message(db, conversation.id, role="assistant", content=reply)
    
    return reply, conversation.id

def stream_reply(
    db: Session,
    message: str,
    conversation_id: int | None,
    language: str,
):
    # 1. Get the existing conversation or make a new one
    if conversation_id is None:
        conversation = None
        history = []
    else:
        conversation = crud.get_conversation(db, conversation_id)
        if conversation is None:
            raise ValueError("Conversation not found")
        history = [
            _to_message_param(m.role, m.content)
            for m in crud.get_messages(db, conversation.id)
        ]
    history.append({"role": "user", "content": message})

    # 2. Streaming: stream words while add them to full_text

    full_text = ""
    with client.messages.stream(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=history,
    ) as stream:
        for text in stream.text_stream:
            full_text += text
            yield {"type":"delta", "text": text}
    
    # 3. Save only after streaming went successful
    if conversation is None:
        conversation = crud.create_conversation(db, title=None, language=language)
    crud.add_message(db, conversation.id, role="user", content=message)
    crud.add_message(db, conversation.id, role="assistant", content=full_text)

    # 4. Return conversation_id at the end
    yield {"type": "done", "conversation_id": conversation.id}
