from math import tan

#These functions are for the use of the 'distance_calculation.py' file ONLY

#get_cam_to_object_distance returns approx distance from camera to object in image

#parameters
#known_size: the approximate size (width) of the object in question
#angle: the HORIZONTAL camera angle between the left and right edge of the object

def get_cam_to_object_distance(known_size, angle):
    return known_size / (2*tan(angle/2))

#get_angle returns approx HORIZONTAL camera angle between two points/pixels in an image

#parameters
#x1: the x coord of the first point/pixel
#x2: the x coord of the second point/pixel
#imagePixelWidth: the width of the image in pixels
#camAngle: the angle of the field of view of the camera in RADIANS

def get_angle(x1, x2, imagePixelWidth, camAngle):
    return (abs(x1-x2)/imagePixelWidth) * camAngle