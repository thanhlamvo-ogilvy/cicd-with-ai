import asyncio
from collections.abc import AsyncGenerator
from concurrent.futures import ThreadPoolExecutor

from google import genai

from app.services.providers.base import AIProvider, ChatMessage

# Timeout in seconds for API calls
API_TIMEOUT = 60


class GoogleProvider(AIProvider):
    def __init__(self, api_key: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self._executor = ThreadPoolExecutor(max_workers=1)

    async def stream_chat(
        self, messages: list[ChatMessage], model: str
    ) -> AsyncGenerator[str, None]:
        contents = []
        for m in messages:
            role = "model" if m.role == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": m.content}]})

        # Run the synchronous call in a thread pool to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            self._executor,
            lambda: self.client.models.generate_content_stream(
                model=model,
                contents=contents,
            ),
        )

        # Stream the response chunks
        for chunk in response:
            if chunk.text:
                yield chunk.text
