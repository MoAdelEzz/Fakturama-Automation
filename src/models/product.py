from dataclasses import dataclass
from typing import Any

from .formatting import DEFAULT_PAYMENT, TAX_FREE_LABEL
from .vat import VAT


@dataclass
class Product:
    sku: str
    description: str
    quantity: int
    vat: VAT
    net_price: float = 0.0

    @property
    def gross_price(self) -> float:
        return self.vat.apply(self.net_price)

    def search_query(self) -> str:
        return self.sku

    def formatted_gross_price(self) -> str:
        return f"{self.gross_price}"

    def resolve_fields(self) -> dict[str, Any]:
        return {
            "Item Number": self.sku,
            "Name": self.description,
            "Description": self.description,
            "Price (gross)": self.formatted_gross_price(),
            "Cost price (net)": self.net_price,
            "VAT": self.vat.name,
        }
