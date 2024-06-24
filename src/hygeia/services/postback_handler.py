from linebot.v3.webhooks import PostbackEvent

from hygeia.botconf import handler, line_bot_api


@handler.add(PostbackEvent)
async def handle_postback(event: PostbackEvent) -> None:  # type: ignore[no-any-unimported]
    pass
