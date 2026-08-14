from dataclasses import dataclass
from typing import Any
from .payment_method import PaymentMethod

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

    alias: str | None = None

    salutation: str = "---"
    additional_name: str | None = None
    address_specification: str | None = None
    district: str | None = None
    payment_method: PaymentMethod | None = None

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
                "address type": "Invoice address"
            },
            "Miscellaneous": {
                "Alias name": self.alias,
                "Net or Gross": "Net",
                "Payment Method": (
                    self.payment_method.name
                    if self.payment_method
                    else "Pay Cash"
                ), 
            }
        }