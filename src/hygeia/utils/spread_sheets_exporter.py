import os
from pathlib import Path

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from hygeia_ai.service_plan_2 import CarePlan

# Load your service account credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    Path(__file__).parent / ".key.json", scope
)
client = gspread.authorize(creds)


def export_sheet(sheet_name: str, care_plan_obj: CarePlan) -> str:
    # Create a new Google Spreadsheet
    sheet = client.create(sheet_name)
    sheet.share(os.getenv("email_address", ""), perm_type="user", role="writer")

    # Select the first sheet
    worksheet = sheet.get_worksheet(0)

    # Prepare and write the header row
    headers = [
        "生活上の課題",
        "長期目標",
        "長期目標に向けた期限",
        "短期目標",
        "短期目標に向けた期限",
        "サービス内容",
        "サポート頻度",
    ]
    worksheet.append_row(headers)

    # Prepare data for each issue and plan in the care plan
    for issue in care_plan_obj.care_plan:
        for plan in issue.plans:
            data = [
                issue.patient_problem,
                issue.long_term_goal,
                issue.due_date_for_long_term_goal,
                plan.short_term_goal,
                plan.due_date_for_short_term_goal,
                plan.action,
                plan.frequency,
            ]

            # Append data to the worksheet row by row
            worksheet.append_row(data)

    return sheet.url
