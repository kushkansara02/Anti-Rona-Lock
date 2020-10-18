import os


def getAllImages():
    imagesArr = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    images_path = dir_path + "/images/"

    for filename in os.listdir(images_path):
        if "DS_Store" not in filename:
            imagesArr.append(images_path + filename)

    return imagesArr
