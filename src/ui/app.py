import uiautomation as auto

from .window import FakturamaWindow

class FakturamaApp:
    def connect(self) -> FakturamaWindow:
        self.window = auto.WindowControl(
            searchDepth=1,
            RegexName=r"^Fakturama - .*",
        )

        if not self.window.Exists(5):
            raise RuntimeError("Fakturama window not found")

        self.window.SetFocus()

        return FakturamaWindow(self.window)