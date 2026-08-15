from dataclasses import dataclass
from datetime import date
from typing import Any

from .debtor import Debtor
from .formatting import format_fakturama_date
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

    def order_date_parts(self) -> list[str]:
        return format_fakturama_date(self.order_date)

    def paid_date_parts(self) -> list[str] | None:
        if self.paid_at is None:
            return None
        return format_fakturama_date(self.paid_at)

    def discount_display(self) -> str | None:
        if self.discount is None:
            return None
        return f"{self.discount}"

    def resolve_fields(self) -> dict[str, Any]:
        return {
            "Date": self.order_date_parts(),
            "Cust.Ref.": self.external_reference,
            "Price mode": "Net",
            "Discount": self.discount_display(),
        }
