from src.models.order import OrderItem
from src.ui.dialogs.common import DialogHelper, ROW_HEIGHT, ROW_START_OFFSET
from src.ui.window import FakturamaWindow

class ProductPickerDialog:
    DIALOG_NAME = "Select a product"

    def __init__(self, window: FakturamaWindow):
        self.window = window
        self._helper = DialogHelper(window)

    def _modify_item_quantities(self, item: OrderItem, index: int) -> None:
        num_text = self.window.find_text("No.")
        parent = num_text.GetParentControl()
        if parent is None:
            raise RuntimeError("Section text has no parent")
        table = parent.GetChildren()[-1]
        row_y = ROW_START_OFFSET + (index + 1) * ROW_HEIGHT

        for column_offset in (0, 7):
            table.Click(x=75 + 100 * column_offset, y=row_y)
            self.window.send_keys(f"{item.quantity}")
            self.window.send_keys("{ENTER}")

    def populate_items(self, items: list[OrderItem]) -> None:
        for index, item in enumerate(items):
            self._helper.click_section_button(section_label="Items", button_index=1)

            self._helper.search_and_select_first_row(
                self.DIALOG_NAME,
                item.product.search_query(),
            )

            self._modify_item_quantities(item, index)
