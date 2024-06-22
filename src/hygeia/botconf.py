from linebot.v3.messaging import (
    ApiClient,
    AsyncApiClient,
    AsyncMessagingApi,
    AsyncMessagingApiBlob,
    Configuration,
)

from hygeia.config import settings

from .utils.aio_webhook_handler import AsyncWebhookHandler

handler = AsyncWebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = AsyncMessagingApi(
    AsyncApiClient(Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN))
)
line_bot_api_blob = AsyncMessagingApiBlob(
    AsyncApiClient(Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN))
)
