import datetime
import pytz
from googleapiclient.discovery import build
from google.oauth2 import service_account

# --- Google Sheets Setup ---
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Your credentials file
SPREADSHEET_ID = 'your_spreadsheet_id'
RANGE = 'Timetable!A1:J6'  # Covers full timetable

# --- Set timezone ---
IST = pytz.timezone('Asia/Kolkata')

def get_current_subject():
    # Auth
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Read data
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
    values = result.get('values', [])

    if not values:
        print("No data found.")
        return None

    # Get current time
    now = datetime.datetime.now(IST)
    current_day = now.strftime("%A").upper()  # e.g., 'MONDAY'
    current_time = now.time()

    # Map day to row number
    day_row_map = {
        'MONDAY': 1,
        'TUESDAY': 2,
        'WEDNESDAY': 3,
        'THURSDAY': 4,
        'FRIDAY': 5
    }

    if current_day not in day_row_map:
        return None  # Weekend or not found

    row_idx = day_row_map[current_day]
    time_slots = values[0][1:]  # Skip header (first column)
    subjects = values[row_idx][1:]  # Skip day name

    # Match current time with time slot
    for i, slot in enumerate(time_slots):
        try:
            start_str, end_str = slot.split('-')
            start = datetime.datetime.strptime(start_str.strip(), "%I:%M").time()
            end = datetime.datetime.strptime(end_str.strip(), "%I:%M").time()
        except ValueError:
            continue  # Skip if slot is not proper

        if start <= current_time <= end:
            return subjects[i]

    return None  # No subject found
