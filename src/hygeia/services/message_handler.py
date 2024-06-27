import json
from logging import getLogger

from botocore.exceptions import ClientError
from linebot.v3.messaging import (
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from hygeia import models
from hygeia.botconf import handler, hygeia_user, line_bot_api
from hygeia.config import settings
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
                            text=f"患者名を入力する必要があります。もう一度業務報告を作成してください。"
                        ),
                    ],
                )
            )
        else:
            patient_report = models.PatientReport(patient_name=patient_name, report=text)
            crud.insert_patient_report(hygeia_user, user_id, patient_report)
            crud.set_default_patient(hygeia_user, user_id, patient_name)

        """
        if patient_name == "":
            patient_names = crud.get_patient_names(hygeia_user, user_id)
            patient_names.remove("")
            if patient_names:
                canditate_text = f"候補:\n{'\n'.join(patient_names)}"
            else:
                canditate_text = ""
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(
                            text=f"誰についての報告ですか? 名前を送信してください。{canditate_text}"
                        ),
                    ],
                )
            )
            crud.set_user_state(hygeia_user, user_id, models.UserState.input_patient_name)
        """

    if crud.get_user_state(hygeia_user, user_id) == models.UserState.input_patient_name.value:
        crud.set_user_state(hygeia_user, user_id, models.UserState.default)
        new_name = text.strip().replace("様", "").replace("さん", "").strip()
        crud.rename_patient(hygeia_user, user_id, "", new_name)
