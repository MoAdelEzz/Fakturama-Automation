from datetime import date

TAX_FREE_NAME = "Tax-free"
TAX_FREE_LABEL = "Free of Tax"
DEFAULT_PAYMENT = "Pay Cash"


def format_fakturama_date(d: date) -> list[str]:
    return [
        f"{d.day:02d}",
        f"{d.month:02d}",
        str(d.year),
    ]
