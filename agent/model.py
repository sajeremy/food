from enum import StrEnum

from langchain_google_genai import ChatGoogleGenerativeAI

from config import settings


class GeminiModels(StrEnum):
    """
    Enum for Google Gemini models.
    """

    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"


def create_gemini_model(
    model: GeminiModels = GeminiModels.GEMINI_2_0_FLASH, temperature: int = 0, google_api_key: str | None = None
) -> ChatGoogleGenerativeAI:
    """
    Create a Google Gemini model instance.

    Args:
        model (str): The model name to use.
        temperature (float): The temperature setting for the model.
        api_key (str): The API key for Google Gemini.

    Returns:
        ChatGoogleGenerativeAI: An instance of the Google Gemini model.
    """
    google_api_key = google_api_key or settings.google_api_key

    if not google_api_key:
        raise ValueError("Google API key must be provided.")
    return ChatGoogleGenerativeAI(model=model.value, temperature=temperature, google_api_key=google_api_key)
