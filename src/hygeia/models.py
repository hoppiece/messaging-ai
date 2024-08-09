import datetime
from decimal import Decimal
from enum import Enum

import sqlmodel
from pydantic import BaseModel, Field, field_serializer


class HealthCheckResponse(BaseModel):
    status: str = "OK"


class RichmenuCreateResponse(BaseModel):
    rich_menu_id: str


class UserState(Enum):
    default = Decimal(0)

    # 名無しのレポートに対して患者名を入力
    input_patient_name = Decimal(1)

    # ユーザーがpatient_nameを選択中
    select_patient_name = Decimal(10)


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


class Caregiver(sqlmodel.SQLModel, table=True):
    class Config:
        use_enum_values = True

    __table_args__ = {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_0900_ai_ci"}
    id: str = sqlmodel.Field(primary_key=True)  # line_user_id
    name: str
    current_state: UserState = sqlmodel.Field(default=UserState.default)
    default_patient_id: int = sqlmodel.Field(default=None, foreign_key="patient.id", nullable=True)


class Patient(sqlmodel.SQLModel, table=True):
    __table_args__ = {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_0900_ai_ci"}
    id: int = sqlmodel.Field(
        default=None,
        primary_key=True,
    )
    name: str = sqlmodel.Field(nullable=False)
    caregiver_id: str = sqlmodel.Field(foreign_key="caregiver.id")


class CareReport(sqlmodel.SQLModel, table=True):
    __table_args__ = {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_0900_ai_ci"}
    id: int = sqlmodel.Field(default=None, primary_key=True)
    created_at: datetime.datetime = sqlmodel.Field(default_factory=datetime.datetime.now)
    caregiver_id: str = sqlmodel.Field(foreign_key="caregiver.id")
    patient_id: int = sqlmodel.Field(foreign_key="patient.id")
    report: str = sqlmodel.Field()  # json strings
