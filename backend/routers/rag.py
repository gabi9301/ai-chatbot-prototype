from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import anthropic
import json
from i18n import t
from database import get_db
from schemas import IngestRequest, DocumentRead, AskRequest, AskResponse
from services.ingest import ingest_document
from services.generation import answer_question, stream_answer

router = APIRouter()

@router.post("/ingest", response_model=DocumentRead)
def ingest(request: IngestRequest, db: Session = Depends(get_db)):
    try:
        document = ingest_document(
            db,
            request.content,
            request.source
        )
    except ValueError:
        raise HTTPException(status_code=422, detail=t(request.language, "no_content_to_ingest"))
    return document

@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, db: Session = Depends(get_db)):
    answer = answer_question(
        db,
        request.query,
        request.language,
        request.k
    )
    return AskResponse(answer = answer)

@router.post("/ask/stream", response_class=StreamingResponse)
def ask_stream(request: AskRequest, db: Session = Depends(get_db)):
    def event_stream():
        try:
            for event in stream_answer(
                db,
                request.query,
                request.language,
                request.k,
            ):
                yield f"data: {json.dumps(event)}\n\n"
        except anthropic.APIError:
            error = {"type": "error", "detail": t(request.language, "ai_unavailable")}
            yield f"data: {json.dumps(error)}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
