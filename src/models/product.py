from dataclasses import dataclass
from typing import Any
from .vat import VAT

@dataclass
class Product:
    sku: str
    description: str
    vat: VAT | None = None
    net_price: float = 0.0

    @property
    def gross_price(self) -> float:
        return round(
            self.net_price * (1 + self.vat.percentage / 100),
            2,
        ) if self.vat else self.net_price

    def resolve_fields(self) -> dict[str, Any]:
        return {
            "Item Number": self.sku,
            "Name": self.description,
            "Description": self.description,
            "Price (gross)": self.gross_price,
            "Cost price (net)": self.net_price,
            "VAT": (
                self.vat.name
                if self.vat
                else "Pay Cash"
            ),
        }