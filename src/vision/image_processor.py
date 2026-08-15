import cv2
import numpy as np

from src.vision.utils import get_dpi_scale

FIRST_ROW_TOP = 57
ROW_HEIGHT = 20

X_START = 0
X_END = 630

DARK_THRESHOLD = 120


def _row_has_content(
    image: np.ndarray,
    row_top: int,
) -> bool:
    dpi_scale = get_dpi_scale()

    def scale(value: int) -> int:
        return round(value * dpi_scale)

    y_start = scale(row_top + 3)
    y_end = scale(row_top + ROW_HEIGHT - 3)

    height, width = image.shape[:2]

    x_start = max(0, scale(X_START))
    x_end = min(width, scale(X_END))

    # Make sure coordinates are valid.
    if y_start >= height or y_start >= y_end or x_start >= x_end:
        return False

    y_end = min(y_end, height)

    roi = image[
        y_start:y_end,
        x_start:x_end,
    ]

    gray = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2GRAY,
    )

    dark_pixels = gray < DARK_THRESHOLD

    return bool(np.any(dark_pixels))


def count_rows(src) -> int:
    image = np.array(src)

    image = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2BGR,
    )

    height = image.shape[0]

    dpi_scale = get_dpi_scale()

    count = 0

    while True:
        row_top = FIRST_ROW_TOP + count * ROW_HEIGHT

        # Compare scaled coordinate against actual image size.
        if round(row_top * dpi_scale) >= height:
            break

        if not _row_has_content(
            image,
            row_top,
        ):
            break

        count += 1

    return count