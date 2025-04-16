from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def generate_content(self, model: str, prompt: str) -> str:
        pass