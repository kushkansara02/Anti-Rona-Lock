from __future__ import print_function
from pyimagesearch.facedetector import FaceDetector
import imutils
import cv2
from imagePipeline import getAllImages

allImages = getAllImages()
facePath = "cascades/haarcascade_frontalface_default.xml"

for file in allImages:
    height = 750
    image = imutils.resize(cv2.imread(file), height=height)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    fd = FaceDetector(facePath)
    faceRects = fd.detect(gray, scaleFactor=1.1,
                          minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faceRects:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, "{} faces in this image".format(len(faceRects)),
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

    cv2.imshow("Faces", image)
    cv2.waitKey(0)
