from pydantic import BaseModel
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import anthropic

load_dotenv()

app = FastAPI()
client = anthropic.Anthropic()

@app.get("/")
def read_root():
  return {"message" : "hello! My first server is alive!"}


@app.get("/test-claude")
def test_claude():
    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Say hello and introduce yourself in one short, friendly sentence"}
        ]
    )
    reply = next((block.text for block in response.content if block.type == "text"), "")
    return {"reply": reply}

class ChatRequest(BaseModel):
    message: str

SYSTEM_PROMPT = "You are a friendly and helpful assistant. Keep your answers clear and concise."


conversation_history = []

@app.post("/chat")
def chat(request: ChatRequest):
    conversation_history.append({"role": "user", "content": request.message})

    try:
        response = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=conversation_history,
        )
    except anthropic.APIError as e:
        # The API call failed, so roll back the user message just added,
        # keeping the conversation history clean for the next request.
        conversation_history.pop()
        raise HTTPException(
            status_code=502,
            detail="The AI service is temporally unavailable. Please try again in a moment."
        )
    
    reply = next((block.text for block in response.content if block.type == "text"), "")

    conversation_history.append({"role": "assistant", "content": reply})
    return {"reply" : reply}

@app.post("/reset")
def reset():
    conversation_history.clear()
    return {"message" : "Conversation has been reset."}