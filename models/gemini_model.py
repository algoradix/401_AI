import os

from google import genai
from google.genai import types

from models.base import BaseModel
from models.verdict import VERDICT_SCHEMA, parse_verdict


class GeminiModel(BaseModel):

    def __init__(self, model_id: str):
        super().__init__(model_id)

        self.client = genai.Client(
            api_key=os.environ["GEMINI_API_KEY"]
        )

    def generate(
        self,
        instructions: str,
        input_text: str,
    ) -> str:

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=input_text,
            config=types.GenerateContentConfig(
                system_instruction=instructions,
            ),
        )

        if not response.text:
            raise RuntimeError("Gemini returned no text.")

        return response.text

    def generate_verdict(
        self,
        instructions: str,
        input_text: str,
    ) -> dict:

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=input_text,
            config=types.GenerateContentConfig(
                system_instruction=instructions,
                response_mime_type="application/json",
                response_json_schema=VERDICT_SCHEMA,
            ),
        )

        if not response.text:
            raise RuntimeError("Gemini returned no verdict.")

        return parse_verdict(response.text)