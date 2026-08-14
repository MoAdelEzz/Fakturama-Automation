import cv2
import numpy as np

# Geometry of the Fakturama table.
FIRST_ROW_TOP = 57
ROW_HEIGHT = 20

# Only inspect the actual table area.
X_START = 0
X_END = 630

# Ignore very light pixels.
DARK_THRESHOLD = 120

def _row_has_content(
    image: np.ndarray,
    row_top: int,
) -> bool:
    y_start = row_top + 3
    y_end = row_top + ROW_HEIGHT - 3

    _, width = image.shape[:2]

    x_start = max(0, X_START)
    x_end = min(width, X_END)

    roi = image[
        y_start:y_end,
        x_start:x_end,
    ]

    # Convert to grayscale.
    gray = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2GRAY,
    )

    # Dark pixels = text.
    dark_pixels = gray < DARK_THRESHOLD

    return bool(np.any(dark_pixels))


def count_rows(src) -> int:
    image = np.array(src)

    image = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2BGR,
    )

    height = image.shape[0]

    count = 0

    while True:
        row_top = (
            FIRST_ROW_TOP
            + count * ROW_HEIGHT
        )

        if row_top >= height:
            break

        if not _row_has_content(
            image,
            row_top,
        ):
            break

        count += 1

    return count