from numpy import *
def load_csv(fname, otype):
	return genfromtxt(fname, delimiter=",", dtype=otype)

def save_csv(data, fname):
	to_write = open(fname, "w")
	for d in data:
		line = [str(i) for i in d]
		line = ",".join(line)
		to_write.write(line+'\n')

	to_write.close()