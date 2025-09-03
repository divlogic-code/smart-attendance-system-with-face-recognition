import cv2
import time
import datetime
import os
from backend.face_recognition import load_known_faces, recognize_faces
from backend.sheets_api import mark_attendance
from backend.timetable import get_current_subject
import logging

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/attendance_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

INTERVAL = 600  # 10 minutes
FACE_FOLDER = 'data/faces'
TOTAL_STUDENTS = 60
ATTENDANCE_THRESHOLD_PERCENT = 30

# Load known student faces once at start
print("[INIT] Loading known faces...")
known_faces = load_known_faces(FACE_FOLDER)

cap = cv2.VideoCapture(0)
print("[INIT] Camera initialized. Starting snapshot loop...")

try:
    while True:
        print("\n[INFO] Taking snapshot...")
        logging.info("Taking snapshot...")

        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to capture frame from camera.")
            logging.error("Failed to capture frame from camera.")
            time.sleep(INTERVAL)
            continue

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = f"snapshot_{timestamp}.jpg"
        cv2.imwrite(img_path, frame)

        print("[INFO] Running face recognition...")
        logging.info("Running face recognition...")
        recognized_rolls = recognize_faces(frame, known_faces)

        if recognized_rolls:
            present_count = len(recognized_rolls)
            attendance_percent = (present_count / TOTAL_STUDENTS) * 100

            print(f"[INFO] Recognized Roll Numbers: {recognized_rolls}")
            logging.info(f"Recognized Roll Numbers: {recognized_rolls}")

            if attendance_percent < ATTENDANCE_THRESHOLD_PERCENT:
                warning_msg = f"Low attendance alert: Only {attendance_percent:.2f}% present."
                print(f"[ALERT] {warning_msg}")
                logging.warning(warning_msg)

            subject = get_current_subject()
            if subject:
                print(f"[INFO] Current Subject: {subject}")
                logging.info(f"Current Subject: {subject}")
                mark_attendance(recognized_rolls, subject)
            else:
                print("[INFO] No class scheduled currently. Skipping attendance marking.")
                logging.info("No class scheduled currently. Skipping attendance marking.")
        else:
            print("[INFO] No known faces recognized.")
            logging.info("No known faces recognized.")

        os.remove(img_path)
        print(f"[WAIT] Sleeping for {INTERVAL // 60} minutes...\n")
        logging.info(f"Sleeping for {INTERVAL // 60} minutes...")
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("[EXIT] Snapshot automation manually stopped by user.")
    logging.info("Snapshot automation manually stopped by user.")
finally:
    cap.release()
    print("[CLEANUP] Camera released. Program terminated.")
    logging.info("Camera released. Program terminated.")
