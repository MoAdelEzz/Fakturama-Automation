from dataclasses import dataclass
from typing import Any

from .formatting import DEFAULT_PAYMENT, TAX_FREE_LABEL
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

    def search_query(self) -> str:
        return self.sku

    def formatted_gross_price(self) -> str:
        return f"{self.gross_price}"

    def vat_combo_label(self) -> str:
        return self.vat.name if self.vat else TAX_FREE_LABEL

    def resolve_fields(self) -> dict[str, Any]:
        return {
            "Item Number": self.sku,
            "Name": self.description,
            "Description": self.description,
            "Price (gross)": self.formatted_gross_price(),
            "Cost price (net)": self.net_price,
            "VAT": self.vat_combo_label(),
        }
