import os

from groq import Groq

from models.base import BaseModel
from models.verdict import VERDICT_SCHEMA, parse_verdict


class GroqModel(BaseModel):

    def __init__(self, model_id: str):
        super().__init__(model_id)

        self.client = Groq(
            api_key=os.environ["GROQ_API_KEY"]
        )

    def generate(
        self,
        instructions: str,
        input_text: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": instructions,
                },
                {
                    "role": "user",
                    "content": input_text,
                },
            ],
        )

        output = response.choices[0].message.content

        if not output:
            raise RuntimeError("Groq returned no text.")

        return output

    def generate_verdict(
        self,
        instructions: str,
        input_text: str,
    ) -> dict:

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": instructions,
                },
                {
                    "role": "user",
                    "content": input_text,
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "scam_assessment",
                    "strict": True,
                    "schema": VERDICT_SCHEMA,
                },
            },
        )

        output = response.choices[0].message.content

        if not output:
            raise RuntimeError("Groq returned no verdict.")

        return parse_verdict(output)