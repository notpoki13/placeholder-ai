
import os
import secrets

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from openai import AsyncOpenAI
from pydantic import BaseModel

app = FastAPI(title="Placeholder AI")

security = HTTPBearer()

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-6.2-sol"


class ChatRequest(BaseModel):
    message: str


def check_access(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    expected = os.getenv("PLACEHOLDER_ACCESS_TOKEN")

    if not expected:
        raise HTTPException(
            status_code=503,
            detail="Backend access is not configured."
        )

    if not secrets.compare_digest(
        credentials.credentials, expected
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect access password."
        )


@app.get("/")
def home():
    return {"message": "Placeholder AI is running!"}


@app.post("/chat")
async def chat(
    request: ChatRequest,
    authorized: None = Depends(check_access)
):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key is missing."
        )

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:
        response = await client.responses.create(
            model=MODEL,
            instructions=(
                "You are Placeholder, a helpful, "
                "professional AI assistant."
            ),
            input=request.message,
            max_output_tokens=800
        )

        return {
            "reply": response.output_text,
            "model": MODEL
        }

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to contact OpenAI."
        )
