import logging

from src.models.order import Order
from src.ui.forms.invoice_form import InvoiceFormUI
from src.ui.window import FakturamaWindow

logger = logging.getLogger(__name__)


class InvoiceCreationWorkflow:
    def __init__(
        self,
        window: FakturamaWindow,
        order: Order,
        OID: str,
    ):
        self.window = window
        self.order = order
        self.OID = OID

    def run(self):
        logger.info(
            "Creating invoice from order %s (paid=%s)...",
            self.OID,
            self.order.isPaid,
        )
        self.window.focus()

        form = InvoiceFormUI(self.window)
        form.open_from_order(self.OID)
        form.fill_payment(self.order)

        self.window.save()
        self.window.close_active_tab()
        logger.info("Invoice for order %s saved successfully", self.OID)
