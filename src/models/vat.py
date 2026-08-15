from dataclasses import dataclass
from typing import Any

from .formatting import TAX_FREE_LABEL, TAX_FREE_NAME


@dataclass
class VAT:
    percentage: float

    @property
    def name(self) -> str:
        return f"VAT {self.percentage:g}%"

    def search_query(self) -> str:
        return f"{self.name} {self.name}"

    def resolve_fields(self) -> dict[str, Any]:
        return {
            "Name": self.name,
            "Description": self.name,
            "Value": str(self.percentage),
        }

    @classmethod
    def tax_free_resolve_fields(cls) -> dict[str, Any]:
        return {
            "Name": TAX_FREE_NAME,
            "Description": TAX_FREE_LABEL,
            "Value": "0",
        }

    @classmethod
    def tax_free_search_query(cls) -> str:
        fields = cls.tax_free_resolve_fields()
        return f"{fields['Name']} {fields['Description']}"
