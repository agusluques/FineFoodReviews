from numpy import *
def load_csv(fname, otype):
	if otype == "int" or otype == "float":
		return genfromtxt(open(fname, "rb"), dtype=otype, delimiter=',')

	return None
def save_csv(data, fname):
	to_write = open(fname, "w")
	for d in data:
		line = [str(i) for i in d]
		line = ",".join(line)
		to_write.write(line+'\n')

	to_write.close()