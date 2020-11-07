from image_handling import *
import imutils
import cv2

# webcam
camera = cv2.VideoCapture(0)

## ENABLE THIS AND DISABLE ABOVE WEBCAM CODE IF YOU ARE USING VIDEO FILE ##
# camera = cv2.VideoCapture("path_to_video.mp4")

# a video is just a collection of frames. to do active face detection in a video, call face detector on every frame
# not sure how this will transfer to Arduino, for now I'm using my Mac's webcam
# this code will also work with a video file

while True:
    (grabbed, frame) = camera.read()

    ## ENABLE THIS IF YOU ARE USING A VIDEO FILE ##
    # if not grabbed:
    #     break

    detector = DistanceDetector(image=frame)
    allBreaches = detector.getCloseFaces()
    print(allBreaches)
    cv2.imshow("Webcam!", detector.image)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()