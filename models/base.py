from abc import ABC, abstractmethod


class BaseModel(ABC):

    def __init__(self, model_id: str):
        self.model_id = model_id

    @property
    def display_name(self) -> str:
        return self.model_id

    @abstractmethod
    def generate(
        self,
        instructions: str,
        input_text: str,
    ) -> str:
        pass

    @abstractmethod
    def generate_verdict(
        self,
        instructions: str,
        input_text: str,
    ) -> dict:
        pass