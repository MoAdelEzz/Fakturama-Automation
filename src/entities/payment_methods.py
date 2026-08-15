from src.models.payment import PaymentMethod
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
        return self.data.search_query()

    def fill_form(self):
        if self.data is None:
            raise TypeError("PAYMENT_METHOD_IS_REQUIRED")

        fields = self.data.resolve_fields()

        self.window.edit_text_field(
            field_name="Name",
            value=fields["Name"],
        )

        self.window.edit_text_field(
            field_name="Description",
            value=fields["Description"],
        )

        self.window.edit_combobox_field(
            field_name="!editorPaymentPaymentcode!",
            value=fields["Payment code"],
        )
