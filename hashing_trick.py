from sys import *
from os.path import *
from random import *
from loadcsv import *
from clean_text import *
import csv

def gen_fhash(m):
	p = m
	a = randint(1, p-1)
	b = randint(0, p-1)
	fhashint = lambda x: int((((a * x + b) % p) % m))
	def fhashstr(x):
		hashx = sum([hash(x[i]) * a**i for i in range(len(x))])
		hashx = hashx % p
		return fhashint(hashx)
	
	return fhashstr

def tovect(fhash, text, vtxt):
	for w in text.split(" "):
		if len(w) <= 1: continue
		fhashw = fhash(w)
		vtxt[fhashw] += 1 if fhashw % 2 == 0 else -1

def hashing_trick(dim, test_name, train_name):
	train_file = "train_clean.csv"
	test_file = "test_clean.csv"
	if not isfile(train_file) or not isfile(test_file):
		clean_text()

	test_tht = []
	train_tht = []
	fhash = gen_fhash(dim)
	with open(train_file, "rb") as csvfile:
		datareader = csv.reader(csvfile, delimiter=',')
		datareader.next()
		for d in datareader:
			vtxt = [0] * dim
			tovect(fhash, d[9], vtxt)
			tovect(fhash, d[8], vtxt)
			train_tht.append([d[6]] + vtxt)

		save_csv(train_tht, train_name)

	with open(test_file, "rb") as csvfile:
		datareader = csv.reader(csvfile, delimiter=',')
		datareader.next()
		for d in datareader:
			vtxt = [0] * dim
			tovect(fhash, d[8], vtxt)
			tovect(fhash, d[7], vtxt)
			test_tht.append([d[0]] + vtxt)

		save_csv(test_tht, test_name)
