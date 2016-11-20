from numpy import *
from os.path import *
from sys import *
from random import *
from hashing_trick import *
from loadcsv import *

class Cluster(object):
	"""docstring for Cluster"""
	def __init__(self, centroid, metric, k):
		super(Cluster, self).__init__()
		self.centroid = array(centroid, dtype(float))
		self.dim = len(centroid)
		self.k = k
		self.metric = metric
		self.points = []

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

def gen_data(dim):
	test_name = "testin"+str(dim)+"dim.csv"
	train_name = "trainin"+str(dim)+"dim.csv"
	if not isfile(train_name) or not isfile(test_name):
		hashing_trick(dim, test_name, train_name)

	train = load_csv(train_name, "int")
	train = [(t[0], t[1:]) for t in train]
	test = load_csv(test_name, "int")
	test = [(t[0], t[1:]) for t in test]
	return train, test

def gen_centroids(train, kc, m):
	centroids_name = str(kc) + "centroids.csv"
	if isfile(centroids_name):
		return load_csv(centroids_name, "int")

	f = randint(0, len(train))
	centroids = [f]
	for _ in range(1, kc):
		min_dist = []
		for i in range(len(train)):
			dist = [(m(train[i][1], train[j][1]), i) for j in centroids]
			min_dist.append(min(dist))

		sum_dist = sum([d[0] for d in min_dist])
		_, centroid = max([(d[0] / sum_dist, d[1]) for d in min_dist])
		centroids.append(centroid)

	centroids = [train[i][1] for i in centroids]
	save_csv(centroids, centroids_name)
	return centroids

# dim: dimension de los datos tras aplicar hashing trick
# kc: cantidad de clusters
# kn: cantidad de vecinos en knn
# m: metrica a usar
def kmeans(dim, kc, kn, m):
	# train es una lista de tuplas del tipo (label,point)
	# test es una lista de tuplas del tipo (id,point)
	train, test = gen_data(dim)
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
		_, cluster = min([(c.dist(t[1]), c) for c in clusters])
		result.append((int(t[0]), cluster.knn(t[1])))

	return result

metric = lambda a,b: linalg.norm(a-b)
print kmeans(int(argv[1]), int(argv[2]), int(argv[3]), metric)