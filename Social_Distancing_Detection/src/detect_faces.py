from __future__ import print_function
from imagePipeline import getAllImages
from image_handling.distance_detection import DistanceDetector

allImages = getAllImages()

for file in allImages:
    detector = DistanceDetector(file)
    detector.detectFaces()
    detector.detectDistances()
    detector.getCloseFaces()
    detector.showImage()
