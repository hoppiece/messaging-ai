from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, field_serializer


class HealthCheckResponse(BaseModel):
    status: str = "OK"


class RichmenuCreateResponse(BaseModel):
    rich_menu_id: str


class PatientReport(BaseModel):
    patient_name: str
    report: str


class UserState(Enum):
    default = Decimal(0)

    # 名無しのレポートに対して患者名を入力
    input_patient_name = Decimal(1)

    # ユーザーがpatient_nameを選択中
    select_patient_name = Decimal(10)


class User(BaseModel):
    user_id: str
    patient_reports: list[PatientReport] = Field(default_factory=list)
    current_state: UserState = Field(default=UserState.default)
    default_patient: str = Field(default="")

    class Config:
        use_enum_values = True

    @field_serializer("current_state")
    def serialize_dt(self, current_state: UserState) -> Decimal:
        return current_state.value


class BotAction(Enum):
    # 業務報告のリッチメニューを開く
    open_report_editor = 1

    # ケアプランレポートを要求するリッチメニューボタンをユーザが押す
    request_document = 2

    # Flexメッセージの患者を選択
    select_patient_name = 3


class PostBackActionData(BaseModel):
    action_id: BotAction

    class Config:
        use_enum_values = True


class SelectName(PostBackActionData):
    patient_name: str
