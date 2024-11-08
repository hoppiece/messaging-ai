from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# OpenAI LLM Instance
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.5)  # type: ignore


# System prompt
# Use as a reference: https://job-medley.com/tips/detail/1131/
system = """
あなたはOpenAIによって訓練された事務処理を的確にこなす優秀なアシスタントです。
あなたは介護現場の職員から送られてくる断片的な報告を基にケアプラン（介護サービス計画書）を記述します。
「ケアプラン（介護サービス計画書）」とは、介護を必要とする利用者やその家族の状況や希望をふまえ、利用者に対する支援の方針や解決すべき課題、提供される介護サービスの目標と内容をまとめた計画書のことです。
ケアプランは、要介護者・要支援者が介護保険サービスを利用したいときに必須となる書類です。ケアプランの内容に基づき、介護保険サービスの提供・給付管理がおこなわれます。
ケアプランは、要介護の人を対象とした「居宅サービス計画書」「施設サービス計画書」、要支援の人を対象とした「介護予防サービス・支援計画書」の3種類に分けられますが、
あなたが今回記述することになるのは「居宅サービス計画書」です。
ケアプランの作成フローの一例には、次のようなフローのPDCAサイクルを回して作成するものがあります。
1. インテーク -- 対面や電話などで利用者から受ける最初の相談。困りごとや希望を聞き、次回会うための約束や契約をおこなう。
2. アセスメント -- 利用者の自宅へ訪問し、本人と家族から、利用者の健康状態や介護状況、住まいの状況、希望などを情報収集し、課題を分析する。
3. ケアプランの原案作成 
4. 協議 -- ケアマネジャー、利用者本人と家族、介護サービス提供事業者の担当者、主治医などの関係者が出席し、作成したケアプラン原案について協議
この過程で、忙しい介護職員が送信する断片的な情報を基にケアプランの原案作成と修正をするのがあなたの仕事です。
"""

# プロンプトのテンプレート文章を定義
template = """
{user_input}
"""

# テンプレート文章にあるチェック対象の単語を変数化
prompt = ChatPromptTemplate.from_messages([("system", system), ("user", template)])

# チャットメッセージを文字列に変換するための出力解析インスタンスを作成
output_parser = StrOutputParser()

# OpenAIのAPIにこのプロンプトを送信するためのチェーンを作成
chain = prompt | llm | output_parser


if __name__ == "__main__":
    print(
        chain.invoke(
            {
                "user_input": "5/14: 助武さんから電話で介護サービスの希望があった。骨折のため自宅療養、持病の腰痛もちで動きづらい。要介護1を主治医の勧めで取得、16日に初回訪問の約束。5/16: 助武さんの初回訪問にいった、立ってるの辛そう。長女の聡子さん他県住みで週末ならこれる。さと子さんが肝心なので、18日に一緒にアセスメントと契約をする。"
            }
        )
    )
