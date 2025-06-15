# main.py
import schedule
import time
from backend.attendance_manager import run_attendance_check

schedule.every(10).minutes.do(run_attendance_check)

print("Attendance system running...")

while True:
    schedule.run_pending()
    time.sleep(1)
