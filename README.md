# AI Chatbot Prototype

A simple conversational chatbot backend built with FastAPI and the Anthropic Claude API.
It keeps track of the conversation across multiple messages and handles API errors gracefully.

## Features

- Multi-turn chat endpoint that remembers conversation history
- Powered by Anthropic's Claude model
- Graceful error handling with clear HTTP responses
- Reset endpoint to clear the conversation

## Tech Stack

- Python
- FastAPI
- Anthropic Claude API
- Uvicorn (ASGI server)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/gabi9301/ai-chatbot-prototype.git
   cd ai-chatbot-prototype
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API key:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ```

## Running the Server

```
uvicorn main:app --reload
```

The server runs at `http://127.0.0.1:8000`.
Interactive API docs are available at `http://127.0.0.1:8000/docs`.

## API Endpoints

| Method | Endpoint  | Description                      |
|--------|-----------|----------------------------------|
| GET    | `/`       | Health check                     |
| POST   | `/chat`   | Send a message and get a reply   |
| POST   | `/reset`  | Clear the conversation history   |

### Example: POST `/chat`

Request body:
```json
{
  "message": "Hello! Who are you?"
}
```

Response:
```json
{
  "reply": "Hi! I'm a friendly assistant here to help you."
}
```