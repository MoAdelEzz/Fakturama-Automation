import logging

from src.models.order import Order
from src.ui.dialogs.address_picker import AddressPickerDialog
from src.ui.dialogs.product_picker import ProductPickerDialog
from src.ui.forms.order_form import OrderFormUI
from src.ui.window import FakturamaWindow

logger = logging.getLogger(__name__)


class OrderCreationWorkflow:
    def __init__(
        self,
        window: FakturamaWindow,
        order: Order,
    ):
        self.window = window
        self.order = order

    def run(self):
        logger.info(
            "Creating order for debtor '%s' with %d item(s)...",
            self.order.debtor.company,
            len(self.order.items),
        )
        self.window.focus()

        form = OrderFormUI(self.window)
        form.open()
        order_number = form.get_order_number()
        logger.info("Order number assigned: %s", order_number)

        form.populate_general_info(self.order)
        form.populate_discount(self.order)

        logger.info("Selecting debtor address...")
        AddressPickerDialog(self.window).select(self.order.debtor)

        logger.info("Adding products to order...")
        ProductPickerDialog(self.window).populate_items(self.order.items)

        self.window.save()
        logger.info("Order %s saved successfully", order_number)

        return order_number
