from datetime import date

TAX_FREE_NAME = "Tax-free"
TAX_FREE_LABEL = "Free of Tax"
DEFAULT_PAYMENT = "Pay Cash"


def format_fakturama_date(d: str) -> list[str]:
    parts = d.split("-")
    return [
        f"{int(parts[2]):02d}",
        f"{int(parts[1]):02d}",
        str(parts[0]),
    ]
