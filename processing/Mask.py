from tensorflow.python.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.python.keras.preprocessing.image import img_to_array
from tensorflow.python.keras.models import load_model
import numpy as np
import os
import cv2


script_dir = os.path.dirname(__file__)

rel_path_mask = "model/mask_detector.model"
abs_path_mask = os.path.join(script_dir,rel_path_mask)



class Mask:

	def __init__(self):

		print("[INFO] loading face mask detector model...")
		self.faces = []
		self.maskNet = load_model(abs_path_mask)
		super(Mask,self)


	def predict(self, img, faceDetections):
		self.faces.clear()
		(h, w) = img.shape[:2]
		for i in range(0, faceDetections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the detection
			confidence = faceDetections[0, 0, i, 2]

			# filter out weak detections by ensuring the confidence is
			# greater than the minimum confidence
			if confidence > 0.5:
				# compute the (x, y)-coordinates of the bounding box for
				# the object
				box = faceDetections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# ensure the bounding boxes fall within the dimensions of
				# the frame
				(startX, startY) = (max(0, startX), max(0, startY))
				(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

				# extract the face ROI, convert it from BGR to RGB channel
				# ordering, resize it to 224x224, and preprocess it
				face = img[startY:endY, startX:endX]
				face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
				face = cv2.resize(face, (224, 224))
				face = img_to_array(face)
				face = preprocess_input(face)
				face = np.expand_dims(face, axis=0)
				(mask, withoutMask) = self.maskNet.predict(face)[0]
				label = "Mask" if mask > withoutMask else "No Mask"
				thereIs = 1 if label == "Mask" else 0

				# add the face and bounding boxes to their respective
				# lists
				self.faces.append(thereIs)
		return (self.faces)
