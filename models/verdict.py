import json

from jsonschema import validate


VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["YES", "NO"],
        },
        "risk_level": {
            "type": "string",
            "enum": ["LOW", "MEDIUM", "HIGH"],
        },
        "confidence": {
            "type": "string",
            "enum": ["LOW", "MEDIUM", "HIGH"],
        },
        "explanation": {
            "type": "string",
        },
        "warning_signs": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
    },
    "required": [
        "verdict",
        "risk_level",
        "confidence",
        "explanation",
        "warning_signs",
    ],
    "additionalProperties": False,
}


def parse_verdict(response_text: str) -> dict:
    result = json.loads(response_text)

    validate(
        instance=result,
        schema=VERDICT_SCHEMA,
    )

    return result