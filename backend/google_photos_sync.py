# backend/google_photos_sync.py
import os
import shutil

def sync_student_images():
    # Simulate sync (replace with real API later)
    source = "simulated_google_photos/"
    target = "data/student_images/"
    if os.path.exists(target):
        shutil.rmtree(target)
    shutil.copytree(source, target)
    print("Student images synced.")
