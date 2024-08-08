from openai import OpenAI
from pydantic import BaseModel

from hygeia_ai.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class AdditionalReportRequest(BaseModel):
    require_additional_report: bool
    question_to_caregiver: str


class AssistantPlanAction(BaseModel):
    short_term_goal: str
    due_date_for_short_term_goal: str
    action: str
    frequency: str


class Issue(BaseModel):
    patient_problem: str
    long_term_goal: str
    due_date_for_long_term_goal: str
    plans: list[AssistantPlanAction]


class CarePlan(BaseModel):
    additional_report_request: AdditionalReportRequest
    care_plan: list[Issue]


def generate_plan(reports: str) -> CarePlan | None:
    model = "gpt-4o-2024-08-06"

    system = """
あなたは介護に関する事務処理を的確にこなすアシスタントです。
あなたは介護現場の職員から送られてくる断片的な報告を基にケアプラン（介護サービス計画書）の記述を支援します。
「ケアプラン（介護サービス計画書）」は、介護を必要とする利用者やその家族の状況や希望をふまえ、利用者に対する支援の方針や解決すべき課題、提供される介護サービスの目標と内容をまとめた計画書のことです。
ケアプランは、要介護者・要支援者が介護保険サービスを利用したいときに必須となる書類です。ケアプランの内容に基づき、介護保険サービスの提供・給付管理がおこなわれます。

あなたが今回作成するのは「居宅サービス計画書(2)」です。生活上の課題を発見し、それに対する目標・期間を設定し、必要な支援内容を取りまとめてください。
例えば、「歩行時にふらつくことがあるが、家事ができるようになりたい。」という課題やニーズを発見して, 長期目標を「家事（掃除・洗濯・買い物）が自分でできていること。」と設定し期日を考えます。
次に、その目標を達成するために短期目標と期間を定めてください。例えば、「自宅内の掃除が自分でできていること」、「洗濯と調理が自分でできてること
」などです。短期目標に対して支援内容と頻度を設定してください。支援内容は「1. 一緒に掃除と洗濯を行う 2. 掃除は、リビングと居室行う 3.洗濯は、洗濯物を居室内に干す」などを、頻度は「週2回」「月2回」などを設定します。

介護士は業務報告としてチャットをあなたに送信するので、それを基にケアプランを作成してください。
また、必要な情報が不足している場合は介護士に追加の業務報告を依頼することができます。
また、むやみに質問をするのではなく、報告内容をよく読み、必要な情報を抽出して介護されている人が何に困っているのかを類推しながらケアプランを作成してください。
"""

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": reports},
    ]

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=messages,
        response_format=CarePlan,
    )

    return completion.choices[0].message.parsed


if __name__ == "__main__":
    print(
        generate_plan(
            "5/14: 助武さんから電話で介護サービスの希望があった。骨折のため自宅療養、持病の腰痛もちで動きづらい。要介護1を主治医の勧めで取得、16日に初回訪問の約束。5/16: 助武さんの初回訪問にいった、立ってるの辛そう。長女の聡子さん他県住みで週末ならこれる。さと子さんが肝心なので、18日に一緒にアセスメントと契約をする。"
        )
    )
