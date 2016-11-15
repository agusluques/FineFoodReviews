from numpy import *

class Cluster(object):
	"""docstring for Cluster"""
	def __init__(self, centroid, metric, k):
		super(Cluster, self).__init__()
		self.centroid = centroid
		self.metric = metric
		self.k = k
		self.points = []

	def dist(self, point):
		return self.metric(self.centroid, point)

	def append(self, point):
		self.points.append(point)
	
	def update(self):
		avg = sum([p[1] for p in self.points])
		avg = array(avg, float)
		avg = avg / len(self.points)
		

# kc: cantidad de clusters
# kn: cantidad de vecinos en knn
# m: metrica a usar
def kmeans(kc, kn, m):
	# train es una lista de tuplas del tipo (l,p)
	# donde l es el label del punto p
	train, test = load_data()
	centroids = load_centroids(train, kc)
	clusters = [Cluster(c, m, kn) for c in centroids]

	# Training
	for t in train:
		_, cluster = min([(c.dist(t[1]), c) for c in clusters])
		cluster.append(t)
		cluster.update()

	# Testing
	result = []
	for t in test:
		_, cluster = min([(c.dist(t), c) for c in clusters])
		result.append(cluster.knn(t))

	return result