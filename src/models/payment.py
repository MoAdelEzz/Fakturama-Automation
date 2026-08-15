from dataclasses import dataclass
from typing import Any

from .formatting import DEFAULT_PAYMENT

ALLOWED_METHODS = [
    "Bank Transfer",
    "Credit Card",
    "SEPA Direct Debit"
]

METHOD_CODE_MAP = {
    "Bank Transfer": "Credit transfer",
    "Credit Card": "Credit card",
    "SEPA Direct Debit": "SEPA direct debit"
}

@dataclass
class PaymentMethod:
    name: str | None
    
    @property
    def payment_code(self) -> str:
        return METHOD_CODE_MAP[self.name] if self.name is not None else DEFAULT_PAYMENT
    
    @property
    def description(self) -> str:
        return self.name if self.name is not None else DEFAULT_PAYMENT

    def search_query(self) -> str:
        return f"{self.name} {self.description}"

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
    def create_payment_method(method: str | None):
        if method in ALLOWED_METHODS:
            return PaymentMethod(
                name=method
            )
        else:
            return PaymentMethod(
                name=None
            )
