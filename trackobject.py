class TrackObject:
	def __init__(self, objectID, centroid):
		# store object ID and initialize a list of centroids
		self.objectID = objectID
		self.centroids = [centroid]

		# initialize a boolean to see if object is counted
		self.counted = False