from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .agent import agent_manager

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/ask")
async def chat_with_agent(request: ChatRequest):
    try:
        answer = agent_manager.run(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))