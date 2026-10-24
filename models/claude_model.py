import os

from anthropic import Anthropic

from models.base import BaseModel
from models.verdict import VERDICT_SCHEMA, parse_verdict


class ClaudeModel(BaseModel):

    def __init__(self, model_id: str):
        super().__init__(model_id)

        self.client = Anthropic(
            api_key=os.environ["ANTHROPIC_API_KEY"]
        )

    def generate(
        self,
        instructions: str,
        input_text: str,
    ) -> str:

        response = self.client.messages.create(
            model=self.model_id,
            max_tokens=2048,
            system=instructions,
            messages=[
                {
                    "role": "user",
                    "content": input_text,
                }
            ],
        )

        output = "".join(
            block.text
            for block in response.content
            if block.type == "text"
        )

        if response.stop_reason == "max_tokens":
            raise RuntimeError("Claude response was truncated.")

        if not output:
            raise RuntimeError("Claude returned no text.")

        return output

    def generate_verdict(
        self,
        instructions: str,
        input_text: str,
    ) -> dict:

        response = self.client.messages.create(
            model=self.model_id,
            max_tokens=2048,
            system=instructions,
            messages=[
                {
                    "role": "user",
                    "content": input_text,
                }
            ],
            output_config={
                "format": {
                    "type": "json_schema",
                    "schema": VERDICT_SCHEMA,
                }
            },
        )

        if response.stop_reason == "max_tokens":
            raise RuntimeError("Claude verdict was truncated.")

        output = "".join(
            block.text
            for block in response.content
            if block.type == "text"
        )

        if not output:
            raise RuntimeError("Claude returned no verdict.")

        return parse_verdict(output)