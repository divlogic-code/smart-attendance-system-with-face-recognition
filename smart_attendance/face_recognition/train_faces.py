import os
import pickle
from face_recognition import encode_face

def train_and_save_encodings():
    face_encodings = {}
    for filename in os.listdir("photos"):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            student_id = filename.split(".")[0]
            encoding = encode_face(f"photos/{filename}")
            if encoding is not None:
                face_encodings[student_id] = encoding
                print(f"[+] Encoded {student_id}")
            else:
                print(f"[!] Could not encode {student_id}")

    with open("attendance_data/face_encodings.pkl", "wb") as f:
        pickle.dump(face_encodings, f)
    print("✅ All encodings saved!")

if __name__ == "__main__":
    train_and_save_encodings()
