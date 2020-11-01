from __future__ import print_function
from imagePipeline import getAllImages
from image_handling import *

# this file is an example of how to use the image_handling module in order to detect faces in an IMAGE

allImages = getAllImages()

for file in allImages:
    detector = DistanceDetector(image_file = file)
    detector.getCloseFaces()
    detector.showImage()