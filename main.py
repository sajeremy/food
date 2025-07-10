import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from model.groceries import GroceryReceiptSchema
from utils import ImageType, create_gemini_img_message


def main():
    # Get environment variables and constants
    load_dotenv(".env.local")
    api_key = os.getenv("GEMINI_API_KEY")
    food_username = os.getenv("FOOD_USERNAME")
    img_path = Path("/Users/jeremysantiago/Desktop/Projects/food/resources/receipt_1.HEIC")

    # Initialize the Google Gemini model
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=api_key)
    grocery_parsing_model = model.with_structured_output(
        schema=GroceryReceiptSchema,
    )

    # Read image file
    img_type = ImageType.from_extension(img_path.suffix)
    with img_path.open("rb") as img_file:
        img_content = img_file.read()

    # Create message for Model
    system_prompt = (
        "You are a helpful assistant that parses images of receipts and extracts the information."
        "Format all dates in ISO format (YYYY-MM-DD HH:MM:SS)."
        f"Populate the user field with the value '{food_username}'."
        "If uploaded image is not a valid grocery receipt or cannot be parsed, mark is_valid as false"
        "and return None for all other fields."
    )
    human_message = create_gemini_img_message(img_content=img_content, img_type=img_type)
    messages = [("system", system_prompt), human_message]

    # Call model
    response = grocery_parsing_model.invoke(messages)
    print(response)
    print(type(response))


if __name__ == "__main__":
    main()
