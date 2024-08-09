import json
from logging import getLogger

from hygeia_ai.service_plan_2 import generate_plan
from linebot.v3.messaging import (
    FlexMessage,
    PushMessageRequest,
    ReplyMessageRequest,
    ShowLoadingAnimationRequest,
    TextMessage,
)
from linebot.v3.webhooks import PostbackEvent
from sqlmodel import Session

from hygeia import models
from hygeia.botconf import engine, handler, line_bot_api
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
        with Session(engine) as session:
            patients = crud.list_current_user_patients(session, user_id)
            patient_names = [patient.name for patient in patients]

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

        with Session(engine) as session:
            patient = crud.get_current_user_patient(session, user_id, patient_name)
            if patient is None:
                patient = crud.create_patient(session, user_id, patient_name)

            patient_report_objects = crud.list_care_reports(session, user_id, patient.id)
            reports = [json.loads(report.report).get("text") for report in patient_report_objects]

        generated_plan = generate_plan("\n".join(reports))
        if generated_plan is not None:
            if generated_plan.additional_report_request.require_additional_report:
                await line_bot_api.push_message(
                    PushMessageRequest(
                        to=user_id,
                        messages=[
                            TextMessage(
                                text=generated_plan.additional_report_request.question_to_caregiver
                                + "\n\n追加情報の補足は【業務報告】から行ってください。"
                            )
                        ],
                    )
                )
            else:
                await line_bot_api.push_message(
                    PushMessageRequest(
                        to=user_id,
                        messages=[TextMessage(text=f"{generated_plan}")],
                    )
                )
