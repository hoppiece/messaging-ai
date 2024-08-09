from typing import Annotated, Generator

from fastapi import Depends
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    AsyncMessagingApiBlob,
    Configuration,
)
from sqlmodel import Session, SQLModel, create_engine

from hygeia.config import settings

from .utils.aio_webhook_handler import AsyncWebhookHandler

handler = AsyncWebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = AsyncMessagingApi(
    AsyncApiClient(Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN))
)
line_bot_api_blob = AsyncMessagingApiBlob(
    AsyncApiClient(Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN))
)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
