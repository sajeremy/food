import hashlib
from datetime import datetime
from enum import StrEnum

from sqlalchemy import String
from sqlmodel import Column, Field, Relationship, SQLModel


class UnitType(StrEnum):
    LB = "lb"
    EACH = "ea"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, description="Unique identifier for the user")
    username: str = Field(description="Username of the user")

    receipts: list["GroceryReceipt"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "select"})


class Store(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, description="Unique identifier for the store")
    name: str | None = Field(default=None, description="Name of the store")
    address: str | None = Field(default=None, description="Address of the store")
    phone: str | None = Field(default=None, description="Phone number of the store")

    receipts: list["GroceryReceipt"] = Relationship(back_populates="store", sa_relationship_kwargs={"lazy": "select"})


class Purchase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, description="Unique identifier for the purchase")
    receipt_id: int | None = Field(
        default=None, foreign_key="groceryreceipt.id", description="ID of the associated grocery receipt"
    )
    name: str = Field(description="Name of the purchased item")
    quantity: float = Field(description="Quantity of the purchased item")
    unit_price: float = Field(description="Unit price of the purchased item")
    unit_type: UnitType = Field(description="Unit type of the purchased item, e.g., lb, ea")

    receipt: "GroceryReceipt" = Relationship(back_populates="purchases", sa_relationship_kwargs={"lazy": "select"})


class GroceryReceiptBase(SQLModel):
    date_time: datetime | None = Field(default=None, description="Date and time of the purchase as datetime object")


class GroceryReceiptSchema(GroceryReceiptBase):
    is_valid: bool = Field(description="Indicates if a valid grocery receipt")
    user: User = Field(default=None, description="User who made the purchase")
    store: Store | None = Field(default=None, description="Store where the purchase was made")
    purchases: list[Purchase] | None = Field(default=None, description="List of purchased items")


class GroceryReceipt(GroceryReceiptBase, table=True):
    # Attributes
    id: int = Field(primary_key=True, description="Unique identifier for the grocery receipt")
    user_id: int = Field(foreign_key="user.id", description="ID of the user who made the purchase")
    store_id: int | None = Field(
        default=None, foreign_key="store.id", description="ID of the store where the purchase was made"
    )
    image_hash: str | None = Field(
        default=None,
        sa_column=Column(String(64), unique=True, index=True),
        description="Unique hash of the receipt image for deduplication",
    )

    # Relationships
    user: User = Relationship(back_populates="receipts", sa_relationship_kwargs={"lazy": "select"})
    store: Store | None = Relationship(back_populates="receipts", sa_relationship_kwargs={"lazy": "select"})
    purchases: list["Purchase"] = Relationship(back_populates="receipt", sa_relationship_kwargs={"lazy": "select"})

    @staticmethod
    def generate_image_hash(image_content: bytes) -> str:
        """Generate a SHA-256 hash for the given image content."""
        return hashlib.sha256(image_content).hexdigest()

    @classmethod
    def from_image_and_data(
        cls, image_content: bytes, user_id: int, store_id: int | None, date_time: datetime | None
    ) -> "GroceryReceipt":
        receipt_data = {
            "image_hash": cls.generate_image_hash(image_content),
            "user_id": user_id,
            "store_id": store_id,
            "date_time": date_time,
        }

        receipt = cls(**receipt_data)
        return receipt
