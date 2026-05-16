from collections.abc import AsyncGenerator
from typing import cast

from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletionChunk, ChatCompletionMessageParam

from app.services.providers.base import AIProvider, ChatMessage

# Timeout in seconds for API calls
API_TIMEOUT = 60


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, base_url: str | None = None) -> None:
        self.client = AsyncOpenAI(
            api_key=api_key or "lm-studio",
            base_url=base_url,
            timeout=API_TIMEOUT,
        )

    async def stream_chat(
        self, messages: list[ChatMessage], model: str
    ) -> AsyncGenerator[str, None]:
        typed_messages = cast(
            list[ChatCompletionMessageParam],
            [{"role": m.role, "content": m.content} for m in messages],
        )
        stream: AsyncStream[ChatCompletionChunk] = await self.client.chat.completions.create(
            model=model,
            messages=typed_messages,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
