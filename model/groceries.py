from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class UnitType(StrEnum):
    LB = "lb"
    EACH = "ea"


class Store(BaseModel):
    name: str | None = Field(default=None, description="Name of the store")
    address: str | None = Field(default=None, description="Address of the store")
    phone: str | None = Field(default=None, description="Phone number of the store")


class Purchase(BaseModel):
    name: str = Field(description="Name of the purchased item")
    quantity: float = Field(description="Quantity of the purchased item")
    unit_price: float = Field(description="Unit price of the purchased item")
    unit_type: UnitType = Field(description="Unit type of the purchased item, e.g., lb, ea")


class GroceryReceipt(BaseModel):
    is_valid: bool = Field(description="Indicates if a valid grocery receipt")
    purchaser_username: str | None = Field(default=None, description="Username of purchaser")
    store: Store | None = Field(default=None, description="Store information")
    date_time: datetime | None = Field(default=None, description="Date and time of the purchase as datetime object")
    purchases: list[Purchase] | None = Field(default=None, description="List of purchased items")

    @property
    def total_cost(self) -> float:
        return sum(purchase.price * purchase.quantity for purchase in self.purchases)

    @property
    def total_items(self) -> int:
        return sum(purchase.quantity for purchase in self.purchases)
