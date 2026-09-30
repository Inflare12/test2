import cv2
from insightface.app import FaceAnalysis

# Load AI model
app = FaceAnalysis(
    name="buffalo_sc",
    providers=["CPUExecutionProvider"]
)

app.prepare(ctx_id=0)

camera = cv2.VideoCapture(0)

while True:

    ret, frame = camera.read()

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
            "Face",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imshow("ROUX Vision", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()