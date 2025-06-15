import cv2
import time
import datetime
import os
from backend.face_recognition import recognize_faces
from backend.sheets_api import mark_attendance

# Adjust this interval in seconds (10 mins = 600 seconds)
INTERVAL = 600

# Initialize camera (0 = default webcam)
cap = cv2.VideoCapture(0)

# Main loop to run every 10 minutes
try:
    while True:
        print("[INFO] Taking snapshot...")

        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame")
            time.sleep(INTERVAL)
            continue

        # Optional: Save frame with timestamp for debugging/log
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = f"snapshot_{timestamp}.jpg"
        cv2.imwrite(img_path, frame)

        # ✅ Recognize faces in the snapshot
        print("[INFO] Recognizing faces...")
        recognized_rolls = recognize_faces(frame)  # expects a list of roll numbers

        if recognized_rolls:
            print(f"[INFO] Recognized: {recognized_rolls}")
            mark_attendance(recognized_rolls)
        else:
            print("[INFO] No known faces recognized.")

        # Optional: Delete the snapshot after processing
        os.remove(img_path)

        print(f"[WAIT] Sleeping for {INTERVAL / 60:.0f} minutes...")
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("[EXIT] Snapshot automation stopped by user.")
finally:
    cap.release()
