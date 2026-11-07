import anthropic
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import crud

load_dotenv()

client = anthropic.Anthropic()

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
            {"role": m.role, "content": m.content}
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
