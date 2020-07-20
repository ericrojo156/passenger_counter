import numpy as np

class DirectionTracker:
	def __init__(self, directionMode, H, W):
		# initialize height and width of input image
		self.H = H
		self.W = W

		# initialize direction variables
		self.directionMode = directionMode
		self.totalUp = 0
		self.totalDown = 0
		self.totalRight = 0
		self.totalLeft = 0

		# initialize object direction
		self.direction = ""

	def find_direction(self, to, centroid):
		# difference between x-coordinate of current centroid position and the mean of *previous* centroids, will give us object direction 
		# if difference = negative -> direction = 'left' and if difference is positive -> direction = 'right'
		# if object is moving horizontally		
		if self.directionMode == "horizontal":

			x = [c[0] for c in to.centroids]
			difference = centroid[0] - np.mean(x)

			if difference < 0:
				self.direction = "left"

			elif difference > 0:
				self.direction = "right"

		# difference between y-coordinate of current centroid position and the mean of *previous* centroids, will give us object direction 
		# if difference = negative -> direction = 'up' and if difference is positive -> direction = 'down'
		# else if object is moving vertically
		elif self.directionMode == "vertical":
			y = [c[1] for c in to.centroids]
			difference = centroid[1] - np.mean(y)

			if difference < 0:
				self.direction = "up"

			elif difference > 0:
				self.direction = "down"

	def count_object(self, to, centroid):
		# initialize final object count list
		output = []

		# if object is moving right or left, count it, update boolean counted and add total to a list
		if self.directionMode == "horizontal":
			leftOfCenter = centroid[0] < self.W // 2
			if self.direction == "left" and leftOfCenter:
				self.totalLeft += 1
				to.counted = True

			elif self.direction == "right" and not leftOfCenter:
				self.totalRight += 1
				to.counted = True

			output = [("Left", self.totalLeft),
				("Right",self.totalRight)]

		# else if object is moving up or down, count it, update boolean counted and add total to a list
		elif self.directionMode == "vertical":
			aboveMiddle = centroid[1] < self.H // 2
			if self.direction == "up" and aboveMiddle:
				self.totalUp += 1
				to.counted = True

			elif self.direction == "down" and not aboveMiddle:
				self.totalDown += 1
				to.counted = True

			output = [("Up", self.totalUp), ("Down", self.totalDown)]

		# return final output list of all objects
		return output