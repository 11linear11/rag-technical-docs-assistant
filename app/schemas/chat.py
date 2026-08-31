from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    query: str = Field(...,min_length=1,description="The query to be asked to the agent")
    thread_id: Optional[str] = Field(None,description="The thread id to be used for the query")

class ChatResponse(BaseModel):
    response: str
    thread_id: str

