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
    
    def _parse_data(self):
        data: VAT | None = self.data
        name = data.name if data is not None else "Tax-free"
        description = name if data is not None else "Free of Tax"
        
        return name, description
        
    def search_value(self) -> str:
        name, description = self._parse_data()
        return f"{name} {description}"

    def fill_form(self):
        name, description = self._parse_data()

        self.window.edit_text_field(
            field_name="Name",
            value=name,
        )

        self.window.edit_text_field(
            field_name="Description",
            value=name,
        )

        self.window.edit_text_field(
            field_name="Value",
            value=description,
        )

        self.window.save()