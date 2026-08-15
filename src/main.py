import sys

from datetime import date

from src.entities.debtors import DebtorUI
from src.entities.VATs import VATsUI
from src.entities.payment_methods import PaymentMethodUI
from src.entities.products import ProductsUI
from src.models.vat import VAT
from src.models.payment import PaymentMethod
from src.models.debtor import Debtor
from src.models.product import Product
from src.models.order import Order
from src.ui.app import FakturamaApp
from src.vision.n8n_controller import N8NClient
from src.workflows.entity import EntityWorkflow
from src.workflows.invoice_creation import InvoiceCreationWorkflow
from src.workflows.order_creation import OrderCreationWorkflow


def main():
    if len(sys.argv) < 2:
        raise RuntimeError(
            "Usage: python -m src.main <image_path>"
        )
    image_path = sys.argv[1]
    
    nNClient = N8NClient()
    order = nNClient.parse_order_image(image_path)
    
    print(order)
    
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
                item.vat,
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
                item,
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