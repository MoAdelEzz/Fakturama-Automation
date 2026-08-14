from src.models.debtor import Debtor
from .base import FakturamaEntityUI

class DebtorUI(FakturamaEntityUI):
    @property
    def footer_tab_name(self) -> str:
        return "Debtors"

    @property
    def create_button_name(self) -> str:
        return "Create a new debtor"

    @property
    def creation_tab_name(self) -> str:
        return "New Debtor"
    
    def _parse_data(self):
        data: Debtor | None = self.data
        
        if data is None:
            raise TypeError("DEBTOR_IS_REQUIRED")
            
        return data
        
    def search_value(self) -> str:
        data: Debtor = self._parse_data()
        return f"{data.first_name} {data.last_name} { data.company } { data.zip_code } {data.city}"
    
    def fill_form(self):
        data: Debtor = self._parse_data()

        self.window.edit_text_field(
            field_name="Company",
            value=data.company,
        )
        
        self.window.edit_fields(
            label_name="First Name Last Name",
            values=[data.first_name, data.last_name]
        )
        
        if data.additional_name is not None:
            self.window.edit_text_field(
                field_name="additional name",
                value=data.additional_name,
            )
        
        self.window.edit_text_field(
            field_name="Street",
            value=data.street
        )
        
        if data.address_specification is not None:
            self.window.edit_text_field(
                field_name="Address specification",
                value=data.address_specification,
            )
        
        if data.district is not None:
            self.window.edit_text_field(
                field_name="district",
                value=data.district,
            )
        
        self.window.edit_fields(
            label_name="ZIP - City",
            values=[data.zip_code, data.city]
        )
        
        self.window.edit_combobox_field(
            field_name="Country",
            value=data.country
        )
        
        self.window.edit_fields(
            label_name="address type",
            values=["Invoice address"]
        )
        
        self.window.edit_text_field(
            field_name="E-Mail",
            value=data.email
        )
        
        self.window.edit_text_field(
            field_name="Telephone",
            value=data.telephone
        )
        
        self.window.open_tab("Miscellaneous")

        if data.alias is not None:
            self.window.edit_text_field(
                field_name="Alias name",
                value=data.alias
            )
        
        self.window.edit_combobox_field(
            field_name="Net or Gross",
            value="Net"
        )
        
        if data.payment_method is not None:
            self.window.edit_combobox_field(
                field_name="Payment",
                value=data.payment_method.name
            )

        self.window.save()