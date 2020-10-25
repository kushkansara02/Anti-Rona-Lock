from __future__ import print_function
from imagePipeline import getAllImages
from pyimagesearch.distance_detection import DistanceDetector

allImages = getAllImages()
file_num = 0

for file in allImages:
    if file_num == 0:
        detector = DistanceDetector(file)
        detector.detectFaces()
        detector.detectDistances()
        detector.getCloseFaces()
        detector.showImage()

    file_num += 1
