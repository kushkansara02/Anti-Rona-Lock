import cv2
import os

class FaceDetector:

    faceCascade = None

    def __init__(self, faceCascadePath = "/cascades/haarcascade_frontalface_default.xml"):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        finalPath = dir_path + faceCascadePath
        self.faceCascade = cv2.CascadeClassifier(finalPath)

    def detect(self, image, scaleFactor=1.1, minNeighbors=1, minSize=(30, 30)):
        rects = self.faceCascade.detectMultiScale(
            image, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize, flags=cv2.CASCADE_SCALE_IMAGE)
        return rects
