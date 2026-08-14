from dataclasses import dataclass
from typing import Any

@dataclass
class VAT:
    percentage: float

    @property
    def name(self) -> str:
        return f"VAT {self.percentage:g}%"

    def resolve_fields(self) -> dict[str, Any]:
        return {
            "Name": self.name,
            "Description": self.name,
            "Value": self.percentage,
        }