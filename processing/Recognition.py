import numpy as np
import os
import cv2
import face_recognition
from sklearn import svm
import os


script_dir = os.path.dirname(__file__)
rel_path_dataset = "utils/dataset"
parent_path = os.path.abspath(os.path.join(script_dir, os.pardir))
abs_path_dataset = os.path.join(parent_path, rel_path_dataset)



class Recognition:

	def __init__(self):

		self.train_dir = os.listdir(abs_path_dataset)
		self.encodings = []
		self.names = []
		self.classifier = None

	def train(self):

		for person in self.train_dir:
			pix = os.listdir(abs_path_dataset + "/" +person)

			for person_img in pix:

				face = face_recognition.load_image_file(abs_path_dataset + "/" + person +"/" + person_img)
				face_bounding_boxes = face_recognition.face_locations(face)

				if len(face_bounding_boxes) == 1:

					face_enc = face_recognition.face_encodings(face)[0]

					self.encodings.append(face_enc)
					self.names.append(person)

				else:
					print(person + "/" + person_img + " was skipped and can't be used from training")

		self.classifier = svm.SVC(gamma ='scale')
		self.classifier.fit(self.encodings, self.names)


	def predict(self, img):

		result = []
		face_locations = face_recognition.face_locations(img)
		no = len(face_locations)
		print("Number of faces detected: ", no)
		for i in range(no):
			test_image_enc = face_recognition.face_encodings(img)[i]
			name = self.classifier.predict([test_image_enc])
			result.append(*name)

		print(result)
		return result

	def getPaths(self):
		print(abs_path_dataset)









