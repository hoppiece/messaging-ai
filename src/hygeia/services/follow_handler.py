from logging import getLogger

from linebot.v3.messaging import (
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import FollowEvent

from hygeia.botconf import handler, hygeia_user, line_bot_api
from hygeia.repositories import crud

logger = getLogger("uvicorn.app")


@handler.add(FollowEvent)
async def handle_follow(event: FollowEvent) -> None:  # type: ignore[no-any-unimported]
    logger.info(f"FollowEvent. user_id: {event.source.user_id}")

    user_profile = await line_bot_api.get_profile(event.source.user_id)
    welcome_message_1 = f"{user_profile.display_name}さん、友達登録ありがとうございます。"
    welcome_message_2 = f"{user_profile.display_name}さんのケアプラン作成のアシスタントをします。"
    await line_bot_api.reply_message(
        ReplyMessageRequest(
            replyToken=event.reply_token,
            messages=[
                TextMessage(text=welcome_message_1),
                TextMessage(text=welcome_message_2),
            ],
        )
    )
    user_id: str = event.source.user_id
    crud.create_user(hygeia_user, user_id)
