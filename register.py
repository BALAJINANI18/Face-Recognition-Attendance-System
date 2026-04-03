import cv2
import sqlite3
import os

# Create folder
if not os.path.exists("faces"):
    os.makedirs("faces")

name = input("Enter student name: ")

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
student_id = cursor.lastrowid

conn.commit()
conn.close()

# ✅ SAFE CAMERA OPEN
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not detected ❌")
    exit()

print("Press 's' to capture image, 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera error ❌")
        break

    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        filename = f"faces/{student_id}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Face saved as {filename} ✅")
        break

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()