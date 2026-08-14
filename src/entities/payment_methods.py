from .base import FakturamaEntityUI

class PaymentMethodUI(FakturamaEntityUI):
    @property
    def footer_tab_name(self) -> str:
        return "terms of payment"

    @property
    def create_button_name(self) -> str:
        return "Create a new term of payment"

    @property
    def creation_tab_name(self) -> str:
        return "New Term of Payment"

    def search_value(self) -> str:
        return f"{self.data.name} {self.data.name}" if self.data is not None else "Cash Pay Cash"

    def fill_form(self):
        self.window.edit_text_field(
            field_name="Name",
            value=self.data.name,
        )

        self.window.edit_text_field(
            field_name="Description",
            value=self.data.name,
        )

        self.window.edit_combobox_field(
            field_name="!editorPaymentPaymentcode!",
            value=self.data.payment_code,
        )

        self.window.save()