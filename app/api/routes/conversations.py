
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.conversation import (
    ConversationCreate,
    ConversationDetailResponse,
    ConversationListResponse,
    ConversationResponse,
)
from app.services import chat_service

router = APIRouter(prefix="/conversations", tags=["conversations"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=ConversationListResponse)
async def list_conversations(
    db: DbSession,
    skip: int = 0,
    limit: int = 50,
) -> ConversationListResponse:
    conversations, total = await chat_service.list_conversations(db, skip=skip, limit=limit)
    return ConversationListResponse(conversations=conversations, total=total)


@router.post("", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    payload: ConversationCreate, db: DbSession
) -> ConversationResponse:
    from app.models.conversation import Conversation

    conversation = Conversation(
        title=payload.title,
        provider=payload.provider,
        model=payload.model,
    )
    db.add(conversation)
    await db.flush()
    await db.refresh(conversation)
    return ConversationResponse.model_validate(conversation)


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: str, db: DbSession
) -> ConversationDetailResponse:
    conversation = await chat_service.get_conversation(db, conversation_id)
    return ConversationDetailResponse.model_validate(conversation)


@router.delete("/{conversation_id}", status_code=204)
async def delete_conversation(conversation_id: str, db: DbSession) -> None:
    await chat_service.delete_conversation(db, conversation_id)
