import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from models.gpt_model import OpenAIModel
from models.claude_model import ClaudeModel
from models.gemini_model import GeminiModel
from models.groq_model import GroqModel

from services.orchestration import run_all_models


load_dotenv()

app = Flask(__name__)


MODEL_PROVIDERS = {
    "OPENAI_MODELS": (OpenAIModel, "OPENAI_API_KEY"),
    "ANTHROPIC_MODELS": (ClaudeModel, "ANTHROPIC_API_KEY"),
    "GEMINI_MODELS": (GeminiModel, "GEMINI_API_KEY"),
    "GROQ_MODELS": (GroqModel, "GROQ_API_KEY"),
}


def load_models():
    models = []

    for env_variable, (model_class, api_key_name) in MODEL_PROVIDERS.items():

        model_ids = [
            model_id.strip()
            for model_id in os.getenv(env_variable, "").split(",")
            if model_id.strip()
        ]

        if model_ids and not os.getenv(api_key_name):
            raise RuntimeError(
                f"{api_key_name} is required for {env_variable}"
            )

        for model_id in model_ids:
            models.append(model_class(model_id))

    if not models:
        raise RuntimeError("No models configured.")

    return models


MODELS = load_models()


@app.route("/")
def index():
    return render_template(
        "index.html",
        models=[model.display_name for model in MODELS],
    )


@app.route("/analyze", methods=["POST"])
def analyze():

    print("Hello...")

    data = request.get_json(silent=True) or {}

    conversation = data.get("text", "")

    print(conversation)

    if not isinstance(conversation, str):
        return jsonify({"error": "Text must be a string."}), 400

    conversation = conversation.strip()

    if not conversation:
        return jsonify({
            "error": "Please enter an SMS conversation."
        }), 400

    if len(conversation) > 12000:
        return jsonify({
            "error": "Conversation is too long."
        }), 400

    results = run_all_models(MODELS, conversation)



    return jsonify({
        "results": results,
    })




if __name__ == "__main__":
    app.run(debug=True)