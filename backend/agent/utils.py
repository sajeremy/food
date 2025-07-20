import base64
from enum import StrEnum

from langchain_core.messages import HumanMessage, SystemMessage

from agent.model import create_gemini_model
from orm.data_models import GroceryCategory, GroceryReceiptSchema


class ImageType(StrEnum):
    JPEG = "jpeg"
    JPG = "jpg"
    PNG = "png"
    HEIC = "heic"

    @classmethod
    def from_extension(cls, extension: str) -> "ImageType":
        """
        Get the ImageType from a file extension.

        Args:
            extension (str): The file extension (e.g., '.jpeg', '.png', '.heic').

        Returns:
            ImageType: The corresponding ImageType.
        """

        try:
            return cls(extension.lstrip(".").lower())
        except ValueError as err:
            raise ValueError(f"Unsupported image type: {extension}.") from err


def b64_encode(data: bytes) -> str:
    """Base64 encode the given bytes."""
    return base64.b64encode(data).decode("utf-8")


def create_gemini_img_message(img_content: bytes, img_type: ImageType) -> HumanMessage:
    """
    Create message with image to Gemini API.

    Args:
        img_content (bytes): The image content in bytes.
        img_type (ImageType): The type of the image.

    Returns:
        HumanMessage: A formatted message for Google Gemini.
    """
    return HumanMessage(
        content=[
            {"type": "image_url", "image_url": f"data:image/{img_type.value};base64,{b64_encode(img_content)}"},
        ]
    )


def create_grocery_parsing_system_prompt(user: str) -> str:
    """Create the system prompt with the specified username."""
    return SystemMessage(
        content=[
            "You are a helpful assistant that parses images of receipts and extracts the information.",
            "Format all dates in ISO format (YYYY-MM-DD HH:MM:SS).",
            f"Populate the user.username field with the value '{user}'.",
            f"Populate Purchase.category with one of the following values: {', '.join(GroceryCategory.__members__.keys())}.",
            "Populate Purchase.brand with the brand name if available, otherwise leave it as None.",
            "If uploaded image is not a valid grocery receipt or cannot be parsed, mark is_valid as false",
            "and return None for all other fields.",
        ]
    )


def parse_grocery_receipt(user: str, img_content: bytes, img_type: ImageType) -> GroceryReceiptSchema:
    """
    Get a LLM model configured for grocery receipt parsing.

    Returns:
        ChatGoogleGenerativeAI: A model instance configured for grocery receipt parsing.
    """

    base_model = create_gemini_model()
    messages = [
        create_grocery_parsing_system_prompt(user=user),
        create_gemini_img_message(img_content=img_content, img_type=img_type),
    ]
    gr_parser = base_model.with_structured_output(schema=GroceryReceiptSchema)
    return gr_parser.invoke(messages)
