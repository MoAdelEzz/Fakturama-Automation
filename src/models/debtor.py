from dataclasses import dataclass
from typing import Any

from .formatting import DEFAULT_PAYMENT
from .payment import PaymentMethod


@dataclass
class Debtor:
    company: str
    first_name: str
    last_name: str

    street: str
    zip_code: str
    city: str
    country: str

    email: str
    telephone: str

    payment_method: PaymentMethod
    
    alias: str | None = None

    salutation: str = "---"
    additional_name: str | None = None
    address_specification: str | None = None
    district: str | None = None

    def search_query(self) -> str:
        return (
            f"{self.first_name} {self.last_name} "
            f"{self.company} {self.zip_code} {self.city}"
        )

    def payment_label(self) -> str:
        return (
            self.payment_method.name
            if self.payment_method
            else DEFAULT_PAYMENT
        )

    def resolve_fields(self) -> dict[str, Any]:
        return {
            "Company": self.company,
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Salutation": self.salutation,
            "Addresses": {
                "Street": self.street,
                "ZIP": self.zip_code,
                "City": self.city,
                "Country": self.country,
                "E-Mail": self.email,
                "Telephone": self.telephone,
                "additional name": self.additional_name,
                "Address specification": self.address_specification,
                "district": self.district,
                "address type": "Invoice address",
            },
            "Miscellaneous": {
                "Alias name": self.alias,
                "Net or Gross": "Net",
                "Payment": self.payment_label(),
            },
        }
