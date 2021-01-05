class TrackableObject:
	def __init__(self, objectID, centroid):
		# stocam un id si o lista de centeroizi
		self.objectID = objectID
		self.centroids = [centroid]

		# booleana pentru a contoriza daca obiectul curent a fost numarat
		self.counted = False
