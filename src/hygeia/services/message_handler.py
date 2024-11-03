import json
from logging import getLogger

from linebot.v3.messaging import ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from sqlmodel import Session

from hygeia.botconf import engine, handler, line_bot_api
from hygeia.repositories import crud

logger = getLogger("uvicorn.app")


@handler.add(MessageEvent, message=TextMessageContent)
async def message_text(event: MessageEvent) -> None:  # type: ignore[no-any-unimported]
    text: str = event.message.text
    user_id = event.source.user_id

    if text.startswith("---\n【業務報告】"):
        lines = text.split("\n")
        try:
            patient_line = [_ for _ in lines if _.startswith("患者名:")][0]
            patient_name = patient_line.replace("患者名:", "").strip()
            patient_name = patient_name.replace("様", "").replace("さん", "").strip()
        except IndexError:
            patient_name = "不明"

        if patient_name == "":
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(
                            text="患者名を入力する必要があります。もう一度業務報告を作成してください。"
                        ),
                    ],
                )
            )
        else:
            with Session(engine) as session:
                patient = crud.get_current_user_patient(session, user_id, patient_name)
                if patient is None:
                    patient = crud.create_patient(session, user_id, patient_name)
                crud.create_care_report(
                    session, user_id, patient.id, json.dumps({"text": text}, ensure_ascii=False)
                )

                caregiver = crud.get_caregiver_by_id(session, user_id)
                if caregiver and caregiver.default_patient_id != patient.id:
                    # TODO update filled in patient name on the rich menu
                    crud.set_default_patient(session, user_id, patient.id)
