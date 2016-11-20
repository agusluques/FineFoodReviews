from numpy import *
def load_csv(fname, otype):
	if otype != None:
		return genfromtxt(open(fname, "rb"), comments="\\",delimiter=',', dtype=otype)

	to_read = open(fname, "rb")
	data = [r.split(',') for r in to_read]
	to_read.close()
	return data

def save_csv(data, fname):
	to_write = open(fname, "w")
	for d in data:
		line = [str(i) for i in d]
		line = ",".join(line)
		to_write.write(line+'\n')

	to_write.close()