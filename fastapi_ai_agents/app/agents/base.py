from abc import ABC, abstractmethod
from app.models.schema import ChatRequest

class BaseAgent(ABC):
    @abstractmethod
    async def chat(self, request: ChatRequest) -> str:
        pass
