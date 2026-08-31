"""Chat schemas module.

Defines Pydantic request and response models for the chat endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for interacting with the AI documentation agent.

    Attributes:
        query (str): The user's query or prompt. Must be non-empty.
        thread_id (Optional[str]): Unique thread/session ID for conversation state persistence.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="The technical query or question asked to the assistant.",
        examples=["How do I create custom exception handlers in FastAPI?"],
    )
    thread_id: Optional[str] = Field(
        None,
        description="Unique thread identifier for multi-turn conversational memory. If omitted, a new UUID is generated.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )


class ChatResponse(BaseModel):
    """Response schema returned by the AI documentation agent.

    Attributes:
        response (str): The generated response text grounded in documentation.
        thread_id (str): The active thread identifier for the ongoing conversation.
    """

    response: str = Field(
        ...,
        description="The assistant's generated response, grounded in technical documentation and containing citations.",
    )
    thread_id: str = Field(
        ...,
        description="The session/thread identifier used for this interaction.",
    )


