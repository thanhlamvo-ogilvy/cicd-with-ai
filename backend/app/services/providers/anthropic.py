from collections.abc import AsyncGenerator

from anthropic import AsyncAnthropic

from app.services.providers.base import AIProvider, ChatMessage

# Timeout in seconds for API calls
API_TIMEOUT = 60


class AnthropicProvider(AIProvider):
    def __init__(self, api_key: str) -> None:
        self.client = AsyncAnthropic(api_key=api_key, timeout=API_TIMEOUT)

    async def stream_chat(
        self, messages: list[ChatMessage], model: str
    ) -> AsyncGenerator[str, None]:
        # Anthropic requires separating the system message
        system_content = ""
        chat_messages = []
        for m in messages:
            if m.role == "system":
                system_content = m.content
            else:
                chat_messages.append({"role": m.role, "content": m.content})

        async with self.client.messages.stream(
            model=model,
            messages=chat_messages,
            system=system_content or "You are a helpful assistant.",
            max_tokens=4096,
        ) as stream:
            async for text in stream.text_stream:
                yield text
