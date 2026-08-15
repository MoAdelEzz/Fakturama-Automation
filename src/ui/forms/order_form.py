from src.models.order import Order
from src.ui.window import FakturamaWindow


class OrderFormUI:
    TAB_NAME = "New Order"
    CREATE_BUTTON = "Create: New Order"

    def __init__(self, window: FakturamaWindow):
        self.window = window

    def open(self) -> None:
        is_open, _ = self.window.is_tab_opened(self.TAB_NAME)
        if not is_open:
            self.window.click_button(button_name=self.CREATE_BUTTON)

    def get_order_number(self) -> str:
        return self.window.get_labeled_field_value("No.")

    def populate_general_info(self, order: Order) -> None:
        self.window.enter_date_parts("Date", order.order_date_parts())
        self.window.set_price_mode("Net")
        self.window.edit_text_field(
            field_name="Cust.Ref.",
            value=order.external_reference,
        )

    def populate_discount(self, order: Order) -> None:
        discount = order.discount_display()
        if discount is not None:
            self.window.edit_text_field(
                field_name="Discount",
                value=discount,
            )
