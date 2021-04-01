import imutils
import time
import cv2
import sys, os


from imutils.video import VideoStream
from imutils.video import FPS
import asyncio

script_dir = os.path.dirname(__file__)
sys.path.append('..')
sys.path.append(os.path.abspath(os.path.join(script_dir, 'utils')))
from utils import Pipeline

OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}



async def producer(image, pipeline, event):
    while not event.is_set():
        logging.info("Producer income")
        await pipeline.setImage(image, "Producer")
    logging.info("Producer received EXIT event. Exiting")




async def consumer(pipeline, event):

    while not event.is_set() or not pipeline.empty():

        target = await pipeline.getImage("Consumer")

        logging.info("Consumer is processing image, (queue size=%s)", pipeline.qsize())

        (x,y,w,h) = run(target)
        print(x,y,w,h)

    logging.info("Consumer received EXIT event. Exiting")



class Tracking:


	def __init__(self, _typeTracker):
		global OPENCV_OBJECT_TRACKERS
		self.tracker = OPENCV_OBJECT_TRACKERS[_typeTracker]()
		self.initBB = None
		self.fps = None
		super(Tracking, self)




	def produce_consume_lock(self, image):
		logging.basicConfig(format=format, level=logging.INFO, datefmt = "%H:%M:%S")
		pipeline = Pipeline.Pipeline()
		event = threading.Event()

		with concurrunt.futures.ThreadPoolExecutor(max_workers=2) as executor:
			executor.submit(producer, image, pipeline, event)
			executor.submit(consumer, pipeline, event)

			time.sleep(0.1)
			logging.info("Main Thread: set event")
			event.set()


	def run(self, frame):

		x = None;
		y = None;
		w = None;
		h = None;

		if frame is None:
			return

		(W,H) = frame.shape[:2]

		if self.initBB is not None:
			(success, box) = tracker.update(frame)

			if success:
				(x, y, w, h) = [int(v) for v in box]
				cv2.rectangle(frame, (x, y), (x + w, y + h),
					(0, 255, 0), 2)

		self.fps.update()
		self.fps.stop()

		return (x,y,w,h)


	def setROI(self, startX, startY, endX, endY, frame):

		self.initBB = frame[startX:endX, startY:endY]

		self.tracker.init(frame, initBB)
		self.fps = FPS().start()


	def getFPS():

		 return "{:.2f}".format(self.fps.fps())

