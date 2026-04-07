from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from dataclasses import dataclass


@dataclass
class ChatMessage:
    role: str
    content: str


class AIProvider(ABC):
    @abstractmethod
    async def stream_chat(
        self, messages: list[ChatMessage], model: str
    ) -> AsyncGenerator[str, None]:
        """Yield response tokens as they arrive from the AI provider."""
        yield ""  # pragma: no cover
