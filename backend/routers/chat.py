from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import anthropic
from database import get_db
from schemas import ChatRequest, ChatResponse
from services.claude_client import get_reply

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        reply, conversation_id = get_reply(
            db,
            request.message,
            request.conversation_id,
            request.language,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Conversation not found")
    except anthropic.APIError:
        raise HTTPException(
            status_code=502,
            detail="The AI service is temporarily unavailable. Please try again in a moment",
        )
    return {"reply" : reply, "conversation_id": conversation_id}