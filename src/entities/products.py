from src.models.product import Product
from .base import FakturamaEntityUI

# NOTE: what if we concatenate vat to sku so that it becomes a unique id
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
    
    def _parse_data(self):
        data: Product = self.data
        return data
        
    def search_value(self) -> str:
        data = self._parse_data()
        return f"{data.sku}"

    def fill_form(self):
        data = self._parse_data()

        self.window.edit_text_field(
            field_name="Item Number",
            value=data.sku,
        )

        self.window.edit_text_field(
            field_name="Name",
            value=data.description,
        )
        
        self.window.edit_fields(
            label_name="Price (gross)",
            values=[f"{data.gross_price}"]
        )

        self.window.edit_combobox_field(
            field_name="VAT",
            value=data.vat.name if data.vat else "Free of Tax",
        )

        self.window.save()