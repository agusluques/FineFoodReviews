from sys import *
from os.path import *
from random import *
from loadcsv import *

def find_next_prime(n):
    return find_prime_in_range(n, 2*n)

def find_prime_in_range(a, b):
    for p in range(a, b):
        for i in range(2, p):
            if p % i == 0:
                break
        else:
            return p
	return None

def gen_fhash(m):
	p = find_next_prime(m)
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
	train = load_csv("train_clean.csv", "str")
	test = load_csv("test_clean.csv", "str")
	fhash = gen_fhash(dim)	
	test_tht = []
	train_tht = []
	for t in train[1:]:
		vtext = tovect(fhash, t[3], dim)
		train_tht.append(([t[6]] + vtext))

	save_csv(train_tht, train_name)
	for t in test[1:]:
		vtext = tovect(fhash, t[2], dim)
		test_tht.append([t[0]] + vtext)

	save_csv(test_tht, test_name)
