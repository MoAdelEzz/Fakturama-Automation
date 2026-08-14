import time
import win32con
import win32gui
from abc import ABC, abstractmethod
from PIL import ImageGrab
from ..ui.window import FakturamaWindow
from ..vision.image_processor import count_rows

class FakturamaEntityUI(ABC):
    def __init__(
        self,
        window: FakturamaWindow,
        data,
    ):
        self.window = window
        self.data = data

    @property
    @abstractmethod
    def footer_tab_name(self) -> str:
        ...
    
    @property
    @abstractmethod
    def create_button_name(self) -> str:
        ...

    @property
    @abstractmethod
    def creation_tab_name(self) -> str:
        ...

    def open_footer_tab(self):
        self.window.open_sidebar_item(self.footer_tab_name)

    def _search_box(self):
        search = self.window.find_edit_under(
            self.footer_tab_name
        )

        if not search.Exists(5):
            raise RuntimeError(
                f"Search box not found in "
                f"'{self.footer_tab_name}'"
            )

        return search

    @abstractmethod
    def search_value(self) -> str:
        ...

    def search(self) -> int:
        self.window.focus()

        search = self._search_box()

        search.Click()
        search.SendKeys("{CTRL}A")
        search.SendKeys(self.search_value())

        try:
            return self.count_table_rows()
        except:
            print("Failed To Count Table Rows, Falling Back To Default Creation Process")
            return 0

    def _table(self):
        tab = self.window.element.TabControl(
            Name=self.footer_tab_name,
            searchDepth=30,
        )

        if not tab.Exists(5):
            raise RuntimeError(
                f"Tab '{self.footer_tab_name}' not found"
            )

        panes = tab.GetChildren()

        pane_controls = [
            child
            for child in panes
            if child.ControlTypeName == "PaneControl"
        ]

        if not pane_controls:
            raise RuntimeError(
                f"No panes found under "
                f"'{self.footer_tab_name}'"
            )

        return max(
            pane_controls,
            key=lambda pane: pane.BoundingRectangle.top,
        )

    def _capture_table(self):
        self.window.focus()

        table = self._table()

        hwnd = table.NativeWindowHandle

        if not hwnd:
            raise RuntimeError(
                f"'{self.footer_tab_name}' table "
                "has no native HWND"
            )

        win32gui.ShowWindow(
            hwnd,
            win32con.SW_RESTORE,
        )

        win32gui.SetForegroundWindow(hwnd)

        time.sleep(0.2)

        left, top, right, bottom = (
            win32gui.GetWindowRect(hwnd)
        )

        image = ImageGrab.grab(
            bbox=(left, top, right, bottom)
        )
        
        # image.save("debug/debug-payment-methods.png")
        
        return image

    def count_table_rows(self) -> int:
        image = self._capture_table()        
        numOfRows = count_rows(image)
        return numOfRows

    def open_create_form(self):
        button = self.window.element.ButtonControl(
            Name=self.create_button_name,
            searchDepth=30,
        )

        if not button.Exists(5):
            raise RuntimeError(
                f"Create button "
                f"'{self.create_button_name}' not found"
            )

        button.Click()

    @abstractmethod
    def fill_form(self):
        ...

    def resetWindow(self):
        self.window.close_active_tab()
        

    def save(self):
        self.window.save()
        self.resetWindow()