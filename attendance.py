import cv2
import face_recognition
import os
import sqlite3
from datetime import datetime

known_encodings = []
known_ids = []

# Load faces
for file in os.listdir("faces"):
    path = f"faces/{file}"
    image = face_recognition.load_image_file(path)
    encodings = face_recognition.face_encodings(image)

    if len(encodings) > 0:
        known_encodings.append(encodings[0])
        known_ids.append(int(file.split(".")[0]))

print("Faces loaded ✅")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera not detected")
    exit()

marked_ids = set()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera error ")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding)

        if True in matches:
            index = matches.index(True)
            student_id = known_ids[index]

            if student_id in marked_ids:
                continue

            marked_ids.add(student_id)

            conn = sqlite3.connect("attendance.db")
            cursor = conn.cursor()

            today = datetime.now().strftime("%Y-%m-%d")

            try:
                cursor.execute("""
                INSERT INTO attendance (student_id, date, status)
                VALUES (?, ?, ?)
                """, (student_id, today, "Present"))

                conn.commit()
                print(f"Attendance marked for ID {student_id} ✅")

            except:
                pass

            conn.close()

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()