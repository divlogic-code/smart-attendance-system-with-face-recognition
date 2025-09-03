import os
import cv2
import face_recognition

def load_known_faces(folder):
    encodings = []
    names = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img = face_recognition.load_image_file(os.path.join(folder, filename))
            encoding = face_recognition.face_encodings(img)
            if encoding:
                encodings.append(encoding[0])
                names.append(filename.split('.')[0])  # Use filename as roll number
    return encodings, names

def recognize_faces(frame, known_encodings, known_names):
    small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = small[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    present = []
    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding)
        if True in matches:
            matched_index = matches.index(True)
            present.append(known_names[matched_index])
    return list(set(present))
