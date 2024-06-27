from typing import Any

from botocore.exceptions import ClientError
from hygeia import models


def get_item(table: Any, user_id: str) -> dict | None:
    try:
        response = table.get_item(Key={"user_id": user_id})
    except ClientError as e:
        raise e
    else:
        return response.get("Item")  # type: ignore[no-any-return]


def create_user(table: Any, user_id: str) -> dict:
    response = table.get_item(Key={"user_id": user_id})
    if response.get("Item"):
        return response.get("Item")  # type: ignore[no-any-return]
    else:
        response = table.put_item(Item=models.User(user_id=user_id).model_dump())
        return response  # type: ignore[no-any-return]


def delete_user(table: Any, user_id: str) -> None:
    user = get_item(table=table, user_id=user_id)
    if user is None:
        return None

    table.delete_item(Key={"user_id": user_id})


def insert_patient_report(table: Any, user_id: str, report: models.PatientReport) -> dict:
    response = table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET patient_reports = list_append(patient_reports, :val)",
        ExpressionAttributeValues={":val": [report.model_dump()]},
        ReturnValues="UPDATED_NEW",
    )
    return response  # type: ignore[no-any-return]


def get_patient_names(table: Any, user_id: str) -> list[str]:
    item = get_item(table, user_id)
    if item is None:
        return []
    user = models.User(**item)
    patient_names = set()
    for report in user.patient_reports:
        patient_names.add(report.patient_name)
    return list(patient_names)


def rename_patient(table: Any, user_id: str, current_name: str, new_name: str) -> dict | None:
    user_data = get_item(table, user_id)
    if user_data is None:
        return None

    # patient_reportsリストを取得
    patient_reports = user_data.get("patient_reports", [])

    # 指定されたcurrent_nameを持つレポートの名前をnew_nameに更新
    updated_reports = [
        {**report, "patient_name": new_name} if report["patient_name"] == current_name else report
        for report in patient_reports
    ]

    # 更新されたレポートでアイテムをアップデート
    update_response = table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="set patient_reports = :r",
        ExpressionAttributeValues={":r": updated_reports},
        ReturnValues="UPDATED_NEW",
    )
    return update_response  # type: ignore[no-any-return]


def get_user_state(table: Any, user_id: str) -> models.UserState | None:
    item = get_item(table, user_id)
    if item is None:
        return None
    user = models.User(**item)
    return user.current_state


def set_user_state(table: Any, user_id: str, state: models.UserState) -> dict:
    response = table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET current_state = :val1",
        ExpressionAttributeValues={":val1": state.value},
    )
    return response  # type: ignore[no-any-return]


def set_default_patient(table: Any, user_id: str, patient_name: str) -> dict:
    response = table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET default_patient = :val1",
        ExpressionAttributeValues={":val1": patient_name},
    )
    return response  # type: ignore[no-any-return]


def get_patient_reports(table: Any, user_id: str, patient_name: str) -> list[models.PatientReport]:
    item = get_item(table, user_id)
    if item is None:
        return []
    user = models.User(**item)
    return [report for report in user.patient_reports if report.patient_name == patient_name]
