# RUN:
# To read and write back out to video:
# python passenger_counter.py --mode vertical \
# 	--input videos/vertical_01.mp4 --output output/vertical_01.avi
#
# To read from webcam and write back out to disk:
# python passenger_counter.py --mode vertical \
# 	--output output/webcam_output.avi
#
# To run based on live feed:
# python passenger_counter.py

import DirectionTracker
import CentroidTracker
import TrackObject
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import Value
import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import time
import cv2

# def write_video(outputPath, writeVideo, frameQueue, W, H):
# 	# initialize FourCC and video writer object
# 	fourcc = cv2.VideoWriter_fourcc(*"MJPG")
# 	writer = cv2.VideoWriter(outputPath, fourcc, 30,
# 		(W, H), True)

# 	# loop while write flag is set or output frame queue is not empty
# 	while writeVideo.value or not frameQueue.empty():
# 		# check if the output frame queue is not empty
# 		if not frameQueue.empty():
# 			# get the frame from the queue and write the frame
# 			frame = frameQueue.get()
# 			writer.write(frame)

# 	# release the video writer object
# 	writer.release()

# construct argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-m", "--mode", type=str, required=True,
# 	choices=["horizontal", "vertical"],
# 	help="direction in which people will be moving")
ap.add_argument("-i", "--input", type=str,
	help="path to optional input video file")
ap.add_argument("-o", "--output", type=str,
	help="path to optional output video file")
ap.add_argument("-s", "--skip-frames", type=int, default=30,
	help="# of skip frames between detections")
args = vars(ap.parse_args())

# if a video path was not supplied, use webcam
if not args.get("input", False):
	print("[INFO] starting video stream...")
	# vs = VideoStream(src=0).start()
	vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

# else, reference a video file
else:
	print("[INFO] opening video file...")
	vs = cv2.VideoCapture(args["input"])

# initialize video writing process object and frame dimensions
writerProcess = None
W = None
H = None

# instantiate our centroid tracker, then initialize a list to store
# each of our dlib correlation trackers, followed by a dictionary to
# map each unique object ID to a track object
ct = CentroidTracker(maxDisappeared=15, maxDistance=100)
trackers = []
trackableObjects = {}

# initialize variable to store direction information(up/down, left/right)
directionInfo = None

# initialize MOG foreground background subtractor and start the FPS throughput estimator
mog = cv2.bgsegm.createBackgroundSubtractorMOG()
fps = FPS().start()

# loop over frames from video stream
while True:
	# read from VideoCapture or VideoStream till we reach the last frame
	frame = vs.read()
	frame = frame[1] if args.get("input", False) else frame

	if args["input"] is not None and frame is None:
		break

	# set object frame dimensions and direction counter
	if W is None or H is None:
		(H, W) = frame.shape[:2]
		dc = DirectionCounter(args["mode"], H, W)

	# # begin writing the video to disk if required
	# if args["output"] is not None and writerProcess is None:
	# 	# set write flad
	# 	writeVideo = Value('i', 1)
	# 	
	# 	# initialize a process, and start the process
	# 	frameQueue = Queue()
	# 	writerProcess = Process(target=write_video, args=(
	# 		args["output"], writeVideo, frameQueue, W, H))
	# 	writerProcess.start()

	# initialize list for bounding box rectangles after background subtraction
	rects = []

	# convert frame to grayscale and smoothen it using a gaussian kernel
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)

	# apply MOG background subtraction model
	mask = mog.apply(gray)

	# apply a series of erosions to reduce noise and find contours
	erode = cv2.erode(mask, (7, 7), iterations=2)
	cnts = cv2.findContours(erode.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# looping over contours
	for c in cnts:
		# ignore object if contour length than set minimum
		if cv2.contourArea(c) < 2000:
			continue

		# compute bounding box coordinates of contour
		(x, y, w, h) = cv2.boundingRect(c)
		(startX, startY, endX, endY) = (x, y, x + w, y + h)

		# add bounding box coordinates to rectangles list
		rects.append((startX, startY, endX, endY))

	# This line will be set co-ordinates for our project
	#  check if direction is vertical
	# if args["mode"] == "vertical":
	# 	# draw a horizontal line in the center of the frame - go up or down
	# 	cv2.line(frame, (0, H // 2), (W, H // 2), (0, 255, 255), 2)

	# # else, the direction is horizontal
	# else:
	# 	# draw a vertical line in the center of the frame - go left or right
	# 	cv2.line(frame, (W // 2, 0), (W // 2, H), (0, 255, 255), 2)

	# associate old object centroids with newly input object centroids
	objects = ct.update(rects)

	# loop over object list using their objectID
	for (objectID, centroid) in objects.items():
		to = trackableObjects.get(objectID, None)
		color = (0, 0, 255)

		# create a new track object if needed
		if to is None:
			to = TrackObject(objectID, centroid)

		# find direction and update list of centroids
		else:
			dc.find_direction(to, centroid)
			to.centroids.append(centroid)

			# if not counted aleady, find movement direction
			if not to.counted:
				directionInfo = dc.count_object(to, centroid)

			# else, update colour to red to indicate object has been counted
			else:
				color = (255, 0, 0)

		# store trackable object in our dictionary
		trackableObjects[objectID] = to

		# draw objectID and centroid on the output
		text = "ID {}".format(objectID)
		cv2.putText(frame, text, (centroid[0] - 10,	centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
		cv2.circle(frame, (centroid[0], centroid[1]), 4, color, -1)

	# get passenger counts and write/draw them
	if directionInfo is not None:
		for (i, (k, v)) in enumerate(directionInfo):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

	# put frame in shared queue for video writing - don't need this if we don't want a video output
	if writerProcess is not None:#
		frameQueue.put(frame)

	# show output
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# exit if 'q' clicked
	if key == ord("q"):
		break

	# update FPS counter - might not need FPS counter
	fps.update()

# stop timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# # terminate video writer process
# if writerProcess is not None:
# 	writeVideo.value = 0
# 	writerProcess.join()

# if we are not using a video file, stop the camera video stream
if not args.get("input", False):
	vs.stop()

# otherwise, release the video file pointer
else:
	vs.release()

# close all windows
cv2.destroyAllWindows()