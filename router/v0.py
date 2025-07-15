from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from agent.utils import ImageType, parse_grocery_receipt
from config import settings
from orm.data_models import GroceryReceiptSchema, UserBase
from orm.utils import is_receipt_in_db

router = APIRouter(prefix="/v0", tags=["v0"])


@router.get("/status")
def get_status():
    return {"status": "ok"}


@router.post("/grocery_receipt")
async def parse_grocery_receipt_image(
    user: Annotated[str, Form()], img_file: Annotated[UploadFile, File()]
) -> GroceryReceiptSchema:
    """
    Parse a grocery receipt image and return the structured data.

    Args:
        user (str): The username of the user parsing the receipt.
        img_file (UploadFile): The uploaded image file of the grocery receipt.

    Returns:
        GroceryReceiptSchema: The parsed receipt data.
    """

    file_extension = Path(img_file.filename).suffix
    img_type = ImageType.from_extension(extension=file_extension)
    img_content = await img_file.read()

    # todo: handle separate cases for invalid image, file type, already existing receipt, server error
    if is_receipt_in_db(img_content=img_content, db_url=settings.database_url):
        return GroceryReceiptSchema(is_valid=False, user=UserBase(username=user), purchases=[])

    return parse_grocery_receipt(user=user, img_content=img_content, img_type=img_type)
