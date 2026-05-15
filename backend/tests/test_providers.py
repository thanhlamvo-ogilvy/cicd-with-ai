"""Tests for AI provider implementations (OpenAI, Anthropic, Google)."""

from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.providers.anthropic import AnthropicProvider
from app.services.providers.base import ChatMessage
from app.services.providers.google import GoogleProvider
from app.services.providers.openai import OpenAIProvider


# ── OpenAI ────────────────────────────────────────────────────────────────


class TestOpenAIProvider:
    def test_init_creates_client(self) -> None:
        with patch("app.services.providers.openai.AsyncOpenAI") as mock_cls:
            provider = OpenAIProvider(api_key="sk-test")
            mock_cls.assert_called_once()
            assert provider.client is mock_cls.return_value

    def test_init_passes_base_url(self) -> None:
        with patch("app.services.providers.openai.AsyncOpenAI") as mock_cls:
            OpenAIProvider(api_key="", base_url="http://localhost:11434/v1")
            assert mock_cls.call_args.kwargs["base_url"] == "http://localhost:11434/v1"

    @pytest.mark.asyncio
    async def test_stream_chat_yields_content(self) -> None:
        chunk = MagicMock()
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta.content = "Hello"

        async def mock_create(**kwargs: Any) -> AsyncGenerator[Any, None]:
            async def _stream() -> AsyncGenerator[Any, None]:
                yield chunk

            return _stream()  # type: ignore[return-value]

        with patch("app.services.providers.openai.AsyncOpenAI") as mock_cls:
            mock_client = MagicMock()
            mock_cls.return_value = mock_client
            mock_client.chat.completions.create = mock_create

            provider = OpenAIProvider(api_key="sk-test")
            tokens = [
                t
                async for t in provider.stream_chat(
                    [ChatMessage(role="user", content="Hi")], "gpt-4o"
                )
            ]
        assert tokens == ["Hello"]

    @pytest.mark.asyncio
    async def test_stream_chat_skips_empty_delta(self) -> None:
        chunk_empty = MagicMock()
        chunk_empty.choices = [MagicMock()]
        chunk_empty.choices[0].delta.content = None

        chunk_text = MagicMock()
        chunk_text.choices = [MagicMock()]
        chunk_text.choices[0].delta.content = "World"

        async def mock_create(**kwargs: Any) -> AsyncGenerator[Any, None]:
            async def _stream() -> AsyncGenerator[Any, None]:
                yield chunk_empty
                yield chunk_text

            return _stream()  # type: ignore[return-value]

        with patch("app.services.providers.openai.AsyncOpenAI") as mock_cls:
            mock_client = MagicMock()
            mock_cls.return_value = mock_client
            mock_client.chat.completions.create = mock_create

            provider = OpenAIProvider(api_key="sk-test")
            tokens = [
                t
                async for t in provider.stream_chat(
                    [ChatMessage(role="user", content="Hi")], "gpt-4o"
                )
            ]
        assert tokens == ["World"]

    @pytest.mark.asyncio
    async def test_stream_chat_skips_empty_choices(self) -> None:
        chunk_no_choices = MagicMock()
        chunk_no_choices.choices = []

        async def mock_create(**kwargs: Any) -> AsyncGenerator[Any, None]:
            async def _stream() -> AsyncGenerator[Any, None]:
                yield chunk_no_choices

            return _stream()  # type: ignore[return-value]

        with patch("app.services.providers.openai.AsyncOpenAI") as mock_cls:
            mock_client = MagicMock()
            mock_cls.return_value = mock_client
            mock_client.chat.completions.create = mock_create

            provider = OpenAIProvider(api_key="sk-test")
            tokens = [
                t
                async for t in provider.stream_chat(
                    [ChatMessage(role="user", content="Hi")], "gpt-4o"
                )
            ]
        assert tokens == []


# ── Anthropic ─────────────────────────────────────────────────────────────


class TestAnthropicProvider:
    def test_init_creates_client(self) -> None:
        with patch("app.services.providers.anthropic.AsyncAnthropic") as mock_cls:
            provider = AnthropicProvider(api_key="ant-test")
            mock_cls.assert_called_once_with(api_key="ant-test", timeout=60)
            assert provider.client is mock_cls.return_value

    @pytest.mark.asyncio
    async def test_stream_chat_yields_tokens(self) -> None:
        async def mock_text_stream() -> AsyncGenerator[str, None]:
            yield "Hello"
            yield " World"

        mock_stream = MagicMock()
        mock_stream.text_stream = mock_text_stream()
        mock_cm = AsyncMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_stream)
        mock_cm.__aexit__ = AsyncMock(return_value=None)

        with patch("app.services.providers.anthropic.AsyncAnthropic") as mock_cls:
            mock_client = MagicMock()
            mock_cls.return_value = mock_client
            mock_client.messages.stream.return_value = mock_cm

            provider = AnthropicProvider(api_key="ant-test")
            tokens = [
                t
                async for t in provider.stream_chat(
                    [ChatMessage(role="user", content="Hello")], "claude-3-opus-20240229"
                )
            ]
        assert tokens == ["Hello", " World"]

    @pytest.mark.asyncio
    async def test_stream_chat_extracts_system_message(self) -> None:
        async def mock_text_stream() -> AsyncGenerator[str, None]:
            yield "Response"

        mock_stream = MagicMock()
        mock_stream.text_stream = mock_text_stream()
        mock_cm = AsyncMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_stream)
        mock_cm.__aexit__ = AsyncMock(return_value=None)

        with patch("app.services.providers.anthropic.AsyncAnthropic") as mock_cls:
            mock_client = MagicMock()
            mock_cls.return_value = mock_client
            mock_client.messages.stream.return_value = mock_cm

            provider = AnthropicProvider(api_key="ant-test")
            messages = [
                ChatMessage(role="system", content="You are a helpful assistant."),
                ChatMessage(role="user", content="Hello"),
            ]
            tokens = [t async for t in provider.stream_chat(messages, "claude-3-opus")]

        call_kwargs = mock_client.messages.stream.call_args.kwargs
        assert call_kwargs["system"] == "You are a helpful assistant."
        assert all(m["role"] != "system" for m in call_kwargs["messages"])
        assert tokens == ["Response"]


# ── Google ────────────────────────────────────────────────────────────────


class TestGoogleProvider:
    def test_init_creates_client(self) -> None:
        with patch("app.services.providers.google.genai") as mock_genai:
            provider = GoogleProvider(api_key="google-test")
            mock_genai.Client.assert_called_once_with(api_key="google-test")
            assert provider.client is mock_genai.Client.return_value

    @pytest.mark.asyncio
    async def test_stream_chat_yields_text(self) -> None:
        mock_chunk = MagicMock()
        mock_chunk.text = "Hello"

        async def mock_run_in_executor(executor: Any, func: Any) -> Any:
            return func()

        with (
            patch("app.services.providers.google.genai") as mock_genai,
            patch("app.services.providers.google.asyncio.get_event_loop") as mock_get_loop,
        ):
            mock_client = MagicMock()
            mock_genai.Client.return_value = mock_client
            mock_client.models.generate_content_stream.return_value = [mock_chunk]

            mock_loop = MagicMock()
            mock_get_loop.return_value = mock_loop
            mock_loop.run_in_executor = mock_run_in_executor

            provider = GoogleProvider(api_key="google-test")
            tokens = [
                t
                async for t in provider.stream_chat(
                    [ChatMessage(role="user", content="Hi")], "gemini-pro"
                )
            ]
        assert tokens == ["Hello"]

    @pytest.mark.asyncio
    async def test_stream_chat_skips_empty_text(self) -> None:
        chunk_empty = MagicMock()
        chunk_empty.text = None
        chunk_text = MagicMock()
        chunk_text.text = "World"

        async def mock_run_in_executor(executor: Any, func: Any) -> Any:
            return func()

        with (
            patch("app.services.providers.google.genai") as mock_genai,
            patch("app.services.providers.google.asyncio.get_event_loop") as mock_get_loop,
        ):
            mock_client = MagicMock()
            mock_genai.Client.return_value = mock_client
            mock_client.models.generate_content_stream.return_value = [chunk_empty, chunk_text]

            mock_loop = MagicMock()
            mock_get_loop.return_value = mock_loop
            mock_loop.run_in_executor = mock_run_in_executor

            provider = GoogleProvider(api_key="google-test")
            tokens = [
                t
                async for t in provider.stream_chat(
                    [ChatMessage(role="user", content="Hi")], "gemini-pro"
                )
            ]
        assert tokens == ["World"]

    @pytest.mark.asyncio
    async def test_stream_chat_maps_assistant_role(self) -> None:
        mock_chunk = MagicMock()
        mock_chunk.text = "Hi"

        async def mock_run_in_executor(executor: Any, func: Any) -> Any:
            return func()

        with (
            patch("app.services.providers.google.genai") as mock_genai,
            patch("app.services.providers.google.asyncio.get_event_loop") as mock_get_loop,
        ):
            mock_client = MagicMock()
            mock_genai.Client.return_value = mock_client
            mock_client.models.generate_content_stream.return_value = [mock_chunk]

            mock_loop = MagicMock()
            mock_get_loop.return_value = mock_loop
            mock_loop.run_in_executor = mock_run_in_executor

            provider = GoogleProvider(api_key="google-test")
            messages = [
                ChatMessage(role="user", content="Hello"),
                ChatMessage(role="assistant", content="Hi there"),
            ]
            tokens = [t async for t in provider.stream_chat(messages, "gemini-pro")]

        # Verify assistant role mapped to "model" for Google API
        call_args = mock_client.models.generate_content_stream.call_args
        contents = call_args.kwargs["contents"]
        assert contents[1].role == "model"
        assert tokens == ["Hi"]
