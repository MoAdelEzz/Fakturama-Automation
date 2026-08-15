from dotenv import load_dotenv

from src.entities.debtors import DebtorUI
from src.entities.VATs import VATsUI
from src.entities.payment_methods import PaymentMethodUI
from src.entities.products import ProductsUI
from src.workflows.entity import EntityWorkflow
from src.workflows.invoice_creation import InvoiceCreationWorkflow
from src.workflows.order_creation import OrderCreationWorkflow
load_dotenv()

from datetime import date
from .models.vat import VAT
from .models.payment import PaymentMethod
from .models.debtor import Debtor
from .models.product import Product
from .models.order import Order, OrderItem
from .ui.app import FakturamaApp


def create_mock_order() -> Order:
    payment_method = PaymentMethod(
        name="Test",
        payment_code="Credit transfer",
    )

    vat_19 = VAT(
        percentage=19,
    )

    debtor = Debtor(
        company="Northstar Office GmbH",
        first_name="Marta",
        last_name="Klein",

        street="Friedrichstrasse 88",
        zip_code="10117",
        city="Berlin",
        country="Germany",

        email="marta.klein@example.test",
        telephone="+49 30 5550 1420",

        alias="NORTHSTAR-BERLIN",

        payment_method=payment_method,
    )

    desk_chair = Product(
        sku="CHR-ERG-01",
        description="Ergonomic Desk Chair",
        vat=vat_19,
        net_price=250.00,
    )

    desk_mat = Product(
        sku="MAT-DESK-02",
        description="Anti-Fatigue Desk Mat",
        net_price=40.00,
    )

    return Order(
        external_reference="WEB-2026-0714-A17",
        order_date=date(2026, 7, 14),
        debtor=debtor,
        items=[
            OrderItem(
                product=desk_chair,
                quantity=2,
            ),
            OrderItem(
                product=desk_mat,
                quantity=3,
            ),
        ],
        discount=10,
        isPaid=True,
        paid_at=date(2004, 8, 10),
    )


def main():
    order = create_mock_order()

    app = FakturamaApp()
    window = app.connect()

    workflows = [
        EntityWorkflow(
            window,
            order.debtor.payment_method,
            PaymentMethodUI
        ),
        *[
            EntityWorkflow(
                window,
                item.product.vat,
                VATsUI,
            )
            for item in order.items
        ],
        EntityWorkflow(
            window,
            order.debtor,
            DebtorUI
        ),
        *[
            EntityWorkflow(
                window,
                item.product,
                ProductsUI,
            )
            for item in order.items
        ],
    ]
    
    for workflow in workflows:
        workflow.run()
    
    orderWorkflow = OrderCreationWorkflow(window, order)
    orderNumber = orderWorkflow.run()
    
    invoiceWorkflow = InvoiceCreationWorkflow(
        window,
        order,
        orderNumber
    )
    invoiceWorkflow.run()
    
    


if __name__ == "__main__":
    main()