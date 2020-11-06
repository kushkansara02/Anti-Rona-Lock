#whole bunch of other imports here
from time import sleep
from PIL import Image, ImageTk
#I installed PIL (pillow) using this: pip3 install pillow
#Not sure if pillow is needed anymore, tkinter might be enough
import tkinter

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

    # main()

    image_list = []

    # image1 = Image.open("cat.png")
    # image_list[0].show()

    root = tkinter.Tk()
    root.title("Main")

    canvas = tkinter.Canvas(root, width=1000, height=1000) 
    canvas.pack()     
    
    img = tkinter.PhotoImage(file="cat.png") #png images done like this
    img2 = ImageTk.PhotoImage(Image.open("cat2.jpg")) #jpg is not supported by tkinter, so gotta do it this way
    image_list.append(img)
    image_list.append(img2)    

    # canvas.create_image(0,0, anchor=tkinter.constants.NW, image=image_list[0])   
    # canvas.pack() 
    # root.update()

    # sleep(2)

    # canvas.delete("all")
    # canvas.create_image(0,0, anchor=tkinter.constants.NW, image=image_list[1]) 
    # canvas.pack()
    # root.update()

    i = 0
    def change_image():
        canvas.delete("all")
        global i
        canvas.create_image(0,0, anchor=tkinter.constants.NW, image=image_list[i])
        root.update() 
        i += 1
        if i >= len(image_list):
            i = 0

    button = tkinter.Button(root, text="Next Image", command=change_image)
    button.place(x=480,y=800)

    root.mainloop()  

    # image2 = Image.open("cat2.jpg")
    # image2.show()