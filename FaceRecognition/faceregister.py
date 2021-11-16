"""
Implements Face Register and encapsulate into a class
"""

import os
import cv2
import numpy as np

class FaceRegister:
    def __init__(self, NUM_IMGS = 400):
        """
        Initialize FaceRegister

        Keyword Argument:

        NUM_IMGS: Number of images captured for this user
        """
        self.NUM_IMGS = NUM_IMGS

    def capture(self, id:int):
        """
        Capture the images

        Keyword Argument:

        id: customer_id, the id of user
        """
        # Initialize Camera
        video_capture = cv2.VideoCapture(0)

        # Create Folder
        if not os.path.exists('FaceRecognition/data/{}'.format(id)):
            os.mkdir('FaceRecognition/data/{}'.format(id))

        for i in range(self.NUM_IMGS):
            # Capture frame-by-frame
            ret, frame = video_capture.read()
            cv2.imwrite("FaceRecognition/data/{}/{}{:03d}.jpg".format(id, id, i), frame)

        video_capture.release()

    def train(self):
        """
        Train the model
        """
        # Get directory
        BASE_DIR = os.path.dirname(os.path.abspath("__file__"))+"/FaceRecognition/"
        image_dir = os.path.join(BASE_DIR, "data")

        # Load the OpenCV face recognition detector Haar
        face_cascade = cv2.CascadeClassifier('FaceRecognition/haarcascade/haarcascade_frontalface_default.xml')
        # Create OpenCV LBPH recognizer for training
        recognizer = cv2.face.LBPHFaceRecognizer_create()

        y_label = []
        x_train = []

        # Traverse all face images in `data` folder
        for root, dirs, files in os.walk(image_dir):
            # This is second-level folder system
            for file in files:
                # file is str
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    id_ = int(file[:-7])

                    # Convert Image to Numpy Array
                    image_array = cv2.imread(path)
                    image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
                    # Detect Faces
                    faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=3)

                    # Add to labels
                    for (x, y, w, h) in faces:
                        roi = image_array[y:y+h, x:x+w]
                        x_train.append(roi)
                        y_label.append(id_)

        # Train the recognizer and save the trained model.
        recognizer.train(x_train, np.array(y_label))
        recognizer.save("FaceRecognition/train.yml")

    def register(self, id:int):
        """
        An wrapper API, equivalent to call capture(id) and train()
        """
        self.capture(id)
        self.train()

#if __name__ == "__main__":
#    faceRegister = FaceRegister()
#    faceRegister.register(6)