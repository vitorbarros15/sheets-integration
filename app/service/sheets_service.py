import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.models.sheet_models import SheetInput

def get_sheet(sheet_name: str):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials/sheets-integration-467001-cdd295836ffa.json", scope
    )
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

def append_row(sheet, data: SheetInput):
    line_new = [data.name, data.serie, data.initial_weight, data.date]
    sheet.append_row(line_new)
