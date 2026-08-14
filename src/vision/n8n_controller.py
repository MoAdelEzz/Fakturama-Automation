from __future__ import annotations

import base64
import io
import json
import os
import re

from PIL import Image
from huggingface_hub import InferenceClient


class RowCounter:
    MODEL = "Qwen/Qwen3-VL-4B-Instruct"

    def __init__(self):
        token = os.getenv("HF_TOKEN")

        if not token:
            raise RuntimeError(
                "HF_TOKEN environment variable is not set"
            )

        self.client = InferenceClient(
            api_key=token,
            provider="featherless-ai"
        )

    @staticmethod
    def _image_to_base64(image: Image.Image) -> str:
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")

        return base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

    def count_rows(self, image: Image.Image) -> int:
        image_base64 = self._image_to_base64(image)

        prompt = """
            You are analyzing a screenshot of a Fakturama table.

            Count ONLY the visible DATA ROWS.

            Rules:
            - Do not count the table header.
            - Do not count toolbars.
            - Do not count the search bar.
            - Do not count borders.
            - Do not count empty rows.
            - Each visible record is exactly one row.
            - Return ONLY valid JSON.

            Required format:
            {
                "row_count": 0
            }
        """

        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": (
                                    "data:image/png;base64,"
                                    f"{image_base64}"
                                )
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )

        print(response)

        if response.choices[0].message.content is None:
            return 0

        raw = response.choices[0].message.content.strip()

        raw = re.sub(
            r"```(?:json)?\s*",
            "",
            raw,
        ).replace("```", "").strip()

        result = json.loads(raw)

        count = result.get("row_count")

        if not isinstance(count, int):
            raise RuntimeError(
                f"Invalid row count returned: {raw}"
            )

        if count < 0:
            raise RuntimeError(
                f"Invalid negative row count: {count}"
            )

        return count