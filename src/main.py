import sys

from src.entities.debtors import DebtorUI
from src.entities.VATs import VATsUI
from src.entities.payment_methods import PaymentMethodUI
from src.entities.products import ProductsUI
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
        
    app = FakturamaApp()
    window = app.connect()
    
    image_path = sys.argv[1]
    
    nNClient = N8NClient()
    order = nNClient.parse_order_image(image_path)
    
    # order = Order(external_reference='WEB-2026-0714-A17', created_at='2026-07-14', discount=None, debtor=Debtor(company='Northstar Office GmbH', first_name='Marta', last_name='Klein', street='Friedrichstrasse 88', zip_code='10117', city='Berlin', country='Germany', email='marta.klein@example.test', telephone='+49 30 5550 1420', payment_method=PaymentMethod(name='Bank Transfer'), alias=None, salutation="---", additional_name=None, address_specification=None, district=None), items=[Product(sku='CHR-ERG-01-VAT19', description='Ergonomic Desk Chair', quantity=2, vat=VAT(percentage=19), net_price=250), Product(sku='MAT-DES-02-VAT19', description='Anti-Fatigue Desk Mat', quantity=3, vat=VAT(percentage=19), net_price=40)], isPaid=True, paid_at='2026-07-18')
    
    uniqueVats = list({
        item.vat.percentage: item.vat
        for item in order.items
    }.values())
    
    workflows = [
        EntityWorkflow(
            window,
            order.debtor.payment_method,
            PaymentMethodUI
        ),
        *[
            EntityWorkflow(
                window,
                vat,
                VATsUI,
            )
            for vat in uniqueVats
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
    
    OID = OrderCreationWorkflow(window, order).run()
    
    InvoiceCreationWorkflow(
        window,
        order,
        OID
    ).run()
    
if __name__ == "__main__":
    main()