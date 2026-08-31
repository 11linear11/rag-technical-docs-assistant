"""Chat API Endpoints (v1).

Exposes the REST API route for interacting with the LangGraph RAG Agent.
"""

import uuid
from fastapi import APIRouter, HTTPException, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.agent.exec import chat_with_agent

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with Technical Documentation Assistant",
    description=(
        "Sends a query to the LangGraph RAG assistant. The assistant retrieves relevant "
        "technical documentation chunks, reasons over them, and generates an accurate, "
        "grounded response with document citations."
    ),
)
async def chat(request: ChatRequest) -> ChatResponse:
    """Handle chat queries and dispatch them to the LangGraph agent.

    Args:
        request (ChatRequest): The incoming chat request containing query and optional thread_id.

    Returns:
        ChatResponse: The agent's grounded response and session thread_id.

    Raises:
        HTTPException: If an unexpected error occurs during agent execution.
    """
    try:
        # Use existing thread_id or generate a new UUID for session persistence
        session_id = request.thread_id or str(uuid.uuid4())
        response = await chat_with_agent(request.query, session_id)
        return ChatResponse(response=response, thread_id=session_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}",
        )