from backend.sheets_api import get_attendance_for_student

# Replace with a real roll number you used in test_write.py
roll_number = "CS101"
records = get_attendance_for_student(roll_number)

for record in records:
    print(f"Roll: {record[0]}, Date: {record[1]}, Status: {record[2]}")
