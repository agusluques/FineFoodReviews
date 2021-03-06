from kmeans import *
from loadcsv import *

def test_kmeans(dim, kc, kn, m):
	result = kmeans(dim, kc, kn, m)
	title = "prediccionesKmeans.csv"
	save_csv(result, title)

metric = lambda a,b: linalg.norm(a-b)
test_kmeans(int(argv[1]), int(argv[2]), int(argv[3]), metric)