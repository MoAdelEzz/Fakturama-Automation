from src.models.product import Product
from .base import FakturamaEntityUI


class ProductsUI(FakturamaEntityUI):
    @property
    def footer_tab_name(self) -> str:
        return "Products"

    @property
    def create_button_name(self) -> str:
        return "Create a new product"

    @property
    def creation_tab_name(self) -> str:
        return "New product"

    def _parse_data(self) -> Product:
        return self.data

    def search_value(self) -> str:
        return self._parse_data().search_query()

    def fill_form(self):
        data = self._parse_data()
        fields = data.resolve_fields()

        self.window.edit_text_field(
            field_name="Item Number",
            value=fields["Item Number"],
        )

        self.window.edit_text_field(
            field_name="Name",
            value=fields["Name"],
        )

        self.window.edit_fields(
            label_name="Price (gross)",
            values=[fields["Price (gross)"]],
        )

        self.window.edit_combobox_field(
            field_name="VAT",
            value=fields["VAT"],
        )
