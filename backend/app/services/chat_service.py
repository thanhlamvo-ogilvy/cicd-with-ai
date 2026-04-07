from collections.abc import AsyncGenerator

import structlog
from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.chat import ChatRequest
from app.services.providers.anthropic import AnthropicProvider
from app.services.providers.base import AIProvider, ChatMessage
from app.services.providers.google import GoogleProvider
from app.services.providers.openai import OpenAIProvider

log = structlog.get_logger(__name__)


def get_provider(provider_name: str) -> AIProvider:
    """Return the appropriate AI provider instance."""
    if provider_name == "openai":
        api_key = settings.openai_api_key
        base_url = settings.openai_base_url
        if not api_key and not base_url:
            raise HTTPException(
                status_code=400, detail="Provider 'openai' is not configured"
            )
        return OpenAIProvider(api_key=api_key, base_url=base_url or None)

    providers: dict[str, tuple[str, type[AIProvider]]] = {
        "anthropic": (settings.anthropic_api_key, AnthropicProvider),
        "google": (settings.google_api_key, GoogleProvider),
    }

    if provider_name not in providers:
        raise HTTPException(status_code=400, detail=f"Unknown provider: {provider_name}")

    api_key, provider_cls = providers[provider_name]
    if not api_key:
        raise HTTPException(
            status_code=400, detail=f"Provider '{provider_name}' is not configured"
        )

    return provider_cls(api_key)


async def get_or_create_conversation(
    db: AsyncSession, request: ChatRequest
) -> Conversation:
    """Get existing conversation or create a new one."""
    if request.conversation_id:
        result = await db.execute(
            select(Conversation).where(Conversation.id == request.conversation_id)
        )
        conversation = result.scalar_one_or_none()
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation

    conversation = Conversation(
        provider=request.provider,
        model=request.model,
        title=request.content[:50],
    )
    db.add(conversation)
    await db.flush()
    await db.refresh(conversation)
    log.info("conversation_created", conversation_id=str(conversation.id))
    return conversation


async def save_message(
    db: AsyncSession, conversation_id: str, role: str, content: str
) -> Message:
    """Save a message to the database."""
    message = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(message)
    await db.flush()
    await db.refresh(message)
    return message


async def get_conversation_messages(
    db: AsyncSession, conversation_id: str
) -> list[ChatMessage]:
    """Load all messages for a conversation as ChatMessage objects."""
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    return [ChatMessage(role=m.role, content=m.content) for m in result.scalars().all()]


async def stream_chat_response(
    db: AsyncSession, request: ChatRequest
) -> AsyncGenerator[str, None]:
    """Orchestrate the full chat flow: save user message, stream AI response, save result."""
    provider = get_provider(request.provider)
    conversation = await get_or_create_conversation(db, request)

    await save_message(db, conversation.id, "user", request.content)
    await db.commit()

    messages = await get_conversation_messages(db, conversation.id)

    log.info(
        "chat_request",
        conversation_id=str(conversation.id),
        provider=request.provider,
        model=request.model,
    )

    full_response = ""
    async for token in provider.stream_chat(messages, request.model):
        full_response += token
        yield token

    await save_message(db, conversation.id, "assistant", full_response)
    await db.commit()

    log.info(
        "chat_response_complete",
        conversation_id=str(conversation.id),
        response_length=len(full_response),
    )


async def list_conversations(
    db: AsyncSession, skip: int = 0, limit: int = 50
) -> tuple[list[Conversation], int]:
    """List conversations with pagination."""
    count_result = await db.execute(select(func.count()).select_from(Conversation))
    total = count_result.scalar_one()

    result = await db.execute(
        select(Conversation)
        .order_by(Conversation.updated_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all()), total


async def get_conversation(db: AsyncSession, conversation_id: str) -> Conversation:
    """Get a single conversation with its messages."""
    result = await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.messages))
        .where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


async def delete_conversation(db: AsyncSession, conversation_id: str) -> None:
    """Delete a conversation and all its messages."""
    conversation = await get_conversation(db, conversation_id)
    await db.delete(conversation)
    await db.flush()
    log.info("conversation_deleted", conversation_id=str(conversation_id))
