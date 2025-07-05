from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from pathlib import Path
from utils import create_gemini_img_txt_message, ImageType

def main():

    # Get environment variables and constants
    load_dotenv(".env.local")
    api_key = os.getenv("GEMINI_API_KEY")
    img_path = Path("resources/receipt_1.HEIC")

    # Initialize the Google Gemini model
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        google_api_key=api_key
    )

    # Read image file
    img_type = ImageType.from_extension(img_path.suffix) 
    with img_path.open("rb") as img_file:
        img_content = img_file.read()
    
    # Create message for Model
    query = "What is in this receipt?"
    system_prompt = "You are a helpful assistant that parses images of receipts and extracts the information into a json structure."
    human_message = create_gemini_img_txt_message(query=query, img_content=img_content, img_type=img_type)
    messages = [("system", system_prompt), human_message]
    
    # Call model
    response = model.invoke(messages)
    print(response)

if __name__ == "__main__":
    main()
