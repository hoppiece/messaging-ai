import datetime
from pathlib import Path

import httpx
from linebot.v3.messaging.models import (
    MessageAction,
    PostbackAction,
    RichMenuArea,
    RichMenuBounds,
    RichMenuRequest,
    RichMenuSize,
)
from zoneinfo import ZoneInfo

from hygeia import models
from hygeia.botconf import line_bot_api, line_bot_api_blob
from hygeia.config import settings


def generate_fillin_text(patient_name: str = "") -> str:
    report_fillin_text = f"""\
---
【業務報告】
日時: {datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date()}
患者名: {patient_name}
---

"""
    return report_fillin_text


def generate_rich_menu() -> RichMenuRequest:  # type: ignore[no-any-unimported]
    rich_menu_to_create = RichMenuRequest(
        size=RichMenuSize(width=2500, height=843),
        selected=False,
        name="Main menu",
        chat_bar_text="メニューを開く",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=8, y=0, width=810, height=835),
                action=PostbackAction(
                    label="push_patient_report",
                    data=models.PostBackActionData(
                        action_id=models.BotAction.open_report_editor
                    ).model_dump_json(),
                    inputOption="openKeyboard",
                    fillInText=generate_fillin_text(),
                ),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=848, y=0, width=810, height=835),
                action=PostbackAction(
                    label="request_care_plan",
                    data=models.PostBackActionData(
                        action_id=models.BotAction.request_document
                    ).model_dump_json(),
                    displayText="ケアプランを作成",
                ),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1690, y=0, width=810, height=835),
                action=MessageAction(label="label3", text="設定"),
            ),
        ],
    )
    return rich_menu_to_create


async def delete_rich_menu() -> None:
    rich_menu_list = await line_bot_api.get_rich_menu_list()
    for rich_menu in rich_menu_list.richmenus:
        await line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)


async def set_rich_menu() -> str:
    rich_menu_id_response = await line_bot_api.create_rich_menu(
        rich_menu_request=generate_rich_menu()
    )
    rich_menu_id: str = rich_menu_id_response.rich_menu_id

    path = Path(__file__).parent / "data/rich_menu.png"

    # The SDK may broken. The above code does not work...
    # with open(path, "rb") as f:
    #     image_data = f.read()
    #     await line_bot_api_blob.set_rich_menu_image(rich_menu_id=rich_menu_id, body=image_data)

    await _upload_rich_menu_image(
        rich_menu_id=rich_menu_id,
        image_path=path,
        channel_access_token=settings.LINE_CHANNEL_ACCESS_TOKEN,
        content_type="image/png",
    )

    # 上記のRichMenuをデフォルトに設定する
    await line_bot_api.set_default_rich_menu(rich_menu_id)
    return rich_menu_id


async def _upload_rich_menu_image(
    rich_menu_id: str,
    image_path: Path | str,
    channel_access_token: str,
    content_type: str = "image/png",
) -> httpx.Response:
    url = f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content"
    headers = {
        "Authorization": f"Bearer {channel_access_token}",
        "Content-Type": content_type,
    }

    async with httpx.AsyncClient() as client:
        with open(image_path, "rb") as file:
            image_data = file.read()
        response = await client.post(url, headers=headers, content=image_data)
        return response
