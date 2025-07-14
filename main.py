import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from orm.data_models import GroceryCategory, GroceryReceiptSchema
from orm.utils import add_grocery_receipt_to_db, is_receipt_in_db
from utils import ImageType, create_gemini_img_message


def print_receipt_info(gr_schema: GroceryReceiptSchema):
    """Prints the parsed receipt information."""
    print("\n==== PARSED RECEIPT INFORMATION ====")
    print(f"Valid Receipt: {gr_schema.is_valid}")
    print(f"Date/Time: {gr_schema.date_time}")
    print(f"User: {gr_schema.user}")

    if gr_schema.store:
        print("\nStore Information:")
        print(f"  Name: {gr_schema.store.name}")
        print(f"  Address: {gr_schema.store.address}")
        print(f"  Phone: {gr_schema.store.phone}")
    else:
        print("\nStore: Not available")

    if gr_schema.purchases:
        print("\nPurchases:")
        total = 0.0
        for i, purchase in enumerate(gr_schema.purchases, 1):
            item_total = purchase.quantity * purchase.unit_price
            total += item_total
            print(
                f"  {i}. {purchase.name}: {purchase.quantity} {purchase.unit_type} x ${purchase.unit_price:.2f} "
                f"= ${item_total:.2f} \n      Category: {purchase.category}\n       Brand: {purchase.brand}"
            )
        print(f"\nTotal: ${total:.2f}")
    else:
        print("\nPurchases: None found")


def get_user_confirmation() -> bool:
    user_input = input("\nIs this parsing correct? (y/n): ")
    if user_input.lower() in ["y", "yes"]:
        print("Proceeding with saving the receipt...")
        return True
    else:
        print("Operation cancelled.")
        return False


def main():
    # Get environment variables and constants
    load_dotenv(".env.local")
    api_key = os.getenv("GEMINI_API_KEY")
    food_username = os.getenv("FOOD_USERNAME")
    db_url = os.getenv("DB_URL")
    img_path = Path("/Users/jeremysantiago/Desktop/Projects/food/resources/receipt_1.HEIC")

    # Read image file
    img_type = ImageType.from_extension(img_path.suffix)
    with img_path.open("rb") as img_file:
        img_content = img_file.read()

    if is_receipt_in_db(img_content=img_content, db_url=db_url):
        print("Receipt already exists in the database. Will not parse.")
        return

    # Initialize the Google Gemini model
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=api_key)
    gr_parsing_model = model.with_structured_output(
        schema=GroceryReceiptSchema,
    )

    # Create message for Model
    system_prompt = (
        "You are a helpful assistant that parses images of receipts and extracts the information."
        "Format all dates in ISO format (YYYY-MM-DD HH:MM:SS)."
        f"Populate the user.username field with the value '{food_username}'."
        f"Populate Purchase.category with one of the following values: {', '.join(GroceryCategory.__members__.keys())}."
        f"Populate Purchase.brand with the brand name if available, otherwise leave it as None."
        "If uploaded image is not a valid grocery receipt or cannot be parsed, mark is_valid as false"
        "and return None for all other fields."
    )
    human_message = create_gemini_img_message(img_content=img_content, img_type=img_type)
    messages = [("system", system_prompt), human_message]

    # Call model
    gr_schema = gr_parsing_model.invoke(messages)

    print_receipt_info(gr_schema)
    if get_user_confirmation():
        add_grocery_receipt_to_db(img_content=img_content, parsed_data=gr_schema, db_url=db_url)
        print("Receipt saved successfully.")


if __name__ == "__main__":
    main()
