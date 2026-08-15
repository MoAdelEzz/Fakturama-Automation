from src.models.vat import VAT
from .base import FakturamaEntityUI


class VATsUI(FakturamaEntityUI):
    @property
    def footer_tab_name(self) -> str:
        return "VATs"

    @property
    def create_button_name(self) -> str:
        return "Create a new tax rate"

    @property
    def creation_tab_name(self) -> str:
        return "New TAX Rate"

    @property
    def entity_name(self) -> str:
        return "VAT rate"

    @property
    def entity_target(self) -> str:
        return self.data.name

    def _resolve_fields(self) -> dict[str, str]:
        data: VAT = self.data
        return data.resolve_fields()

    def search_value(self) -> str:
        data: VAT = self.data
        return data.search_query()

    def fill_form(self):
        fields = self._resolve_fields()

        self.window.edit_text_field(
            field_name="Name",
            value=fields["Name"],
        )

        self.window.edit_text_field(
            field_name="Description",
            value=fields["Description"],
        )

        self.window.edit_text_field(
            field_name="Value",
            value=fields["Value"],
        )
