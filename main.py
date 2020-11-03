#whole bunch of other imports here
from time import sleep
from PIL import Image
#I installed PIL (pillow) using this: pip3 install pillow

def arduino_start():
    print("Arduino started.")
    return

def arduino_get_image():
    print("Retrieved image successfully.")
    return 0

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
    print("Masks are being worn.")
    return True

def distance_detection(image):
    print("Social distancing is being maintained.")
    return True



#main is currently full of dummy functions that have yet to be actually implemented 
def main():
    arduino_start()
    locked = True
    wait_time = 1
    while locked:
        image = arduino_get_image()
        masks = mask_detection(image)
        distancing = distance_detection(image)
        if (masks and distancing): 
            arduino_unlock_door()
            locked = False
        else:
            print("Violation detected. Waiting " + str(wait_time) + " seconds before getting new image.")
            sleep(wait_time)
            
    sleep(10)
    arduino_lock_door()
    arduino_stop()
    print("Program Finished.")


if __name__ == "__main__":
    image1 = Image.open("cat.png")
    image1.show()
    # image2 = Image.open("cat2.jpg")
    # image2.show()
    main()