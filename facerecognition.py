"""
This Python Script Encapsulate Functions for face-recognition
"""

import cv2

class FaceRecognition:
    def __init__(self, max_recognition_itr = 400):
        """
        Initialize FaceRecognizer

        Keyword Argument:

        max_recognition_itr: Max time allowed for re-recognition
        """
        # Set max_recognition_itr
        self.max_recognition_itr = max_recognition_itr

        # Load recognize and read label from model
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("FaceRecognition/train.yml")

        # load labels
        #self.labels = {"person_name": 1}
        #with open("labels.pickle", "rb") as f:
            #self.labels = pickle.load(f)
            #self.labels = {v: k for k, v in self.labels.items()}

        # Define camera and detect face
        self.face_cascade = cv2.CascadeClassifier('FaceRecognition/haarcascade/haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)

    def recognize(self)->int:
        """
        Recoginize the face

        Return -1 if no label matches, return customer_id if face matches.
        """
        for i in range(self.max_recognition_itr):

            # Open Camera and Read Data
            ret, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                # predict the id and confidence for faces
                id_, conf = self.recognizer.predict(roi_gray)

                if conf >= 60:
                    return id_
        return -1

if __name__ == "__main__":
    faceRecognition = FaceRecognition()
    print(faceRecognition.recognize())
