from logging import getLogger

from hygeia_ai.main import chain
from linebot.v3.messaging import (
    FlexMessage,
    PushMessageRequest,
    ReplyMessageRequest,
    ShowLoadingAnimationRequest,
    TextMessage,
)
from linebot.v3.webhooks import PostbackEvent

from hygeia import models
from hygeia.botconf import handler, hygeia_user, line_bot_api
from hygeia.repositories import crud
from hygeia.views.patient_name_selector import generate_patient_names_flex_bubble

logger = getLogger("uvicorn.app")


@handler.add(PostbackEvent)
async def handle_postback(event: PostbackEvent) -> None:  # type: ignore[no-any-unimported]
    logger.info(f"PostbackEvent. user_id: {event.source.user_id}")

    # Get chat_id
    try:
        chat_id = event.source.group_id
    except AttributeError:
        try:
            chat_id = event.source.room_id
        except AttributeError:
            chat_id = event.source.user_id
    user_id = event.source.user_id

    data = models.PostBackActionData.model_validate_json(event.postback.data)
    if data.action_id == models.BotAction.request_document.value:
        patient_names = crud.get_patient_names(hygeia_user, user_id)

        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text="誰についての報告書を作成しますか?"),
                    FlexMessage(
                        altText="Select a name",
                        contents=generate_patient_names_flex_bubble(patient_names),
                    ),
                ],
            )
        )

    if data.action_id == models.BotAction.select_patient_name.value:
        patient_name = models.SelectName.model_validate_json(event.postback.data).patient_name
        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text="ケアプラン作成中"),
                ],
            )
        )
        await line_bot_api.show_loading_animation(ShowLoadingAnimationRequest(chatId=chat_id))

        reports: list[str] = [
            report.report
            for report in crud.get_patient_reports(hygeia_user, user_id, patient_name)
        ]
        ai_generated_message = await chain.ainvoke({"user_input", "\n".join(reports)})
        await line_bot_api.push_message(
            PushMessageRequest(to=user_id, messages=[TextMessage(text=ai_generated_message)])
        )
