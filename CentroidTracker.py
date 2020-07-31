from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np

class CentroidTracker:
	def __init__(self, maxNumOfFrames=60, maxDistance=60):
		# initialize next unique objectID and two ordered dicts to map object ID to its centroid and number of consecutive frames it has been out of frame
		self.nextObjectID = 0
		self.objects = OrderedDict()
		self.outOfFrame = OrderedDict()

		# store maximum number of frames an object is allowed to be out of frame till we stop tracking it
		self.maxNumOfFrames = maxNumOfFrames

		# store maximum distance between centroids to still match an object -- if distance larger than maxDistance, mark as outOfFrame
		self.maxDistance = maxDistance

	def addObject(self, centroid):
		# to add an object, use the next unique objectID to store centroid
		self.objects[self.nextObjectID] = centroid
		self.outOfFrame[self.nextObjectID] = 0
		self.nextObjectID += 1

	def deleteObject(self, objectID):
		# to stop tracking an object, delete objectID from dictionaries
		del self.objects[objectID]
		del self.outOfFrame[objectID]

	def update(self, rects):
		# check if input bounding boxes are 0
		if len(rects) == 0:
			# add outOfFrame objects to a list
			for objectID in list(self.outOfFrame.keys()):
				self.outOfFrame[objectID] += 1

				# if object has been out of frame for maxNoOfFrames, stop tracking
				if self.outOfFrame[objectID] > self.maxNumOfFrames:
					self.deleteObject(objectID)

			# return since no centroids or additional info
			return self.objects

		# initialize array to keep track of inputCentroids
		inputCentroids = np.zeros((len(rects), 2), dtype="int")

		# loop over bounding box rectangles and calculate centroids
		for (i, (startX, startY, endX, endY)) in enumerate(rects):
			cX = int((startX + endX) / 2.0)
			cY = int((startY + endY) / 2.0)
			inputCentroids[i] = (cX, cY)

		# if number of objects being tracked = 0, add all inputCentroids
		if len(self.objects) == 0:
			for i in range(0, len(inputCentroids)):
				self.addObject(inputCentroids[i])

		# else, match inputCentroids to currently being tracked objectCentroids
		else:
			#get currently tracked object ID's and their centroid information
			objectIDs = list(self.objects.keys())
			objectCentroids = list(self.objects.values())

			# calculate distance between each pair of currently tracked object centroids and input centroids
			D = dist.cdist(np.array(objectCentroids), inputCentroids)

			# To match input centroids with object centroids:
			# (1) find smallest value in each row, (2) sort the row indexes in ascending order
			rows = D.min(axis=1).argsort()

			# Repeat for columns by finding smallest value in each column and sorting based on row indexes
			cols = D.argmin(axis=1)[rows]

			# keep track of indexes we've already looked at
			checkedRows = set()
			checkedCols = set()

			# loop through (row, column) index tuples
			for (row, col) in zip(rows, cols):
				# if already looked, ignore
				if row in checkedRows or col in checkedCols:
					continue

				# if distance between centroids > maximum distance, do nothing
				if D[row, col] > self.maxDistance:
					continue

				# else, grab object ID for curr row, set a new centroid, and reset the outOfFrame counter
				objectID = objectIDs[row]
				self.objects[objectID] = inputCentroids[col]
				self.outOfFrame[objectID] = 0

				# add to used row and column lists once we've looked at them
				checkedRows.add(row)
				checkedCols.add(col)

			# calculate row and column index not yet looked at
			uncheckedRows = set(range(0, D.shape[0])).difference(checkedRows)
			uncheckedCols = set(range(0, D.shape[1])).difference(checkedCols)

			# if num of object centroids >= num of input centroids, check if any objects are outOfFrame
			if D.shape[0] >= D.shape[1]:
				# loop over row indexes not looked at, and get objectID and increment outOfFrame counter
				for row in uncheckedRows:
					objectID = objectIDs[row]
					self.outOfFrame[objectID] += 1

					# if object outOfFrame for maxNumOfFrames, stop tracking object
					if self.outOfFrame[objectID] > self.maxNumOfFrames:
						self.deleteObject(objectID)

			# else, if num of input centroids > num of existing object centroids, track new input centroids
			else:
				for col in uncheckedCols:
					self.addObject(inputCentroids[col])

		# return set of objects being tracked
		return self.objects