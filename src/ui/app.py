import uiautomation as auto
from src.ui.window import FakturamaWindow

class FakturamaApp:
    def connect(self) -> FakturamaWindow:
        self.window = auto.WindowControl(
            searchDepth=1,
            RegexName=r"^Fakturama.*",
        )

        if not self.window.Exists(5):
            print("Fakturama.exe Is Not Running")
            exit(-1)

        self.window.SetFocus()

        return FakturamaWindow(self.window)
