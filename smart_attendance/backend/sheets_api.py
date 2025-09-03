from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = '1zW_QB2iGEsLBfJyI0P7EN4Gho_VBA25XpNjAzICScn0'

def get_service():
    creds = Credentials.from_service_account_file(
        os.path.join(os.path.dirname(__file__), 'credentials.json'),
        scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=creds)
    return service

def mark_attendance(roll_numbers, subject):
    service = get_service()
    sheet = service.spreadsheets()
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    values = [[roll, date_str, "Present"] for roll in roll_numbers]
    body = {
        'values': values
    }

    range_name = "Attendance!A1"  # Valid range for append
    try:
        result = sheet.values().append(
            spreadsheetId=SHEET_ID,
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        print(f"[INFO] Attendance for {subject} marked. {result.get('updates').get('updatedCells')} cells updated.")
    except Exception as e:
        print(f"[ERROR] Could not mark attendance for {subject}: {e}")

def get_attendance_for_student(roll_number):
    service = get_service()
    sheet = service.spreadsheets()

    result = sheet.values().get(
        spreadsheetId=SHEET_ID,
        range='Attendance!A1:C1000'  
    ).execute()

    values = result.get('values', [])
    student_records = [row for row in values if row[0] == roll_number]

    return student_records
