from math import cos
from math import sqrt
from math import pi

#Not really necessary to make point class, but whatever
class Point():
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print_point(self):
        print(str(self.x) + ", " + str(self.y))

#This function will eventually be used for calculating the distance between two faces in a picture

def get_distance(x1,y1,x2,y2,x3,y3,x4,y4,face1Dist,face2Dist,imagePixelWidth,camAngle): 
    #(x1,y1) is the top left corner of face 1's "box", (x2,y2) is bottom right corner of face 1, 
    #(x3,y3) is top left corner of face 2, (x4,y4) is bottom right corner of face 2
    #face1Dist and face2Dist is the distance from the camera to face 1 and 2, respectively (say, in METERS)
    #imagePixelWidth is the width of the image in pixels
    #camAngle is the angle of the field of view of the camera in RADIANS

    #note that the y coord is actually unecessary, we only care about x coords, so this code is bad lol
    face1Center = Point((x1+x2)/2, (y1+y2)/2)
    print("f1:")
    face1Center.print_point()
    face2Center = Point((x3+x4)/2, (y3+y4)/2)
    print("f2:")
    face2Center.print_point()
    pixelDistX = abs(face1Center.x-face2Center.x)
    print("Pixel distance x:")
    print(pixelDistX)
    theta = (pixelDistX/imagePixelWidth) * camAngle
    print("theta")
    print(theta)
    
    #rest is trig (law of cosines)
    distanceSquared = face1Dist*face1Dist + face2Dist*face2Dist - 2*face1Dist*face2Dist*cos(theta)
    print("cos(theta):")
    print(cos(theta))
    print("distance squared:")
    print(distanceSquared)
    return sqrt(distanceSquared)


test = get_distance(0,0,50,0,50,0,100,0,1,1,100,pi/2)
print(test)