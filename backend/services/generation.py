import anthropic
from dotenv import load_dotenv
from schemas import ChunkRead
from sqlalchemy.orm import Session
from services.retrieval import retrieve_chunks

from i18n import t


MODEL = "claude-haiku-5-5"

load_dotenv()
client = anthropic.Anthropic()

def build_context(chunks: list[ChunkRead]) -> str:
    """Format retrieved chunks into a reference block for the prompt.

    Each chunk is numbered so the model can tell the sources apart and, if
    asked, cite them.

    Args:
        chunks: The chunks retrieved for the query, most relevant first.

    Returns:
        The chunks joined into a single reference string, or an empty string
        if there are none.
    """
    return "\n\n".join(
        f"[Source {index}] {chunk.content}"
        for index, chunk in enumerate(chunks, start=1)

    )

def answer_question(db: Session, query: str, language: str = "en", k: int = 5) -> str:
    chunks = retrieve_chunks(db, query, k)

    if not chunks:
        return t(language, "no_context_for_rag")
    
    context = build_context(chunks)

    prompt = f"""
    Answer the following query based on the documents provided below:
    <query>
    {query}
    </query>
    You have access to the following documents which are meant to provide context as you answer the query:
    <documents>
    {context}
    </documents>
    """

    response = client.messages.create(
            model=MODEL,
            system=t(language, "system_prompt"),
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
    )

    reply = next((block.text for block in response.content if block.type == "text"), "")

    return reply




