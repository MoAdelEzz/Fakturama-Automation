from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from src.models.payment import PaymentMethod
from src.models.vat import VAT

from .debtor import Debtor
from .formatting import format_fakturama_date
from .product import Product

@dataclass
class Order:
    external_reference: str
    created_at: str
    discount: float | None
    
    debtor: Debtor
    items: list[Product]
    isPaid: bool
    paid_at: str

    def created_at_parts(self) -> list[str]:
        return format_fakturama_date(self.created_at)

    def paid_date_parts(self) -> list[str] | None:
        if self.paid_at is None:
            return None
        return format_fakturama_date(self.paid_at)

    def discount_display(self) -> str | None:
        if self.discount is None:
            return None
        return f"{self.discount}"

    def resolve_fields(self) -> dict[str, Any]:
        return {
            "Date": self.created_at_parts(),
            "Cust.Ref.": self.external_reference,
            "Price mode": "Net",
            "Discount": self.discount_display(),
        }

    @staticmethod
    def from_json(data: dict):
        debtor = data["debtor"]
        payment = data["payment"]

        return Order(
            created_at=data["order_created_at"],
            external_reference=data["order_external_refernece"],
            discount=data.get("order_level_discount", None),
            debtor=Debtor(
                company=debtor["company"],
                first_name=debtor["first_name"],
                last_name=debtor["last_name"],
                street=debtor["street"],
                zip_code=debtor["zip_code"],
                city=debtor["city"],
                country=debtor["country"],
                salutation=debtor.get("salutaion") or "---",
                address_specification=debtor.get("addressSpecification", None),
                district=debtor.get("district", None),
                email=debtor["email"],
                alias=debtor.get("alias", None),
                additional_name=None,
                telephone=debtor["telephone"],
                payment_method=PaymentMethod(
                    name=payment.get("paymentMethod", None)
                ),
            ),
            items=[
                Product(
                    description=product.get("description", product["sku"]),
                    sku=f"{product["sku"]}-VAT{product.get("vat", 0)}",
                    net_price=product["unit_price"],
                    discount=product.get("discount", 0),
                    quantity=product["quantity"],
                    vat=VAT(product["vat"]),
                )
                for product in data["items"]
            ],
            paid_at=payment.get("paid_at", None),
            isPaid=payment.get("isPaid", False),
        )

    @staticmethod
    def load(source: str) -> "Order":
        source = source.strip()

        if source.startswith("{"):
            data = json.loads(source)
        else:
            path = Path(source)
            if not path.exists():
                raise FileNotFoundError(
                    f"Order JSON not found: {path}"
                )
            data = json.loads(path.read_text(encoding="utf-8"))

        return Order.from_json(data)