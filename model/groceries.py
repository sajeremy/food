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
    name: str
    quantity: float
    unit_price: float
    unit_type: UnitType


class GroceryReceipt(BaseModel):
    is_valid: bool = Field(description="Indicates if a valid grocery receipt")
    store: Store | None = Field(default=None, description="Store information")
    date_time: datetime | None = Field(default=None, description="Date and time of the purchase as datetime object")
    purchases: list[Purchase] | None = Field(default=None, description="List of purchased items")

    @property
    def total_cost(self) -> float:
        return sum(purchase.price * purchase.quantity for purchase in self.purchases)

    @property
    def total_items(self) -> int:
        return sum(purchase.quantity for purchase in self.purchases)
