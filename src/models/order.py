from dataclasses import dataclass
from datetime import date
from typing import Any

from .debtor import Debtor
from .product import Product

@dataclass
class OrderItem:
    product: Product
    quantity: int

@dataclass
class Order:
    external_reference: str
    order_date: date
    debtor: Debtor
    items: list[OrderItem]
    discount: float
    isPaid: bool
    paid_at: date

    def resolve_fields(self) -> dict[str, Any]:
        return {
            "Date": self.order_date,
            "Cust.Ref.": self.external_reference,
            "Price mode": "Net",
            "VAT": "With VAT",
        }