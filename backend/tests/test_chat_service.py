"""Tests for chat_service: provider selection and core service functions."""

from collections.abc import AsyncGenerator
from unittest.mock import MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ProviderConfigurationError, ProviderNotFoundError
from app.models.conversation import Conversation
from app.schemas.chat import ChatRequest
from app.services import chat_service
from app.services.providers.base import AIProvider, ChatMessage


class TestGetProvider:
    def test_openai_with_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(chat_service.settings, "openai_api_key", "sk-test")
        monkeypatch.setattr(chat_service.settings, "openai_base_url", "")
        from app.services.providers.openai import OpenAIProvider

        provider = chat_service.get_provider("openai")
        assert isinstance(provider, OpenAIProvider)

    def test_openai_with_base_url_only(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(chat_service.settings, "openai_api_key", "")
        monkeypatch.setattr(chat_service.settings, "openai_base_url", "http://localhost:11434")
        from app.services.providers.openai import OpenAIProvider

        provider = chat_service.get_provider("openai")
        assert isinstance(provider, OpenAIProvider)

    def test_openai_not_configured_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(chat_service.settings, "openai_api_key", "")
        monkeypatch.setattr(chat_service.settings, "openai_base_url", "")
        with pytest.raises(ProviderConfigurationError):
            chat_service.get_provider("openai")

    def test_anthropic_configured(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(chat_service.settings, "anthropic_api_key", "ant-test")
        from app.services.providers.anthropic import AnthropicProvider

        provider = chat_service.get_provider("anthropic")
        assert isinstance(provider, AnthropicProvider)

    def test_anthropic_not_configured_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(chat_service.settings, "anthropic_api_key", "")
        with pytest.raises(ProviderConfigurationError):
            chat_service.get_provider("anthropic")

    def test_google_configured(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(chat_service.settings, "google_api_key", "google-test")
        from app.services.providers.google import GoogleProvider

        provider = chat_service.get_provider("google")
        assert isinstance(provider, GoogleProvider)

    def test_google_not_configured_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(chat_service.settings, "google_api_key", "")
        with pytest.raises(ProviderConfigurationError):
            chat_service.get_provider("google")

    def test_unknown_provider_raises(self) -> None:
        with pytest.raises(ProviderNotFoundError, match="Unknown provider"):
            chat_service.get_provider("some-unknown-llm")


@pytest.mark.asyncio
async def test_save_message(db_session: AsyncSession) -> None:
    conv = Conversation(provider="openai", model="gpt-4o", title="Test")
    db_session.add(conv)
    await db_session.flush()
    await db_session.refresh(conv)

    msg = await chat_service.save_message(db_session, conv.id, "user", "Hello!")

    assert msg.role == "user"
    assert msg.content == "Hello!"
    assert msg.conversation_id == conv.id


@pytest.mark.asyncio
async def test_get_conversation_messages(db_session: AsyncSession) -> None:
    conv = Conversation(provider="openai", model="gpt-4o", title="Test")
    db_session.add(conv)
    await db_session.flush()

    await chat_service.save_message(db_session, conv.id, "user", "Hi")
    await chat_service.save_message(db_session, conv.id, "assistant", "Hello back!")

    messages = await chat_service.get_conversation_messages(db_session, conv.id)

    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[0].content == "Hi"
    assert messages[1].role == "assistant"


@pytest.mark.asyncio
async def test_stream_chat_response(
    db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    conv = Conversation(provider="openai", model="gpt-4o", title="Stream test")
    db_session.add(conv)
    await db_session.flush()
    await db_session.refresh(conv)

    async def mock_stream_chat(
        messages: list[ChatMessage], model: str
    ) -> AsyncGenerator[str, None]:
        yield "Hello"
        yield " World"

    mock_provider = MagicMock(spec=AIProvider)
    mock_provider.stream_chat = mock_stream_chat
    monkeypatch.setattr(chat_service, "get_provider", lambda name: mock_provider)

    request = ChatRequest(content="What is 2+2?", provider="openai", model="gpt-4o")
    tokens = [t async for t in chat_service.stream_chat_response(db_session, request, conv)]

    assert tokens == ["Hello", " World"]


@pytest.mark.asyncio
async def test_get_or_create_conversation_creates_new(db_session: AsyncSession) -> None:
    request = ChatRequest(
        content="Tell me a joke", provider="openai", model="gpt-4o"
    )
    conv = await chat_service.get_or_create_conversation(db_session, request)

    assert conv.provider == "openai"
    assert conv.model == "gpt-4o"
    assert conv.title == "Tell me a joke"


@pytest.mark.asyncio
async def test_get_or_create_conversation_fetches_existing(db_session: AsyncSession) -> None:
    existing = Conversation(provider="openai", model="gpt-4o", title="Existing")
    db_session.add(existing)
    await db_session.flush()
    await db_session.refresh(existing)

    request = ChatRequest(
        conversation_id=existing.id,
        content="Follow-up question",
        provider="openai",
        model="gpt-4o",
    )
    conv = await chat_service.get_or_create_conversation(db_session, request)

    assert conv.id == existing.id


@pytest.mark.asyncio
async def test_get_or_create_conversation_not_found_raises(db_session: AsyncSession) -> None:
    from app.core.exceptions import ConversationNotFoundError

    request = ChatRequest(
        conversation_id="00000000-0000-0000-0000-000000000000",
        content="Hello",
        provider="openai",
        model="gpt-4o",
    )
    with pytest.raises(ConversationNotFoundError):
        await chat_service.get_or_create_conversation(db_session, request)
