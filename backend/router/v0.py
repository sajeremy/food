from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from agent.utils import ImageType, parse_grocery_receipt
from config import settings
from orm.data_models import GroceryReceiptSchema
from orm.utils import is_receipt_in_db

router = APIRouter(prefix="/v0", tags=["v0"])


@router.get("/status")
def get_status():
    return {"status": "ok"}


@router.post("/grocery_receipt")
async def parse_grocery_receipt_image(
    # img_file: Annotated[UploadFile, File()], current_user: User = Depends(get_current_user)
    img_file: Annotated[UploadFile, File()],
    current_user: str = "mock_user",  # Mocked for example purposes
) -> GroceryReceiptSchema:
    """
    Parse a grocery receipt image and return the structured data.

    Args:
        img_file (UploadFile): The uploaded image file of the grocery receipt.
        current_user (User): The authenticated user parsing the receipt.

    Returns:
        GroceryReceiptSchema: The parsed receipt data.
    """

    file_extension = Path(img_file.filename).suffix
    img_type = ImageType.from_extension(extension=file_extension)
    img_content = await img_file.read()

    # todo: handle separate cases for invalid image, file type, already existing receipt, server error
    if is_receipt_in_db(img_content=img_content, db_url=settings.database_url):
        raise HTTPException(
            status_code=409,
            detail="Receipt already exists in the database.",
        )

    return parse_grocery_receipt(user=current_user, img_content=img_content, img_type=img_type)
