import cv2
from insightface.app import FaceAnalysis
from face_memory import FaceMemory

# -------------------------
# Load AI
# -------------------------

print("Loading Vision...")

app = FaceAnalysis(
    name="buffalo_sc",
    providers=["CPUExecutionProvider"]
)

app.prepare(
    ctx_id=0,
    det_size=(320, 320)
)

memory = FaceMemory()

print("Vision Ready")
print()

# -------------------------
# Camera
# -------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open camera.")
    quit()

print("--------------------------------")
print("ROUX FACE REGISTRATION")
print("--------------------------------")
print("Stand in front of the camera.")
print("Press SPACE to save your face.")
print("Press ESC to quit.")
print("--------------------------------")

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    faces = app.get(frame)

    for face in faces:

        x1, y1, x2, y2 = map(int, face.bbox)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Press SPACE",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("ROUX Register Face", frame)

    key = cv2.waitKey(1) & 0xFF

    # ESC
    if key == 27:
        break

    # SPACE
    if key == 32:

        if len(faces) == 0:
            print("No face detected.")
            continue

        face = faces[0]

        name = input("\nPerson name: ").strip()

        if len(name) == 0:
            print("Invalid name.")
            continue

        memory.add_face(
            name,
            face.embedding
        )

        print()
        print("Face saved successfully.")
        print("Person:", name)
        print()

cap.release()

cv2.destroyAllWindows()