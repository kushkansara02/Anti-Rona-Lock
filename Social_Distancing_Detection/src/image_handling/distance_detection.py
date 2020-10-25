from facedetector import FaceDetector
import imutils
import cv2

# the following class will be able to detect whether faces are social distancing given an input file

class DistanceDetector:

    image_file = None
    image = None
    gray = None
    face_path = None
    pixel_tolerance = None
    adj_height = None
    all_faces = None
    face_distances = None

    def __init__(self, image_file, face_path = "cascades/haarcascade_frontalface_default.xml", pixel_tolerance = 100, adj_height = 750):
        self.image_file = image_file
        self.face_path = face_path
        self.pixel_tolerance = pixel_tolerance
        self.adj_height = adj_height
        self.image = imutils.resize(cv2.imread(image_file), height= self.adj_height)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def detectFaces(self):
        fd = FaceDetector(self.face_path)
        face_rects = fd.detect(self.gray, scaleFactor=1.1,
                              minNeighbors=5, minSize=(30, 30))

        self.all_faces = []
        for (x, y, w, h) in face_rects:
            start_cord = (x, y)
            end_cord = (x + w, y + h)
            cv2.rectangle(self.image, start_cord, end_cord, (0, 255, 0), 2)
            cv2.putText(self.image, "{} faces in this image".format(len(face_rects)),
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            self.all_faces.append({"startCord": start_cord, "endCord": end_cord})

    def detectDistances(self):
        self.face_distances = []
        faces_done = []
        for face in self.all_faces:
            # comparing current face's position to all other faces in image
            for compFace in self.all_faces:
                #checking if distances between these faces already exist
                if face != compFace and not ([compFace, face] in faces_done or [face, compFace] in faces_done):
                    # x-distance: -1 if faces are overlapping
                    if compFace["startCord"][0] > face["endCord"][0]:
                        x_dist = abs(compFace["startCord"][0] - face["endCord"][0])
                    elif compFace["startCord"][0] < face["endCord"][0] and face["startCord"][0] < compFace["endCord"][0]:
                        x_dist = -1
                    elif compFace["endCord"][0] > face["startCord"][0] and compFace["startCord"][0] < face["endCord"][0]:
                        x_dist = -1
                    else:
                        x_dist = abs(compFace["endCord"][0] - face["startCord"][0])

                    # y-distance: -1 if faces are overlapping
                    if compFace["startCord"][1] > face["endCord"][1]:
                        y_dist = abs(compFace["startCord"][1] - face["endCord"][1])
                    elif compFace["startCord"][1] < face["endCord"][1] and face["startCord"][1] < compFace["endCord"][1]:
                        y_dist = -1
                    elif compFace["endCord"][1] > face["startCord"][1] and compFace["startCord"][1] < face["endCord"][1]:
                        y_dist = -1
                    else:
                        y_dist = abs(compFace["endCord"][1] - face["startCord"][1])

                    # updating data structures with newfound information
                    self.face_distances.append({"faces": [face, compFace], "dist": [x_dist, y_dist]})
                    faces_done.append([face, compFace])

    def getCloseFaces(self):
        # going through data structure to find exact people in breach and the location of their faces (to draw red rectangle around them)
        allBreaches = []
        for face_combo in self.face_distances:
            distance = pow(pow(face_combo["dist"][0], 2) + pow(face_combo["dist"][1], 2), 0.5)
            if distance < self.pixel_tolerance:
                allBreaches.append([face_combo["faces"], distance])
                print("SOCIAL DISTANCING IN BREACH")
                print("Face 1: {faceStart} to {faceEnd}".format(faceStart = face_combo["faces"][0]["startCord"], faceEnd = face_combo["faces"][0]["endCord"]))
                print("Face 2: {faceStart} to {faceEnd}".format(faceStart = face_combo["faces"][1]["startCord"], faceEnd = face_combo["faces"][1]["endCord"]))
                print("Distance (in pixels for now): {distance}".format(distance = distance))
                print("\n")

        return allBreaches

    def showImage(self):
        cv2.imshow("Faces", self.image)
        cv2.waitKey(0)