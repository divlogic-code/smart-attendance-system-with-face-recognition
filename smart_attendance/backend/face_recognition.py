# backend/face_recognition.py
import face_recognition
import os

def load_known_faces(folder):
    known_encodings = {}
    for filename in os.listdir(folder):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue  # Skip non-image files
        path = os.path.join(folder, filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            roll_number = os.path.splitext(filename)[0]
            known_encodings[roll_number] = encodings[0]
    return known_encodings

def recognize_faces(image, known_faces):
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    present_students = []
    for face_encoding in face_encodings:
        for roll, known_encoding in known_faces.items():
            match = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=0.5)
            if match[0]:
                present_students.append(roll)
                break
    return present_students
