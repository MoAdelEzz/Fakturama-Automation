from dataclasses import dataclass
from typing import Any

from .formatting import DEFAULT_PAYMENT


@dataclass
class PaymentMethod:
    name: str
    payment_code: str

    def search_query(self) -> str:
        return f"{self.name} {self.name}"

    def resolve_fields(self) -> dict[str, Any]:
        return {
            "Name": self.name,
            "Description": self.name,
            "Payment code": self.payment_code,
            "Cash discount": 0,
            "Discount Days": 0,
            "Net Days": 0,
        }

    @staticmethod
    def default_search_query() -> str:
        return f"Cash {DEFAULT_PAYMENT}"
