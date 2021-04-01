import os
import cv2


script_dir = os.path.dirname(__file__)
rel_path_data = "dataset"
abs_path_dataset = os.path.join(script_dir, rel_path_data)

class DataManager:


	def __init__(self):
		self.targetName = None
		super(DataManager,self)


	def setTarget(self, name):
		self.targetName = name
		print(self.targetName)


	def saveImage(self, image):

		count = 0

		relPath = abs_path_dataset + "/" + self.targetName
		imageDir = os.path.join(script_dir, relPath)

		if not os.path.exists(imageDir):
			os.makedirs(imageDir)

		for root, dirs, files in os.walk(imageDir):
			for file in files:
				if file.endswith("png"):
					count = count + 1




		try:
			p = os.path.sep.join([relPath, "{}.png".format(str(count).zfill(5))])
			print(p)
			cv2.imwrite(p,image)
			return 1
		except:
			return 0

