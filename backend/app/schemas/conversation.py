from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime


class ConversationBase(BaseModel):
    provider: str = Field(default="openai", max_length=50)
    model: str = Field(default="gpt-4o", max_length=100)


class ConversationCreate(ConversationBase):
    title: str = Field(default="New Chat", max_length=255)


class ConversationResponse(ConversationBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    created_at: datetime
    updated_at: datetime


class ConversationDetailResponse(ConversationResponse):
    messages: list[MessageResponse] = []


class ConversationListResponse(BaseModel):
    conversations: list[ConversationResponse]
    total: int
