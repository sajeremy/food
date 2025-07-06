import base64
from enum import StrEnum

from langchain_core.messages import HumanMessage


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
