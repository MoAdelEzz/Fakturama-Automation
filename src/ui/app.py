import uiautomation as auto
from src.ui.window import FakturamaWindow


class FakturamaApp:
    def connect(self) -> FakturamaWindow:
        self.window = auto.WindowControl(
            searchDepth=1,
            RegexName=r"^Fakturama.*",
        )

        if not self.window.Exists(5):
            raise RuntimeError(
                "Fakturama.exe is not running. "
                "Please start Fakturama and try again."
            )

        self.window.SetFocus()

        return FakturamaWindow(self.window)
