from src.ui.window import FakturamaWindow

ROW_HEIGHT = 20
ROW_START_OFFSET = 10


class DialogHelper:
    def __init__(self, window: FakturamaWindow):
        self.window = window

    def click_section_button(self, section_label: str, button_index: int = 1) -> None:
        section_text = self.window.find_text(section_label)
        parent = section_text.GetParentControl()
        if parent is None:
            raise RuntimeError("Section text has no parent")
        siblings = parent.GetChildren()
        siblings[button_index].Click()

    def find_dialog(self, dialog_name: str):
        dialog = self.window.element.WindowControl(
            Name=dialog_name,
            searchDepth=30,
        )
        if not dialog.Exists(5):
            raise RuntimeError(f"Dialog '{dialog_name}' not found")
        return dialog

    def search_in_dialog(self, dialog, search_text: str):
        search_label = dialog.TextControl(Name="Search:")
        search_group = search_label.GetParentControl()
        search_field = search_group.EditControl(Name="")
        search_field.SendKeys("{CTRL}A")
        search_field.SendKeys(search_text)
        return search_group

    def select_first_table_row(self, search_group) -> bool:
        search_row = search_group.GetParentControl()
        if search_row is None:
            return False

        both_rows = search_row.GetParentControl().GetChildren()
        table = both_rows[1]

        table.Click(
            ratioX=0.25,
            y=ROW_START_OFFSET + ROW_HEIGHT,
        )
        return True

    def search_and_select_first_row(
        self,
        dialog_name: str,
        search_text: str,
    ) -> bool:
        dialog = self.find_dialog(dialog_name)
        search_group = self.search_in_dialog(dialog, search_text)
        selected = self.select_first_table_row(search_group)
        if selected:
            self.window.click_button("OK")
        return selected
