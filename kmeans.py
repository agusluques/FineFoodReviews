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
		self.sum_points = [0] * self.dim

	def dist(self, point):
		return self.metric(self.centroid, point)

	def append(self, point):
		self.points.append(point)
		self.sum_points += point[1]


	def update(self):
		self.centroid = self.sum_points / float(len(self.points))

	def knn(self, point):
		dists = min([(self.metric(p[1], point), p[0]) for p in self.points])
		return dists[1]

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

def gen_centroids(train, kc, dim, m):
	centroids_name = "centroids"+str(kc)+str(dim)+".csv"
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

def save_clusters(clusters, dim, kc):
	centroids_name = "centroids"+str(kc)+str(dim)+".csv"
	centroids = [c.centroid for c in clusters]
	save_csv(centroids, centroids_name)

	to_save = []
	for i in range(len(clusters)):
		points = clusters[i].points
		for p in points:
			c = [i, p[0]] + list(p[1])
			to_save.append(c)

	kmeans_trained = "kmeans_trained" + str(dim) + str(kc) + ".csv"
	save_csv(to_save, kmeans_trained)

def load_clusters(clusters, kmeans_trained):
	points = load_csv(kmeans_trained, "int")
	for p in points:
		clusters[p[0]].append((p[1], p[2:]))


# dim: dimension de los datos tras aplicar hashing trick
# kc: cantidad de clusters
# kn: cantidad de vecinos en knn
# m: metrica a usar
def kmeans(dim, kc, kn, m):
	# train es una lista de tuplas del tipo (label,point)
	# test es una lista de tuplas del tipo (id,point)
	print "Produciendo datos"
	train, test = gen_data(dim)
	print "Produciendo centroides y clusters"
	centroids = gen_centroids(train, kc, dim, m)
	clusters = [Cluster(c, m, kn) for c in centroids]

	# Training
	print "Entrenando el algortimo"
	kmeans_trained = "kmeans_trained" + str(dim) + str(kc) + ".csv"
	if isfile(kmeans_trained):
		print "Cargando kmeans trained"
		load_clusters(clusters, kmeans_trained)
	else:
		print "Cargando kmeans untrained"
		for t in train:
			_, cluster = min([(c.dist(t[1]), c) for c in clusters])
			cluster.append(t)
			cluster.update()
		print "Salvando Kmeans trained"
		save_clusters(clusters, dim, kc)

	# Testing
	print "Obteniendo resultados"
	result = []
	for t in test:
		_, cluster = min([(c.dist(t[1]), c) for c in clusters])
		result.append((int(t[0]), cluster.knn(t[1])))

	return result