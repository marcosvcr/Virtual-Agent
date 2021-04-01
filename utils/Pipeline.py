import threading
import time
import logging
import random
import queue
import asyncio


class Pipeline(queue.Queue):


	def __init__(self):
		super().__init__(maxsize = 10)


	async def setImage(self, image, message):
		logging.debug("%s:about to add %d to queue", name, value)
		self.put(image)
		logging.debug("%s:added %d to queue", name, value)


	async def getImage(self, message):
		logging.debug("%s:about to get from queue", name)
		image = self.get()
		logging.debug("%s:got %d from queue", name, value)
		return image