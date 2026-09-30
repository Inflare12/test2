import cv2


class Camera:

    def __init__(self, index=0):

        self.cap = cv2.VideoCapture(index)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def get_frame(self):

        ok, frame = self.cap.read()

        if not ok:
            return None

        return frame

    def release(self):

        self.cap.release()

if __name__ == "__main__":

    camera = Camera()

    while True:

        frame = camera.read()

        if frame is None:
            continue

        cv2.imshow("ROUX Camera", frame)

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()