import boto3
from linebot.v3.messaging import (
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

dynamodb = boto3.resource(
    "dynamodb",
    region_name=settings.AWS_DEFAULT_REGION,
    endpoint_url=settings.DYNAMODB_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

hygeia_user = dynamodb.Table(settings.TABLE_NAME)
