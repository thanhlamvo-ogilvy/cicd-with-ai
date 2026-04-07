from collections.abc import AsyncGenerator

from google import genai

from app.services.providers.base import AIProvider, ChatMessage


class GoogleProvider(AIProvider):
    def __init__(self, api_key: str) -> None:
        self.client = genai.Client(api_key=api_key)

    async def stream_chat(
        self, messages: list[ChatMessage], model: str
    ) -> AsyncGenerator[str, None]:
        contents = []
        for m in messages:
            role = "model" if m.role == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": m.content}]})

        response = self.client.models.generate_content_stream(
            model=model,
            contents=contents,
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
