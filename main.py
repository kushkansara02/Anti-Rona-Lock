from time import sleep
from random import randint
from PIL import Image, ImageTk #I installed PIL (pillow) using "pip3 install pillow"
import tkinter
from image_manip import ImageWriter
from Social_Distancing_Detection.image_handling.distance_detection import DistanceDetector
import os
import cv2
import imutils
import numpy
import serial 
#pip3 install pyserial
import urllib.request
from Mask_Detection.detect_mask_video import detect_and_predict_mask
from tensorflow.keras.models import load_model

debug_or_be_bugged_abs_path = os.path.dirname(os.path.realpath(__file__))

# list of images which can be cycled through using buttons
image_list = []

### TKINTER stuff ###

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

img1 = tkimage("logo.jpg", images_abs_path)
# img2 = tkimage("cat2.jpg", images_abs_path)
# img3 = tkimage("cat3.jpg", images_abs_path)

image_list.append(img1)
# image_list.append(img2)    
# image_list.append(img3)

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

# creating instances of each class we are using
image_writer_arduino = ImageWriter(directory=images_abs_path, name="camera")
image_writer_masks = ImageWriter(directory=images_abs_path, name="masks")
image_writer_distancing = ImageWriter(directory=images_abs_path, name="distancing")
detector = DistanceDetector(images_abs_path + "cat1.png") # cat1.png is arbitrary, just need to pass an image or else errors will occur for some reason

### ARDUINO ###

# arduino_port = "COM3"
# ser = serial.Serial(arduino_port)
# ser.write(b'open')

camera_url = "http://192.168.1.106/cam-hi.jpg"
ser = serial.Serial('COM3', 115200);

def arduino_start():
    print("Arduino started.")
    return

def arduino_get_image():
    # https://youtu.be/92UBFhPJQJ8 at 9:20
    camera_response = urllib.request.urlopen(camera_url)
    print(camera_response.info())
    numpy_image = numpy.array(bytearray(camera_response.read()), dtype=numpy.uint8)
    retrieved_image = cv2.imdecode(numpy_image, -1)
    image_writer_arduino.writeImage(retrieved_image)
    print("Retrieved image from arduino successfully.")
    return 0

def arduino_range_sensor():
    # will tell us if there is an object in front of the door
    print("There is someone at the door.")
    return True

def arduino_unlock_door():
    ser.write(b'o') 
    print("Door unlocked successfully.")
    return

def arduino_lock_door():
    ser.write(b'c') 
    print("Door locked successfully.")
    return

def arduino_stop():
    print("Arduino stopped.")
    return

### MASK DETECTION ###

# load our serialized face detector model from disk
prototxtPath = debug_or_be_bugged_abs_path + "/Mask_Detection/face_detector/deploy.prototxt"
weightsPath = debug_or_be_bugged_abs_path + "/Mask_Detection/face_detector/res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
maskNet = load_model(debug_or_be_bugged_abs_path + "/Mask_Detection/mask_detector.model") 

def mask_detection(image):
    # # simulating mask detection (50/50 chance)
    # boolean = bool(randint(0,1))
    # print("Masks are " + ("" if boolean else "not ") + "being worn.")
    # return boolean

    # get the frame (image) using cv2.imread
    frame = cv2.imread(image)

    # detect faces in the frame and determine if they are wearing a face mask or not
    (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

    # loop over the detected face locations and their corresponding locations
    for (box, pred) in zip(locs, preds):
        # unpack the bounding box and predictions
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred

        # determine the class label and color we'll use to draw
        # the bounding box and text
        label = "Mask" if mask > withoutMask else "No Mask"
        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

        # include the probability in the label
        label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

        # display the label and bounding box rectangle on the output frame
        cv2.putText(frame, label, (startX - 20, endY + 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

    # # show the output frame
    # cv2.imshow("Frame", frame)
    # cv2.waitKey(0)
    image_writer_masks.writeImage(frame)
    image_list.append(tkimage(image_writer_masks.getImageName(), images_abs_path))
    if (len(preds) == 0):
        print("Mask detection couldn't detect any faces..")
        return False
    if preds[0][0]*100 > 50:
        print("Mask(s) being worn.")
        return True
    print("Mask(s) not being worn.")
    return False

### DISTANCE DETECTION ###

def distance_detection(image):
    detector.__init__(image)
    detector.getCloseFaces()
    allBreaches = detector.all_breaches
    # detector.showImage()
    image_writer_distancing.writeImage(detector.image)
    image_list.append(tkimage(image_writer_distancing.getImageName(), images_abs_path))
    if len(allBreaches) > 0:
        print("Distance not being maintained.")
        return False # do not open door, they are not following rules
    print("Distance being maintained.")
    return True # open door

### more TKINTER below ###

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

# this replaces main()
arduino_start()
CONST_WAIT_TIME = 3
def while_loop():
    if arduino_range_sensor():
        arduino_get_image()
        image_path = image_writer_arduino.getCurrentImageAbsPath()
        # test_image_path = images_abs_path + "johnCena.jpg"
        masks = mask_detection(image_path)
        distancing = distance_detection(image_path)
        # Auto present the current image
        next_image()
        if (masks and distancing):
            arduino_unlock_door()
            # sleep_time = 3
            # print("Waiting " + str(sleep_time) + " seconds before relocking.")
            # # sleep(sleep_time)
            # arduino_lock_door()
            # arduino_stop()
            print("Program Finished.")
            # root.destroy()
        else:
            print("Violation detected. Waiting " + str(CONST_WAIT_TIME) + " seconds before trying again.")
            root.after(CONST_WAIT_TIME*1000, while_loop)
    
root.after(CONST_WAIT_TIME*1000, while_loop)

root.mainloop()  

### END ###

# deleting all the newly created images after program is finished
image_writer_arduino.deleteImages()
image_writer_masks.deleteImages()
image_writer_distancing.deleteImages()