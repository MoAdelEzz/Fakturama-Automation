import uiautomation as auto
from typing import Any
import re


class FakturamaWindow:
    def __init__(self, element: Any):
        self.element = element

    def find_text(self, name: str) -> auto.Control:
        control = self.element.TextControl(
            Name=name,
            searchDepth=30,
        )
        if not control.Exists(5):
            raise RuntimeError(f"Text control '{name}' not found in window")
        return control

    def send_keys(self, keys: str) -> None:
        self.element.SendKeys(keys)

    def find_edit_under(
        self,
        tab_name: str,
    ) -> auto.Control:
        tab = self.element.TabControl(
            Name=tab_name,
            searchDepth=30,
        )

        if not tab.Exists(5):
            raise RuntimeError(
                f"Tab not found: {tab_name}"
            )

        pane = tab.PaneControl(
            Name=tab_name,
            searchDepth=10,
        )

        if not pane.Exists(5):
            raise RuntimeError(
                f"Pane not found under tab: {tab_name}"
            )

        edit = pane.EditControl(
            searchDepth=30,
        )

        if not edit.Exists(5):
            raise RuntimeError(
                f"Edit control not found under: {tab_name}"
            )

        return edit

    def edit_text_field(
        self,
        field_name: str,
        value: str,
    ) -> None:
        target = self.element.EditControl(
            Name=field_name,
            searchDepth=30,
        )

        if not target.Exists(5):
            raise RuntimeError(
                f"Text field '{field_name}' "
                f"not found in window"
            )

        target.Click()
        target.SendKeys("{CTRL}A")
        target.SendKeys(value)

    def edit_combobox_field(
        self,
        field_name: str,
        value: str,
    ) -> None:
        target = self.element.ComboBoxControl(
            Name=field_name,
            searchDepth=30,
        )

        if not target.Exists(5):
            raise RuntimeError(
                f"Combo box '{field_name}' "
                f"not found in window"
            )

        target.Click()
        target.SendKeys(value)

        item = target.ListItemControl(
            RegexName=rf"{re.escape(value)}",
            searchDepth=10,
        )

        if item.Exists(3):
            item.Click()
            return

        raise RuntimeError(
            f"Combo box option '{value}' "
            f"not found for '{field_name}'"
        )

    def edit_combobox_node(
        self,
        target,
        value: str,
    ) -> None:
        target.Click()
        target.SendKeys(value)

        item = target.ListItemControl(
            RegexName=rf"{re.escape(value)}",
            searchDepth=10,
        )

        if item.Exists(3):
            item.Click()
            return

        raise RuntimeError(
            f"Combo box option '{value}' "
            f"not found"
        )

    def click_button(self, button_name):
        target = self.element.ButtonControl(
            Name=button_name,
            searchDepth=30,
        )

        if not target.Exists(5):
            raise RuntimeError(
                f"Button '{button_name}' "
                f"not found in window"
            )

        target.Click()

    def get_fields(self, label_name: str, count: int):
        label = self.element.TextControl(Name=label_name, searchDepth=30)
        if not label.Exists(5):
            raise RuntimeError(f"Label '{label_name}' not found in window")

        pane = label.GetNextSiblingControl()
        if pane is None or pane.ControlTypeName != "PaneControl":
            raise RuntimeError(
                f"Expected a PaneControl after label '{label_name}', got "
                f"{pane.ControlTypeName if pane else None}"
            )

        edit_fields = [
            c for c in pane.GetChildren()
            if c.ControlTypeName == "EditControl"
        ]

        if len(edit_fields) != count:
            raise RuntimeError(
                f"Expected {count} edit fields in pane after '{label_name}', "
                f"found {len(edit_fields)}"
            )

        return edit_fields

    def get_labeled_field_value(self, label_name: str) -> str:
        [field] = self.get_fields(label_name=label_name, count=1)
        value_pattern = field.GetValuePattern()

        if value_pattern is None:
            raise RuntimeError(
                f"Could not get value pattern for '{label_name}' field"
            )

        return value_pattern.Value

    def enter_date_parts(self, label_name: str, date_parts: list[str]) -> None:
        [date_target] = self.get_fields(label_name=label_name, count=1)
        for value in date_parts:
            date_target.SendKeys(str(value))

    def set_price_mode(self, mode: str) -> None:
        [date_target] = self.get_fields(label_name="Date", count=1)
        parent = date_target.GetParentControl()
        siblings = parent.GetParentControl().GetChildren()
        gross_net_combo = siblings[-1]
        self.edit_combobox_node(gross_net_combo, mode)

    def set_checkbox(self, name: str, checked: bool) -> None:
        checkbox = self.element.CheckBoxControl(
            Name=name,
            searchDepth=30,
        )
        if not checkbox.Exists(5):
            raise RuntimeError(f"Checkbox '{name}' not found in window")

        toggle_pattern = checkbox.GetTogglePattern()
        if toggle_pattern is None:
            if checked:
                checkbox.Click()
            return

        if toggle_pattern.ToggleState != 1 and checked:
            checkbox.Click()
        elif toggle_pattern.ToggleState == 1 and not checked:
            checkbox.Click()

    def edit_fields(self, values: list[str], label_name: str) -> None:
        fields = self.get_fields(label_name, len(values))

        for field, value in zip(fields, values):
            field.Click()
            field.SendKeys("{CTRL}A")
            field.SendKeys(value)

    def open_tab(self, tab_name: str):
        tab = self.element.TabItemControl(
            Name=tab_name,
            searchDepth=30,
        )

        if not tab.Exists(5):
            raise RuntimeError(
                f"Footer tab '{tab_name}' not found"
            )

        tab.Click()

    def is_tab_opened(self, tab_name: str):
        def walk(control):
            yield control

            for child in control.GetChildren():
                yield from walk(child)

        pattern = re.compile(
            rf"\*?{re.escape(tab_name)}"
        )

        for control in walk(self.element):
            if not isinstance(control, auto.TabItemControl):
                continue

            if not pattern.match(control.Name):
                continue

            selection = control.GetSelectionItemPattern()

            if selection and selection.IsSelected:
                tabControl = self.element.TabControl(
                    Name=tab_name,
                    searchDepth=30
                )
                return True, tabControl

        return False, None

    def save(self):
        target = self.element.ButtonControl(
            Name="Save the current contents",
            searchDepth=30,
        )

        if not target.Exists(5):
            raise RuntimeError(
                "Save button not found"
            )

        target.Click()

        if target.IsEnabled:
            raise RuntimeError("SAVE_BUTTON_FAILED")

    def focus(self) -> None:
        self.element.SetFocus()

    def close_active_tab(self) -> None:
        self.focus()
        self.element.SendKeys("{CTRL}{SHIFT}W")

    def open_sidebar_item(self, name: str) -> None:
        self.focus()

        isOpen, _ = self.is_tab_opened(name)

        if isOpen:
            return

        control = self.element.TextControl(
            searchDepth=20,
            Name=name,
        )

        if not control.Exists(5):
            raise RuntimeError(
                f"Could not find sidebar item: {name}"
            )

        control.Click()

        self.open_tab(name)
