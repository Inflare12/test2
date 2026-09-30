import cv2

from insightface.app import FaceAnalysis

from camera import Camera
from face_memory import FaceMemory
from learn_face import FaceLearner
from object_detector import ObjectDetector


class Vision:

    def __init__(self):

        print("Loading Vision...")

        self.camera = Camera()

        self.memory = FaceMemory()

        self.learner = FaceLearner(
            self.memory
        )

        self.detector = ObjectDetector()

        self.app = FaceAnalysis(
            name="buffalo_sc",
            providers=["CPUExecutionProvider"]
        )

        self.app.prepare(
            ctx_id=0,
            det_size=(320, 320)
        )

        self.object_results = None
        self.frame_count = 0

        print("Vision Ready")

    # ============================================
    # MAIN UPDATE
    # ============================================

    def update(self):

        frame = self.camera.get_frame()

        if frame is None:
            return -1

        # ----------------------------------------
        # FACE DETECTION
        # ----------------------------------------

        faces = self.app.get(frame)

        for face in faces:

            embedding = face.embedding

            name = self.memory.find_person(
                embedding
            )

            x1, y1, x2, y2 = map(
                int,
                face.bbox
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                name,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        # ----------------------------------------
        # OBJECT DETECTION
        # ----------------------------------------

        self.frame_count += 1

        if self.frame_count % 5 == 0:

            self.object_results = self.detector.detect(
                frame
            )

        if self.object_results is not None:

            for box in self.object_results.boxes:

                cls = int(box.cls[0])

                label = self.object_results.names[
                    cls
                ]

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (255, 0, 0),
                    2
                )

                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 0),
                    2
                )

        # ----------------------------------------
        # SHOW WINDOW
        # ----------------------------------------

        cv2.imshow(
            "ROUX Vision",
            frame
        )

        return cv2.waitKey(1) & 0xFF

    # ============================================
    # LEARN NEW PERSON
    # ============================================

    def learn_person(self, name):

        frame = self.camera.get_frame()

        if frame is None:
            return False

        faces = self.app.get(frame)

        if len(faces) == 0:
            return False

        self.learner.learn(
            name,
            faces[0].embedding
        )

        print(f"Learned {name}")

        return True

    # ============================================
    # CLOSE
    # ============================================

    def close(self):

        self.camera.release()

        cv2.destroyAllWindows()