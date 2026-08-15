import ctypes

def get_dpi_scale() -> float:
    return ctypes.windll.user32.GetDpiForSystem() / 96.0