# backend/attendance_manager.py
from backend.camera import take_snapshot
from backend.face_recognition import load_known_faces, recognize_faces
from backend.sheets_api import mark_attendance
import os

def run_attendance_check():
    take_snapshot()
    known_faces = load_known_faces("data/student_images")
    latest_snapshot = sorted(os.listdir("data/snapshots"))[-1]
    present_students = recognize_faces(f"data/snapshots/{latest_snapshot}", known_faces)
    print("Recognized students:", present_students)
    mark_attendance(present_students)
