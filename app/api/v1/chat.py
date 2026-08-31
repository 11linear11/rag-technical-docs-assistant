from fastapi import APIRouter,status, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.agent.exec import chat_with_agent
import uuid

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("",response_model=ChatResponse,status_code=status.HTTP_200_OK)
async def chat(request: ChatRequest ):
    try:
        session_id = request.thread_id or str(uuid.uuid4())
        response = await chat_with_agent(request.query, session_id)
        return ChatResponse(response=response, thread_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))