from hygeia.botconf import handler, line_bot_api
from linebot.v3.messaging import (
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent


@handler.add(MessageEvent, message=TextMessageContent)
async def message_text(event: MessageEvent) -> None:  # type: ignore[no-any-unimported]
    await line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=event.message.text)],
        )
    )
