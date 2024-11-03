import os
from pathlib import Path

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from hygeia_ai.service_plan_2 import CarePlan

TEMPLATE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1aBtu5XH78VI1SJimfOwhSbRRfBV6rm_huV0JaGtQzNc/edit?usp=sharing"


# Load your service account credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    Path(__file__).parent / ".key.json", scope
)
client = gspread.authorize(creds)


def map_sheet(wks: gspread.Worksheet, careplan_obj: CarePlan) -> gspread.Worksheet:
    cell_生活上の課題 = ["A10", "A18", "A26", "A34", "A42", "A50", "A58", "A66"]
    # cell生活上の課題 = ["A10:B17", "A18:B25", "A26:B33", "A34:B41", "A42:B49", "A50:B57", "A58:B65", "A66:B73"]
    cell_長期目標 = ["C10", "C18", "C26", "C34", "C42", "C50", "C58", "C66"]
    cell_長期目標に向けた期限 = ["D10", "D18", "D26", "D34", "D42", "D50", "D58", "D66"]

    cell_短期目標 = ["E10", "E14", "E18", "E22", "E26", "E30", "E34", "E38"]
    cell_短期目標に向けた期限 = ["G10", "G14", "G18", "G22", "G26", "G30", "G34", "G38"]
    cell_サービス内容 = ["H10", "H15", "H18", "H23", "H26", "H31", "H34", "H39"]
    cell_サポート頻度 = ["L10", "L15", "L18", "L23", "L26", "L31", "L34", "L39"]

    insert_count = 0
    for issue_idx, issue in enumerate(careplan_obj.care_plan):
        生活上の課題 = issue.patient_problem
        長期目標 = issue.long_term_goal
        長期目標に向けた期限 = issue.due_date_for_long_term_goal
        # insert patient_problem to A10:B17
        wks.update(cell_生活上の課題[issue_idx], [[生活上の課題]])
        wks.update(cell_長期目標[issue_idx], [[長期目標]])
        wks.update(cell_長期目標に向けた期限[issue_idx], [[長期目標に向けた期限]])
        insert_count = 0
        for plan_idx, plan in enumerate(issue.plans):
            短期目標 = plan.short_term_goal
            短期目標に向けた期限 = plan.due_date_for_short_term_goal
            サービス内容 = plan.action
            サポート頻度 = plan.frequency
            wks.update(cell_短期目標[insert_count], [[短期目標]])
            wks.update(cell_短期目標に向けた期限[insert_count], [[短期目標に向けた期限]])
            wks.update(cell_サービス内容[insert_count], [[サービス内容]])
            wks.update(cell_サポート頻度[insert_count], [[サポート頻度]])
            insert_count += 1

    return wks


def export_sheet(
    sheet_name: str,
    care_plan_obj: CarePlan,
    template_sheet_id: str = TEMPLATE_SHEET_URL,
    worksheet_name: str = "居宅サービス計画書（２）",
) -> str:
    # Copy the template sheet
    template_spreadsheet = client.open_by_url(template_sheet_id)

    new_spreadsheet = client.copy(template_spreadsheet.id, title=sheet_name)

    # Create a new Google Spreadsheet
    # sheet = client.create(sheet_name)
    new_spreadsheet.share(os.getenv("email_address", ""), perm_type="user", role="writer")
    worksheet = new_spreadsheet.get_worksheet(0)

    # # Prepare and write the header row
    # headers = [
    #     "生活上の課題",
    #     "長期目標",
    #     "長期目標に向けた期限",
    #     "短期目標",
    #     "短期目標に向けた期限",
    #     "サービス内容",
    #     "サポート頻度",
    # ]
    # worksheet.append_row(headers)

    # Prepare data for each issue and plan in the care plan
    # for issue in care_plan_obj.care_plan:
    #     for plan in issue.plans:
    #         data = [
    #             issue.patient_problem,
    #             issue.long_term_goal,
    #             issue.due_date_for_long_term_goal,
    #             plan.short_term_goal,
    #             plan.due_date_for_short_term_goal,
    #             plan.action,
    #             plan.frequency,
    #         ]

    #         # Append data to the worksheet row by row
    #         worksheet.append_row(data)

    worksheet = map_sheet(worksheet, care_plan_obj)

    return new_spreadsheet.url
