import os
from pathlib import Path
import sys
import requests
from src.env import N8N_WEBHOOK_URL

from src.models.order import Order

class N8NClient:
    def __init__(self):
        self.webhook_url = N8N_WEBHOOK_URL
        
    def handleError(self, error: dict | None):
        raise RuntimeError(error)

    def parse_order_image(self, image_path: str | Path) -> Order:
        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Order image not found: {image_path}"
            )

        with image_path.open("rb") as image:
            response = requests.post(
                self.webhook_url,
                files={
                    "image": (
                        image_path.name,
                        image,
                        self._mime_type(image_path),
                    )
                },
                timeout=120,
            )

        response.raise_for_status()

        data = response.json()

        if "order_created_at" not in data:
            self.handleError(data.get("error"))

        return Order.from_json(data)
            
    @staticmethod
    def _mime_type(path: Path) -> str:
        suffix = path.suffix.lower()

        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }

        return mime_types.get(
            suffix,
            "application/octet-stream",
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise RuntimeError(
            "Usage: python -m src.main <image_path>"
        )

    image_path = sys.argv[1]

    n8n = N8NClient()

    result = n8n.parse_order_image(image_path)

    print(result)