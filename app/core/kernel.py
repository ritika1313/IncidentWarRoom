import os

from dotenv import load_dotenv
from semantic_kernel import Kernel
from pathlib import Path
from semantic_kernel.connectors.ai.google.google_ai import (
    GoogleAIChatCompletion
)

# Load environment variables from .env
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)


def create_kernel():

    # Read Gemini configuration.
    api_key = os.getenv("GOOGLE_AI_API_KEY")
    model_id = os.getenv(
        "GOOGLE_AI_GEMINI_MODEL_ID",
        "gemini-2.5-flash"
    )

    # Ensure API key is available.
    if not api_key:
        raise ValueError(
            "GOOGLE_AI_API_KEY is missing from .env"
        )

    # Create Semantic Kernel instance.
    kernel = Kernel()

    # Configure Gemini as the AI service.
    gemini_service = GoogleAIChatCompletion(
        gemini_model_id=model_id,
        api_key=api_key
    )

    # Register Gemini with Semantic Kernel.
    kernel.add_service(gemini_service)

    return kernel
