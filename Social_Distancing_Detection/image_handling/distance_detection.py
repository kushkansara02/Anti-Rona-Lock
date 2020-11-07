from .facedetector import FaceDetector
from .distance_calculations import get_distance
import imutils
import cv2

# the following class will be able to detect whether faces are social distancing given an input file #

class DistanceDetector:

    image_file = None
    image = None
    gray = None
    distance_tolerance = None
    adj_width = None
    all_faces = None
    face_distances = None
    all_breaches = None

    def __init__(self, image_file = None, image = [], distance_tolerance = 2, adj_width = 500):
        self.image_file = image_file
        self.distance_tolerance = distance_tolerance
        self.adj_width = adj_width
        if len(image) > 0:
            self.image = imutils.resize(image, width=self.adj_width)
        else:
            self.image = imutils.resize(cv2.imread(image_file), width=self.adj_width)

        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def detectFaces(self):
        fd = FaceDetector()
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
        self.detectFaces()
        self.face_distances = []
        faces_done = []
        # for face in self.all_faces:
        #     # comparing current face's position to all other faces in image
        #     # refactor the -1: is messing up distance formulas
        #     for compFace in self.all_faces:
        #         #checking if distances between these faces already exist
        #         if face != compFace and not ([compFace, face] in faces_done or [face, compFace] in faces_done):
        #             # x-distance: -1 if faces are overlapping
        #             if compFace["startCord"][0] > face["endCord"][0]:
        #                 x_dist = abs(compFace["startCord"][0] - face["endCord"][0])
        #             elif compFace["startCord"][0] < face["endCord"][0] and face["startCord"][0] < compFace["endCord"][0]:
        #                 x_dist = -1
        #             elif compFace["endCord"][0] > face["startCord"][0] and compFace["startCord"][0] < face["endCord"][0]:
        #                 x_dist = -1
        #             else:
        #                 x_dist = abs(compFace["endCord"][0] - face["startCord"][0])
        #
        #             # y-distance: -1 if faces are overlapping
        #             if compFace["startCord"][1] > face["endCord"][1]:
        #                 y_dist = abs(compFace["startCord"][1] - face["endCord"][1])
        #             elif compFace["startCord"][1] < face["endCord"][1] and face["startCord"][1] < compFace["endCord"][1]:
        #                 y_dist = -1
        #             elif compFace["endCord"][1] > face["startCord"][1] and compFace["startCord"][1] < face["endCord"][1]:
        #                 y_dist = -1
        #             else:
        #                 y_dist = abs(compFace["endCord"][1] - face["startCord"][1])
        #
        #             # updating data structures with newfound information
        #             self.face_distances.append({"faces": [face, compFace], "dist": [x_dist, y_dist]})
        #             faces_done.append([face, compFace])
        for face in self.all_faces:
            for compFace in self.all_faces:
                if face != compFace and not ([compFace, face] in faces_done or [face, compFace] in faces_done):
                    distance = get_distance(face["startCord"][0], face["startCord"][1], face["endCord"][0], face["endCord"][1], compFace["startCord"][0], compFace["startCord"][1], compFace["endCord"][0], compFace["endCord"][1], 1, 1, self.adj_width)
                    self.face_distances.append({"faces": [face, compFace], "dist": distance})
                    faces_done.append([face, compFace])

    def getCloseFaces(self):
        self.detectDistances()
        # going through data structure to find exact people in breach and the location of their faces (to draw red rectangle around them)
        self.all_breaches = []
        for face_combo in self.face_distances:
            if face_combo["dist"] < self.distance_tolerance:
                self.all_breaches.append(face_combo)
                cv2.putText(self.image, "Faces in this image not following social distancing",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
                print("SOCIAL DISTANCING IN BREACH")
                print("Face 1: {faceStart} to {faceEnd}".format(faceStart = face_combo["faces"][0]["startCord"], faceEnd = face_combo["faces"][0]["endCord"]))
                print("Face 2: {faceStart} to {faceEnd}".format(faceStart = face_combo["faces"][1]["startCord"], faceEnd = face_combo["faces"][1]["endCord"]))
                print("Distance: {distance}".format(distance = face_combo["dist"]))
                print("\n")

    def showImage(self):
        cv2.imshow("Faces", self.image)
        cv2.waitKey(0)
