from dataclasses import dataclass
from typing import Any

from .formatting import TAX_FREE_LABEL, TAX_FREE_NAME


@dataclass
class VAT:
    percentage: float | None

    @property
    def name(self) -> str:
        return f"VAT {self.percentage:g}%" if self.percentage is not None else TAX_FREE_NAME
    
    @property
    def description(self) -> str:
        return f"VAT {self.percentage:g}%" if self.percentage is not None else TAX_FREE_LABEL

    def search_query(self) -> str:
        return f"{self.name} {self.description}"
    
    def apply(self, price: float) -> float:
        return round(
            price * (1 + self.percentage / 100),
            2,
        ) if self.percentage is not None else price

    def resolve_fields(self) -> dict[str, Any]:
        return {
            "Name": self.name,
            "Description": self.description,
            "Value": str(self.percentage),
        }