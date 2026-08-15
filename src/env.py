import os

from dotenv import load_dotenv
load_dotenv()

N8N_WEBHOOK_URL = (
    f"https://{os.getenv("NN_INSTANCE_NAME")}.app.n8n.cloud/"
    "webhook-test/extract-info"
)
