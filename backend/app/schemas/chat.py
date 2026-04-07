from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    conversation_id: str | None = None
    content: str = Field(..., min_length=1)
    provider: str = Field(default="openai", max_length=50)
    model: str = Field(default="gpt-4o", max_length=100)
