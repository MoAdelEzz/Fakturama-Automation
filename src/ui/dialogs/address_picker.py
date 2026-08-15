from src.models.debtor import Debtor
from src.ui.dialogs.common import DialogHelper
from src.ui.window import FakturamaWindow

class AddressPickerDialog:
    DIALOG_NAME = "Select the address"

    def __init__(self, window: FakturamaWindow):
        self._helper = DialogHelper(window)

    def select(self, debtor: Debtor) -> None:
        self._helper.click_section_button("Addresses")
        self._helper.search_and_select_first_row(
            self.DIALOG_NAME,
            debtor.search_query(),
        )
