from numpy import *
from os.path import *
from sys import *
from random import *
from hashing_trick import *
from loadcsv import *
from heapq import *
from math import *

class Heap(object):
    """docstring for Heap."""
    def __init__(self):
        super(Heap, self).__init__()
        self.heap = []

    def push(self, arg):
        heappush(self.heap, (-arg[0], arg[1]))

    def pop(self):
        return heappop(self.heap)

    def pushAll(self, elements):
        self.heap = elements
        heapify(self.heap)

    def top(self):
        return self.heap[0]

    def pushpop(self, arg):
    	heappushpop(self.heap, (-arg[0], arg[1]))
    	

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
		heap = Heap()
		dists = [(self.metric(p[1], point), p[0]) for p in self.points]
		for d in dists[:self.k]:
			heap.push(d)

		for d in dists[self.k:]:
			heap.pushpop(d)
			
		return mean([d[1] for d in heap.heap])

def gen_data(dim):
	test_name = "testin"+str(dim)+"dim.csv"
	train_name = "trainin"+str(dim)+"dim.csv"
	if not isfile(train_name) or not isfile(test_name):
		hashing_trick(dim, test_name, train_name)

	train = []
	test = []
	with open(train_name, "rb") as csvfile:
		dataread = genfromtxt(csvfile, dtype="int", delimiter=",")
		for d in dataread:
			train.append((d[0], d[1:]))

	with open(test_name, "rb") as csvfile:
		dataread = genfromtxt(csvfile, dtype="int", delimiter=",")
		for d in dataread:
			test.append((d[0], d[1:]))

	return train, test

def gen_centroids(train, kc, dim, m):
	centroids_name = "centroids"+str(kc)+str(dim)+".csv"
	centroids = []
	if isfile(centroids_name):
		with open(centroids_name,"rb") as csvfile:
			dataread = genfromtxt(csvfile, dtype="float", delimiter=",")
			for d in dataread:
				centroids.append(d)

		return centroids

	centroids.append(randint(0, len(train)))
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

def save_clusters(clusters, clusters_file):
	to_save = []
	for i in range(len(clusters)):
		points = clusters[i].points
		for p in points:
			c = [i, p[0]] + list(p[1])
			to_save.append(c)

	save_csv(to_save, clusters_file)

def load_clusters(clusters, clusters_file):
	with open(clusters_file, "rb") as csvfile:
		dataread = genfromtxt(csvfile, dtype="int", delimiter=",")
		for d in dataread:
			clusters[d[0]].append((d[1], d[2:]))

	for c in clusters:
		c.update	

def gen_centroids_rnd(train, kc, dim):
	centroids_name = "centroidsrnd"+str(kc)+str(dim)+".csv"
	centroids = []
	if isfile(centroids_name):
		with open(centroids_name,"rb") as csvfile:
			dataread = genfromtxt(csvfile, dtype="float", delimiter=",")
			for d in dataread:
				centroids.append(d)

		return centroids

	for _ in range(kc):
		r = randint(0, len(train))
		centroids.append(train[r][1])
	
	save_csv(centroids, centroids_name)
	return centroids
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
	#centroids = gen_centroids(train, kc, dim, m)
	centroids = gen_centroids_rnd(train, kc, dim)
	clusters = [Cluster(c, m, kn) for c in centroids]

	# Training
	clusters_file = "clusters"+str(kc)+str(dim)+".csv"
	if isfile(clusters_file):
		print "Cargando clusters"
		load_clusters(clusters, clusters_file)
	else:
		print "Entrenando el algortimo"
		i = 0
		for t in train:
			i += 1
			print i
			_, cluster = min([(c.dist(t[1]), c) for c in clusters])
			cluster.append(t)
			cluster.update()

		save_clusters(clusters, clusters_file)

	# Testing
	print "Obteniendo resultados"
	result = []
	i = 0
	for t in test:
		print i 
		i += 1
		_, cluster = min([(c.dist(t[1]), c) for c in clusters])
		patron = cluster.knn(t[1])
		patron = patron if not isnan(patron) else 5.0
		result.append((int(t[0]), patron))

	return result