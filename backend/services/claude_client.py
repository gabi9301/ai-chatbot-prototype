import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

MODEL = "claude-haiku-5-5"
SYSTEM_PROMPT = "You are a friendly and helpful assistant. Keep yourt answers clear and consice."

conversation_history = []

def get_reply(message: str) -> str:
    conversation_history.append({"role": "user", "content": message})

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=conversation_history,
        )

    except anthropic.APIError:
        # Roll back the dangling user message, then let the caller decide
        # how tro response to the outside world (HTTP, etc.).
        conversation_history.pop()
        raise

    reply = next((block.text for block in response.content if block.type == "text"), "")
    conversation_history.append({"role" : "assistant", "content": reply})
    return reply

def reset_conversation() -> None:
    conversation_history.clear()