import os

from openai import OpenAI

from models.base import BaseModel
from models.verdict import VERDICT_SCHEMA, parse_verdict


class OpenAIModel(BaseModel):

    def __init__(self, model_id: str):
        super().__init__(model_id)

        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )

    def generate(
        self,
        instructions: str,
        input_text: str,
    ) -> str:

        response = self.client.responses.create(
            model=self.model_id,
            instructions=instructions,
            input=input_text,
        )

        if not response.output_text:
            raise RuntimeError("OpenAI returned no text.")

        return response.output_text

    def generate_verdict(
        self,
        instructions: str,
        input_text: str,
    ) -> dict:

        response = self.client.responses.create(
            model=self.model_id,
            instructions=instructions,
            input=input_text,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "scam_assessment",
                    "strict": True,
                    "schema": VERDICT_SCHEMA,
                }
            },
        )

        if not response.output_text:
            raise RuntimeError("OpenAI returned no verdict.")

        return parse_verdict(response.output_text)