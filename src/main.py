import argparse
import logging
import sys

from src.entities.debtors import DebtorUI
from src.entities.VATs import VATsUI
from src.entities.payment_methods import PaymentMethodUI
from src.entities.products import ProductsUI
from src.models.order import Order
from src.ui.app import FakturamaApp
from src.vision.n8n_controller import N8NClient
from src.workflows.entity import EntityWorkflow
from src.workflows.invoice_creation import InvoiceCreationWorkflow
from src.workflows.order_creation import OrderCreationWorkflow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Automate Fakturama order and invoice creation",
    )
    
    parser.add_argument(
        "image",
        nargs="?",
        help="Path to order image (parsed via n8n webhook)",
    )
    
    parser.add_argument(
        "--order",
        help="Order JSON — file path or inline JSON string",
    )
    
    args = parser.parse_args()

    if args.order and args.image:
        parser.error("Specify either an image path or --order, not both")
        
    if not args.order and not args.image:
        parser.error("Provide an image path or --order JSON")

    return args


def load_order(args) -> Order:
    if args.order:
        logger.info("Loading order from JSON")
        return Order.load(args.order)

    logger.info("Parsing order from %s", args.image)
    return N8NClient().parse_order_image(args.image)


def run_pipeline(window, order: Order):
    uniqueVats = list({
        item.vat.percentage: item.vat
        for item in order.items
    }.values())

    logger.info("Order parsed — reference: %s", order.external_reference)
    logger.info(
        "Debtor extracted: %s (%s %s)",
        order.debtor.company,
        order.debtor.first_name,
        order.debtor.last_name,
    )
    logger.info(
        "Payment method extracted: %s",
        order.debtor.payment_method.name or "default",
    )
    logger.info(
        "Unique VATs extracted: %s",
        [vat.name for vat in uniqueVats],
    )
    logger.info(
        "Products extracted: %s",
        [f"{item.sku} x{item.quantity}" for item in order.items],
    )

    logger.info("--- Ensuring payment method ---")
    EntityWorkflow(
        window,
        order.debtor.payment_method,
        PaymentMethodUI,
    ).run()

    logger.info("--- Ensuring VAT rates ---")
    for vat in uniqueVats:
        EntityWorkflow(window, vat, VATsUI).run()

    logger.info("--- Ensuring debtor ---")
    EntityWorkflow(window, order.debtor, DebtorUI).run()

    logger.info("--- Ensuring products ---")
    for item in order.items:
        EntityWorkflow(window, item, ProductsUI).run()

    logger.info("--- Creating order ---")
    OID = OrderCreationWorkflow(window, order).run()

    logger.info("--- Creating invoice ---")
    InvoiceCreationWorkflow(window, order, OID).run()

    logger.info("Pipeline complete — order %s invoiced", OID)


def main():
    args = parse_args()

    logger.info("Connecting to Fakturama...")
    app = FakturamaApp()
    window = app.connect()

    order = load_order(args)
    run_pipeline(window, order)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.error("Application stopped by user (Ctrl+C)")
        sys.exit(130)
    except RuntimeError as e:
        logger.error("Application stopped: %s", e)
        sys.exit(1)
    except Exception as e:
        logger.error("Application stopped due to unexpected error: %s", e)
        sys.exit(1)