from math import cos
from math import sqrt
from math import pi
from .image_analysis import get_cam_to_object_distance
from .image_analysis import get_angle

CONST_CAM_ANGLE = pi/2 #Our camera is supposedly 90 degrees or pi/2, but I'm not sure about this. 
#CONST_CAM_ANGLE: angle of the horizontal field of view of the camera in RADIANS
CONST_AVG_FACE_BREADTH = 0.20 #Average is roughly 15cm or 0.15m (https://en.wikipedia.org/wiki/Human_head#Average_head_sizes), but the rectangles around detected faces are usually too big, so I will increase it a bit to account for this
#CONST_AVG_FACE_BREADTH: the average face width/breadth of adult humans in METERS

#Point class is not really necessary
class Point():
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print_point(self):
        print(str(self.x) + ", " + str(self.y))


#get_distance returns the HORIZONTAL distance between the center of two faces (rectangles) in an image using ratios and the law of cosines.

#parameters
#(x1,y1): top left corner of face 1's "rectangle", (x2,y2): bottom right corner of face 1 
#(x3,y3): is top left corner of face 2, (x4,y4): bottom right corner of face 2
#imagePixelWidth: width of the image in pixels

def get_distance(x1, y1, x2, y2, x3, y3, x4, y4, imagePixelWidth): 
    face1Center = Point((x1+x2)/2, (y1+y2)/2)
    # print("f1:")
    # face1Center.print_point()
    face2Center = Point((x3+x4)/2, (y3+y4)/2)
    # print("f2:")
    # face2Center.print_point()
    face1Dist = get_cam_to_object_distance(CONST_AVG_FACE_BREADTH, get_angle(x1, x2, imagePixelWidth, CONST_CAM_ANGLE))
    face2Dist = get_cam_to_object_distance(CONST_AVG_FACE_BREADTH, get_angle(x3, x4, imagePixelWidth, CONST_CAM_ANGLE))
    theta = get_angle(face1Center.x, face2Center.x, imagePixelWidth, CONST_CAM_ANGLE)
    # print("theta: " + str(theta))
    
    #rest is trig (law of cosines)
    distanceSquared = face1Dist*face1Dist + face2Dist*face2Dist - 2*face1Dist*face2Dist*cos(theta)
    # print("cos(theta): " + str(cost(theta)))
    # print("distance squared: " + str(distanceSquared))
    return sqrt(distanceSquared)

if __name__ == "__main__":
    test = get_distance(0,0,50,0,50,0,100,0,100)
    print(test)


