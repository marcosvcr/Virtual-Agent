
import numpy as np
import os
import cv2

script_dir = os.path.dirname(__file__)
rel_path_proto = "model/deploy.prototxt.txt"
rel_path_model = "model/res10_300x300_ssd_iter_140000.caffemodel"
abs_path_model = os.path.join(script_dir, rel_path_model)
abs_path_proto = os.path.join(script_dir,rel_path_proto)


class Detection:


	def __init__(self):
		print("[INFO] loading model...")
		self.net = cv2.dnn.readNetFromCaffe(abs_path_proto, abs_path_model)
		super(Detection, self)


	def detect(self, img):

		# load our serialized model from disk

		# load the input image and construct an input blob for the image
		# by resizing to a fixed 300x300 pixels and then normalizing it
		(h, w) = img.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,
			(300, 300), (104.0, 177.0, 123.0))

		# pass the blob through the network and obtain the detections and
		# predictions
		print("[INFO] computing object detections...")
		self.net.setInput(blob)
		detections = self.net.forward()
		return detections