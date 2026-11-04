from fastapi import APIRouter, HTTPException
import anthropic
from schemas import ChatRequest, ChatResponse
from services.claude_client import get_reply, reset_conversation

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        reply = get_reply(request.message)
    except anthropic.APIError:
        raise HTTPException(
            status_code=502,
            detail="The AI service is temporarily unuvailable. Please try again in a moment",
        )
    return {"reply" : reply}

@router.post("/reset")
def reset():
    reset_conversation()
    return {"message": "Conversation has been reset."}