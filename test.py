from vision import Vision

vision = Vision()

while True:

    key = vision.update()

    if key == ord("q"):
        break

vision.close()