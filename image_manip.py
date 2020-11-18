import cv2
import os

class ImageWriter:

    directory = None
    image_count = 0
    name = None
    extension = None

    def __init__(self, directory = None, name = "image", extension = ".jpg"):
        self.directory = directory
        self.name = name
        self.extension = extension

    def writeImage(self, image):
        self.image_count += 1
        cv2.imwrite(self.directory + self.name + str(self.image_count) + self.extension, image)

    def deleteImages(self):
        i = 1
        while (os.path.isfile(self.directory + self.name + str(i) + self.extension)):
            os.remove(self.directory + self.name + str(i) + self.extension)
            i += 1
    
    def getImageName(self):
        return self.name + str(self.image_count) + self.extension

    def getCurrentImageAbsPath(self):
        return self.directory + self.getImageName()

    def getIthImageName(self, i):
        if (i <= self.image_count and i > 0):
            return self.name + str(i) + self.extension
        else:
            return None

    def getIthImageAbsPath(self, i):
        if (i <= self.image_count and i > 0):
            return self.directory + self.getIthImageName(i)
        else:
            return None