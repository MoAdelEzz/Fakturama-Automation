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

    def _parse_data(self) -> Debtor:
        data: Debtor | None = self.data

        if data is None:
            raise TypeError("DEBTOR_IS_REQUIRED")

        return data

    def search_value(self) -> str:
        return self._parse_data().search_query()

    def fill_form(self):
        data = self._parse_data()
        fields = data.resolve_fields()
        addresses = fields["Addresses"]
        misc = fields["Miscellaneous"]

        self.window.edit_text_field(
            field_name="Company",
            value=fields["Company"],
        )

        self.window.edit_fields(
            label_name="First Name Last Name",
            values=[fields["First Name"], fields["Last Name"]],
        )

        if addresses["additional name"] is not None:
            self.window.edit_text_field(
                field_name="additional name",
                value=addresses["additional name"],
            )

        self.window.edit_text_field(
            field_name="Street",
            value=addresses["Street"],
        )

        if addresses["Address specification"] is not None:
            self.window.edit_text_field(
                field_name="Address specification",
                value=addresses["Address specification"],
            )

        if addresses["district"] is not None:
            self.window.edit_text_field(
                field_name="district",
                value=addresses["district"],
            )

        self.window.edit_fields(
            label_name="ZIP - City",
            values=[addresses["ZIP"], addresses["City"]],
        )

        self.window.edit_combobox_field(
            field_name="Country",
            value=addresses["Country"],
        )

        self.window.edit_fields(
            label_name="address type",
            values=[addresses["address type"]],
        )

        self.window.edit_text_field(
            field_name="E-Mail",
            value=addresses["E-Mail"],
        )

        self.window.edit_text_field(
            field_name="Telephone",
            value=addresses["Telephone"],
        )

        self.window.open_tab("Miscellaneous")

        if misc["Alias name"] is not None:
            self.window.edit_text_field(
                field_name="Alias name",
                value=misc["Alias name"],
            )

        self.window.edit_combobox_field(
            field_name="Net or Gross",
            value=misc["Net or Gross"],
        )

        if data.payment_method is not None:
            self.window.edit_combobox_field(
                field_name="Payment",
                value=misc["Payment"],
            )
