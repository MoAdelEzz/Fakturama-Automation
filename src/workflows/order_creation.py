from src.models.order import Order
from src.ui.dialogs.address_picker import AddressPickerDialog
from src.ui.dialogs.product_picker import ProductPickerDialog
from src.ui.forms.order_form import OrderFormUI
from src.ui.window import FakturamaWindow


class OrderCreationWorkflow:
    def __init__(
        self,
        window: FakturamaWindow,
        order: Order,
    ):
        self.window = window
        self.order = order

    def run(self):
        self.window.focus()

        form = OrderFormUI(self.window)
        form.open()
        order_number = form.get_order_number()
        form.populate_general_info(self.order)
        form.populate_discount(self.order)

        AddressPickerDialog(self.window).select(self.order.debtor)
        ProductPickerDialog(self.window).populate_items(self.order.items)

        self.window.save()

        return order_number
