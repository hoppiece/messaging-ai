from logging import getLogger

from fastapi import APIRouter, HTTPException, Request
from hygeia.aio_webhook_handler import AsyncWebhookHandler
from hygeia.config import settings
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

logger = getLogger("uvicorn.app")


router = APIRouter()
configuration = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = AsyncWebhookHandler(settings.LINE_CHANNEL_SECRET)
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)


@router.post("/webhook")
async def handle_callback(request: Request) -> str:
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body_raw = await request.body()
    body = body_raw.decode()

    logger.info(f"body: {body}")
    try:
        await handler.handle(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
async def message_text(event: MessageEvent) -> None:  # type: ignore
    await line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=event.message.text)],
        )
    )
