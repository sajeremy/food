import hashlib
from datetime import datetime
from enum import StrEnum

from sqlalchemy import String, UniqueConstraint
from sqlmodel import Column, Field, Relationship, SQLModel


class UnitType(StrEnum):
    OZ = "oz"
    LB = "lb"
    EACH = "ea"


class GroceryCategory(StrEnum):
    PRODUCE = "produce"
    DAIRY = "dairy"
    MEAT = "meat"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SNACKS = "snacks"
    FROZEN = "frozen"
    CANNED = "canned"
    GRAINS = "grains"
    CONDIMENTS = "condiments"
    HOUSEHOLD = "household"
    PERSONAL_CARE = "personal_care"
    OTHER = "other"


class UserBase(SQLModel):
    username: str = Field(description="Username of the user, used for identification in the system")


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True, description="Unique identifier for the user")

    receipts: list["GroceryReceipt"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "select"})


class StoreBase(SQLModel):
    name: str = Field(default="unknown", description="Name of the store or 'unknown' if information not parsable")
    address: str | None = Field(default=None, description="Address of the store")
    phone: str | None = Field(default=None, description="Phone number of the store")


class Store(StoreBase, table=True):
    __tablename__ = "stores"

    id: int = Field(primary_key=True, description="Unique identifier for the store")

    receipts: list["GroceryReceipt"] = Relationship(back_populates="store", sa_relationship_kwargs={"lazy": "select"})
    items: list["Item"] = Relationship(back_populates="store", sa_relationship_kwargs={"lazy": "select"})


class TransactionBase(SQLModel):
    quantity: float = Field(description="Quantity of the purchased item")
    unit_price: float = Field(description="Unit price of the purchased item")
    unit_type: UnitType = Field(description="Unit type of the purchased item, e.g., lb, ea")


class Transaction(TransactionBase, table=True):
    __tablename__ = "transactions"

    id: int = Field(primary_key=True, description="Unique identifier for transaction")
    receipt_id: int | None = Field(
        default=None, foreign_key="grocery_receipts.id", description="ID of the associated grocery receipt"
    )
    item_id: int = Field(foreign_key="items.id", description="ID of the purchased item, referencing the Item table")

    receipt: "GroceryReceipt" = Relationship(back_populates="transactions", sa_relationship_kwargs={"lazy": "select"})


class ItemSchema(SQLModel):
    name: str = Field(description="Name of the item")
    category: GroceryCategory = Field(
        default=GroceryCategory.OTHER, description="Category of the item, e.g., produce, dairy, etc."
    )
    brand: str | None = Field(default=None, description="Brand of the item and may be None if not clear")


class Item(ItemSchema, table=True):
    __tablename__ = "items"

    id: int = Field(primary_key=True, description="Unique identifier for the item")
    store_id: int = Field(foreign_key="stores.id", description="ID of the store where the item is sold")

    store: Store | None = Relationship(back_populates="items", sa_relationship_kwargs={"lazy": "select"})
    transactions: list[Transaction] = Relationship(back_populates="item", sa_relationship_kwargs={"lazy": "select"})

    class Config:
        sa_table_args = (UniqueConstraint("store_id", "name", name="uix_item_store"),)


class Purchase(TransactionBase, ItemSchema):
    """Represents a purchase transaction for a specific item."""

    pass


class GroceryReceiptBase(SQLModel):
    date_time: datetime | None = Field(default=None, description="Date and time of the purchase as datetime object")


class GroceryReceiptSchema(GroceryReceiptBase):
    is_valid: bool = Field(description="Indicates if a valid grocery receipt")
    user: UserBase = Field(description="User who made the purchase")
    store: StoreBase = Field(default=StoreBase(), description="Store where the purchase was made")
    purchases: list[Purchase] = Field(description="List of purchased items")


class GroceryReceipt(GroceryReceiptBase, table=True):
    __tablename__ = "grocery_receipts"

    id: int = Field(primary_key=True, description="Unique identifier for the grocery receipt")
    user_id: int = Field(foreign_key="users.id", description="ID of the user who made the purchase")
    store_id: int | None = Field(
        default=None, foreign_key="stores.id", description="ID of the store where the purchase was made"
    )
    image_hash: str | None = Field(
        default=None,
        sa_column=Column(String(64), unique=True, index=True),
        description="Unique hash of the receipt image for deduplication",
    )

    user: User = Relationship(back_populates="receipts", sa_relationship_kwargs={"lazy": "select"})
    store: Store = Relationship(back_populates="receipts", sa_relationship_kwargs={"lazy": "select"})
    purchases: list[Transaction] = Relationship(back_populates="receipt", sa_relationship_kwargs={"lazy": "select"})

    @staticmethod
    def generate_image_hash(image_content: bytes) -> str:
        """Generate a SHA-256 hash for the given image content."""
        return hashlib.sha256(image_content).hexdigest()

    @classmethod
    def from_image_and_data(
        cls, image_content: bytes, user_id: int, store_id: int, date_time: datetime | None
    ) -> "GroceryReceipt":
        receipt_data = {
            "image_hash": cls.generate_image_hash(image_content),
            "user_id": user_id,
            "store_id": store_id,
            "date_time": date_time,
        }

        receipt = cls(**receipt_data)
        return receipt
