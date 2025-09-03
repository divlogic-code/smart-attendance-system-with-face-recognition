# backend/camera.py
import cv2
import time
import os
from datetime import datetime

def take_snapshot():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"data/snapshots/{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Snapshot saved: {filename}")
    cam.release()
