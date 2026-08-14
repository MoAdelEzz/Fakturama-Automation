from typing import Callable, Generic, TypeVar

from src.entities.base import FakturamaEntityUI
from src.ui.window import FakturamaWindow


T = TypeVar("T")
UI = TypeVar("UI", bound=FakturamaEntityUI)

class EntityWorkflow(Generic[T, UI]):
    def __init__(
        self,
        window: FakturamaWindow,
        data: T | None,
        ui_builder: Callable[
            [FakturamaWindow, T | None],
            UI,
        ],
    ):
        self.ui = ui_builder(window, data)

    def run(self):
        self.ui.open_footer_tab()

        count = self.ui.search()

        if count == 1:
            self.ui.resetWindow()
            return

        if count > 1:
            raise RuntimeError(
                f"Multiple records found "
                f"for '{self.ui.data.description}' ({count})"
            )

        self.ui.open_create_form()
        self.ui.fill_form()
        self.ui.save()