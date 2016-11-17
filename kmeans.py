from numpy import *
from os.path import *
from random import *

class Cluster(object):
	"""docstring for Cluster"""
	def __init__(self, centroid, metric, k):
		super(Cluster, self).__init__()
		self.centroid = centroid
		self.dim = len(centroid)
		self.k = k
		self.metric = metric
		self.points = [centroid]

	def dist(self, point):
		return self.metric(self.centroid, point)

	def append(self, point):
		self.points.append(point)
	
	def update(self):
		avg = array([0] * self.dim)
		for p in self.points:
			avg += p[1]

		self.centroid = avg / float(len(self.points))

	def knn(self, point):
		dists = [(self.metric(p[1], point), p[0]) for p in self.points]
		dists = sorted(dists, key = lambda d: d[0])
		dists = dists[:self.k]
		return mean([d[1] for d in dists])

def gen_data():
	test = load_csv("test_kmeans.csv")
	train = load_csv("train_kmeans.csv")
	train = [(t[0], t[1:]) for t in train]
	return train, test
	
def gen_centroids(train, kc, m):
	centroids_file = "centroids_"+str(kc)+".csv"
	if isfile(centroids_file):
		return load_csv(centroids_file)

	f = randint(0,len(train))
	centroids = [f]
	for _ in range(1, kc):
		min_dist = []
		for i in range(len(train)):
			dist = [(m(train[i][1], train[j][1]), i) for j in centroids]
			min_dist.append(min(dist))

		sum_dist = sum([d[0] for d in min_dist])
		_, centroid = max([(d[0] / sum_dist, d[1]) for d in min_dist])
		centroids.append(centroid)

	centroids = [train[i] for i in centroids]
	save_csv(centroids, centroids_file)
	return centroids

# kc: cantidad de clusters
# kn: cantidad de vecinos en knn
# m: metrica a usar
def kmeans(kc, kn, m):
	# train es una lista de tuplas del tipo (l,p)
	# donde l es el label del punto p.
	# p es un array defido por numpy
	train, test = gen_data()
	centroids = gen_centroids(train, kc, m)
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