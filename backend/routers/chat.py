from fastapi.responses import StreamingResponse
import json
import crud
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import anthropic
from database import get_db
from schemas import ChatRequest, ChatResponse
from services.claude_client import get_reply, stream_reply

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

@router.post("/chat/stream", response_class=StreamingResponse)
def chat_stream(request: ChatRequest, db: Session = Depends(get_db)):
    # Check before streaming starts -> wrong ids raise 404 error
        if request.conversation_id is not None and crud.get_conversation(db, request.conversation_id) is None:
            raise HTTPException(status_code=404, detail="Conversation not found")

        def event_stream():
            try:
                for event in stream_reply(db, request.message, request.conversation_id, request.language):
                    yield f"data: {json.dumps(event)}\n\n" 
            except anthropic.APIEroor:
                error = {"type": "error", "detail": "The AI service is temporarily unavailable."}
                yield f"data: {json.dumps(error)}\n\n"
        return StreamingResponse(event_stream(), media_type="text/event-stream")