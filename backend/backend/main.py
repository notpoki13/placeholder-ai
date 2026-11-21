
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Placeholder AI")

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporary development setting
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Placeholder AI is running!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="API key is not configured."
        )

    try:
        response = await client.responses.create(
            model="gpt-6.2-sol",
            instructions=(
                "You are Placeholder, a helpful, "
                "professional AI assistant."
            ),
            input=request.message,
        )

        return {"reply": response.output_text}

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to contact the AI service."
        )
