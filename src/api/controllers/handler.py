import os
from typing import Any

from api import models
from api.config import settings
from fastapi import APIRouter, HTTPException, Request
from linebot.v3 import WebhookHandler  # type: ignore
from linebot.v3.exceptions import InvalidSignatureError  # type: ignore
from linebot.v3.messaging import (  # type: ignore
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhook import WebhookParser  # type: ignore
from linebot.v3.webhooks import MessageEvent, TextMessageContent  # type: ignore

router = APIRouter()
configuration = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@router.get("/healthz", response_model=models.HealthCheckResponse)
async def get_health() -> models.HealthCheckResponse:
    return models.HealthCheckResponse()


@router.post("/")
async def handle_callback(request: Request) -> str:
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body_raw = await request.body()
    body = body_raw.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue

        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token, messages=[TextMessage(text=event.message.text)]
            )
        )

    return "OK"
