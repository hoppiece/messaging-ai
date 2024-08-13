import os
import sys

import httpx
from dotenv import load_dotenv
from logzero import logger

load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")


def get_ngrok_url() -> str | None:
    # Local ngrok API endpoint
    url = "http://127.0.0.1:4040/api/tunnels"

    response = httpx.get(url)
    if response.status_code == 200:
        tunnels = response.json().get("tunnels", [])
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel.get("public_url")  # type: ignore
    return None


def update_webhook_url(webhook_url: str) -> httpx.Response:
    url = "https://api.line.me/v2/bot/channel/webhook/endpoint"
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {"endpoint": webhook_url}
    response = httpx.put(url, headers=headers, json=data)
    return response


def verify_webhook(webhook_url: str) -> httpx.Response:
    url = "https://api.line.me/v2/bot/channel/webhook/test"
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {"endpoint": webhook_url}
    response = httpx.post(url, headers=headers, json=data)
    logger.info(f"Status: {response.status_code}, {response.json()}")
    return response


if __name__ == "__main__":
    ngrok_published_url = get_ngrok_url()
    if ngrok_published_url is None:
        logger.error("Cannot fetch published url.")
        sys.exit(1)

    webhook_url = f"{ngrok_published_url}/webhook"
    logger.info(f"Public webhook endpoint: {webhook_url}")
    update_webhook_url(webhook_url)
    response = verify_webhook(webhook_url)
    if not response.json().get("success"):
        logger.error("Failed to update webhook URL")
        sys.exit(1)
