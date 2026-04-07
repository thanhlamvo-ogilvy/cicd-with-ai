from collections.abc import AsyncGenerator

from openai import AsyncOpenAI

from app.services.providers.base import AIProvider, ChatMessage


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, base_url: str | None = None) -> None:
        kwargs: dict[str, str] = {"api_key": api_key or "lm-studio"}
        if base_url:
            kwargs["base_url"] = base_url
        self.client = AsyncOpenAI(**kwargs)

    async def stream_chat(
        self, messages: list[ChatMessage], model: str
    ) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
