import json

from linebot.v3.messaging import FlexBox, FlexBubble, FlexButton, FlexText, PostbackAction

from hygeia import models


def generate_patient_names_flex_bubble(  # type: ignore [no-any-unimported]
    patient_names: list[str],
) -> FlexBubble:
    container = FlexBubble()
    container.body = FlexBox(layout="vertical", contents=[])

    title = FlexText(text="名前を選択", weight="bold", size="lg")
    container.body.contents.append(title)

    name_list_box_contents = []
    for name in patient_names:
        name_button = FlexButton(
            style="primary",
            margin="md",
            action=PostbackAction(
                label=name,
                data=models.SelectName(
                    action_id=models.BotAction.select_patient_name,
                    patient_name=name,
                ).model_dump_json(),
                displayText=name,
            ),
        )
        name_list_box_contents.append(name_button)

    name_list_box = FlexBox(
        layout="vertical", margin="md", spacing="sm", contents=name_list_box_contents
    )
    container.body.contents.append(name_list_box)

    return container


if __name__ == "__main__":
    flex_bubble = generate_patient_names_flex_bubble(["田中", "佐藤", "井上"])
    print(json.dumps(flex_bubble.to_dict(), indent=True, ensure_ascii=False))
