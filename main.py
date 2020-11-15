from time import sleep
from PIL import Image, ImageTk
#I installed PIL (pillow) using "pip3 install pillow"
import tkinter
from Social_Distancing_Detection.image_handling.distance_detection import DistanceDetector
import os
from random import randint
# from Mask_Detection.detect_mask_video import detect_and_predict_mask
# from tensorflow.keras.models import load_model
# import cv2

debug_or_be_bugged_abs_path = os.path.dirname(os.path.realpath(__file__))

# # load our serialized face detector model from disk
# prototxtPath = debug_or_be_bugged_abs_path + "Mask_Detection/face_detector/deploy.prototxt"
# weightsPath = debug_or_be_bugged_abs_path + "Mask_Detection/face_detector/res10_300x300_ssd_iter_140000.caffemodel"
# faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# # load the face mask detector model from disk
# maskNet = load_model(debug_or_be_bugged_abs_path + "Mask_Detection/mask_detector.model") 

image_list = []

root = tkinter.Tk()
root.title("Main")

CONST_CANVAS_WIDTH = 1000
CONST_CANVAS_HEIGHT = 1000
CONST_CANVAS_MAX_IMAGE_HEIGHT = 800
canvas = tkinter.Canvas(root, width=CONST_CANVAS_WIDTH, height=CONST_CANVAS_HEIGHT) 
canvas.pack()     

# return a new size (2-tuple) given an original size (2-tuple) and a desired width, scales size linearly. Takes into account the max allowed image height.
def new_size(size, desired_width=CONST_CANVAS_WIDTH):
    width = size[0]
    height = size[1]
    new_width = desired_width
    new_height = (int) ((desired_width/width)*height)
    if new_height > CONST_CANVAS_MAX_IMAGE_HEIGHT:
        new_height = CONST_CANVAS_MAX_IMAGE_HEIGHT
        new_width = (int) ((CONST_CANVAS_MAX_IMAGE_HEIGHT/new_height)*new_width)
    return (new_width, new_height)

# return a ImageTk.PhotoImage image given the name of the image and the directory containing it
def tkimage(filename, location):
    abs_path = location + filename
    img_size = Image.open(abs_path).size
    # print(img_size)
    # print("new size: " + str(new_size(img_size)))
    resized_img = Image.open(abs_path).resize(new_size(img_size))
    img = ImageTk.PhotoImage(resized_img)
    # alternative method: img = tkinter.PhotoImage(file="filename")
    return img

images_abs_path = debug_or_be_bugged_abs_path + "/images/"

img1 = tkimage("cat1.png", images_abs_path)
img2 = tkimage("cat2.jpg", images_abs_path)
img3 = tkimage("cat3.jpg", images_abs_path)

image_list.append(img1)
image_list.append(img2)    
image_list.append(img3)

i = 0
canvas.create_image(0,0, anchor=tkinter.constants.NW, image=image_list[i])   

def next_image():
    canvas.delete("all")
    global i
    i += 1
    if i >= len(image_list):
        i = 0
    canvas.create_image(0,0, anchor=tkinter.constants.NW, image=image_list[i])

def prev_image():
    canvas.delete("all")
    global i
    i -= 1
    if i < 0:
        i = len(image_list)-1
    canvas.create_image(0,0, anchor=tkinter.constants.NW, image=image_list[i])
    

button = tkinter.Button(root, text="Next Image", command=next_image)
button.place(x=500,y=900)
button = tkinter.Button(root, text="Previous Image", command=prev_image)
button.place(x=400,y=900)

#below are (mostly) dummy functions

def arduino_start():
    print("Arduino started.")
    return

def arduino_get_image():
    print("Retrieved image successfully.")
    return 0

def arduino_range_sensor():
    #will tell us if there is an object in front of the door
    print("There is someone at the door.")
    return True

def arduino_unlock_door():
    print("Door unlocked successfully.")
    return

def arduino_lock_door():
    print("Door locked successfully.")
    return

def arduino_stop():
    print("Arduino stopped.")
    return

def mask_detection(image):
    # simulating mask detection (50/50 chance)
    boolean = bool(randint(0,1))
    print("Masks are " + ("" if boolean else "not ") + "being worn.")
    return boolean
    # locations_and_predictions = detect_and_predict_mask(cv2.imread(image), faceNet, maskNet)
    # if len(locations_and_predictions[1]) == 0:
    #     printf("Masks being worn.")
    #     return True
    # printf("Masks not being worn.")
    # return False

detector = DistanceDetector(images_abs_path + "cat1.png") # cat.png is arbitrary, just need to pass an image or else errors will occur for some reason

def distance_detection(image):
    detector.__init__(image)
    detector.getCloseFaces()
    allBreaches = detector.all_breaches
    # detector.showImage()
    detector.writeImage(location=images_abs_path)
    if len(allBreaches) > 0:
        print("Distance not being maintained.")
        return False #do not open door, they are not following rules
    print("Distance being maintained.")
    return True #open door

# def main():
#     arduino_start()
#     locked = True
#     wait_time = 1
#     while locked:
#         if arduino_range_sensor():
#             image = arduino_get_image()
#             masks = mask_detection(image)
#             distancing = distance_detection(image)
#             if (masks and distancing):
#                 arduino_unlock_door()
#                 locked = False
#             else:
#                 print("Violation detected. Waiting " + str(wait_time) + " seconds before getting new image.")
#                 sleep(wait_time)
            
#     sleep(5)
#     arduino_lock_door()
#     arduino_stop()
#     print("Program Finished.")


#this code replaces main()
arduino_start()
CONST_WAIT_TIME = 1
def while_loop():
    if arduino_range_sensor():
        image = arduino_get_image()
        # image_list.append(image)
        # next_image()
        masks = mask_detection(image)
        # distancing = distance_detection(image)
        distancing = distance_detection(images_abs_path + "johnCena.jpg")
        image_list.append(tkimage("johnCena.jpg", images_abs_path))
        if (masks and distancing):
            arduino_unlock_door()
            sleep_time = 1
            print("Waiting " + str(sleep_time) + " seconds before relocking.")
            sleep(sleep_time)
            arduino_lock_door()
            arduino_stop()
            print("Program Finished.")
            # comment out root.destory() if not testing
            # root.destroy()
        else:
            print("Violation detected. Waiting " + str(CONST_WAIT_TIME) + " seconds before trying again.")
            root.after(CONST_WAIT_TIME*1000, while_loop)
    
root.after(CONST_WAIT_TIME*1000, while_loop)

root.mainloop()  

def delete_images():
    i = 1
    while (os.path.isfile(images_abs_path + "image" + str(i) + ".jpg")):
        os.remove(images_abs_path + "image" + str(i) + ".jpg")
        i += 1

delete_images()