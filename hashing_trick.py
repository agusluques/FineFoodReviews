from sys import *
from os.path import *
from random import *
from loadcsv import *
from clean_text import *

def gen_fhash(m):
	p = m
	a = randint(1, p-1)
	b = randint(0, p-1)
	fhashint = lambda x: (((a * x + b) % p) % m)
	def fhashstr(x):
		hashx = sum([hash(x[i]) * a**i for i in range(len(x))])
		hashx = hashx % p
		return fhashint(hashx)
	
	return fhashstr

def tovect(fhash, text, dim):
	vtext = [0] * dim
	for w in text.split(" "):
		if len(w) <= 1: continue
		vtext[fhash(w)] += 1 if fhash(w) % 2 == 0 else -1

	return vtext


def hashing_trick(dim, test_name, train_name):
	train_file = "train_clean.csv"
	test_file = "test_clean.csv"
	if not isfile(train_file) or not isfile(test_file):
		clean_text()

	train = load_csv(train_file, None)
	test = load_csv(test_file, None)
	fhash = gen_fhash(dim)	
	test_tht = []
	train_tht = []
	for t in train[1:]:
		vtext = tovect(fhash, t[9], dim)
		train_tht.append(([t[6]] + vtext))

	save_csv(train_tht, train_name)
	for t in test[1:]:
		vtext = tovect(fhash, t[8], dim)
		test_tht.append([t[0]] + vtext)

	save_csv(test_tht, test_name)
