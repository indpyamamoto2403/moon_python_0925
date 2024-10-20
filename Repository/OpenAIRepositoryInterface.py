from abc import ABC, abstractmethod
from typing import List, Dict, Any

class OpenAIRepositoryInterface(ABC):
    @abstractmethod
    def fetch_answer(self, prompt:str) -> str:
        pass
