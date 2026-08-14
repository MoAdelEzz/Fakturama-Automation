from dataclasses import dataclass
from typing import Any

PAYMENT_CODE_MAP = {
    "Bank Transfer": "Credit transfer",
    "Credit Card": "Credit card",
    "SEPA Direct Debit": "SEPA direct debit",
}

@dataclass
class PaymentMethod:
    name: str
    payment_code: str


    def resolve_fields(self) -> dict[str, Any]:        
        return {
            "Name": self.name,
            "Description": self.name,
            "Payment code": self.payment_code,
            "Cash discount": 0,
            "Discount Days": 0,
            "Net Days": 0,
        }