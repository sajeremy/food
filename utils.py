import base64
from langchain_core.messages import HumanMessage
from enum import StrEnum

class ImageType(StrEnum):
    JPEG = "jpeg"
    PNG = "png"
    HEIC = "heic"

    @classmethod
    def from_extension(cls, extension: str) -> 'ImageType':
        """
        Get the ImageType from a file extension.

        Args:
            extension (str): The file extension (e.g., '.jpeg', '.png', '.heic').

        Returns:
            ImageType: The corresponding ImageType.
        """
        
        try:
            return cls(extension.lstrip('.').lower())
        except ValueError:
            raise ValueError(f"Unsupported image type: {extension}.")

def b64_encode(data: bytes) -> str:
    """Base64 encode the given bytes."""
    return base64.b64encode(data).decode('utf-8')

def create_gemini_img_txt_message(query: str, img_content: bytes, img_type: ImageType) -> HumanMessage:
    """
    Format a query for Google Gemini with an image and text.

    Args:
        query (str): The text query.
        img_content (bytes): The image content in bytes.

    Returns:
        HumanMessage: A formatted message for Google Gemini.
    """
    return HumanMessage(
        content=[
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
                "image_url": f"data:image/{img_type.value};base64,{b64_encode(img_content)}"
            }
        ]
    )