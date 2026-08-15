from src.models.order import Order
from src.ui.window import FakturamaWindow

class InvoiceFormUI:
    TAB_NAME = "New Invoice"

    def __init__(self, window: FakturamaWindow):
        self.window = window

    def open_from_order(self, order_tab_name: str) -> None:
        is_open, tab_control = self.window.is_tab_opened(order_tab_name)

        if not is_open or tab_control is None:
            raise RuntimeError("Order Form Is Not Opened")

        trigger = tab_control.ButtonControl(
            Name="Invoice",
            searchDepth=30,
        )
        trigger.Click()

        # Ensuring that the previous action was executed successfully.
        is_open, _ = self.window.is_tab_opened(self.TAB_NAME)
        if not is_open:
            raise RuntimeError("OPEN_NEW_INVOICE_FAILED")

    def fill_payment(self, order: Order) -> None:
        if not order.isPaid or order.paid_at is None:
            return

        self.window.set_checkbox("paid", checked=True)
        date_parts = order.paid_date_parts()
        if date_parts is not None:
            self.window.enter_date_parts("at", date_parts)
