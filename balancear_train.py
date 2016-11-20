import csv

def balancear_train():
	auxin = open("train_clean.csv")
	auxout = open("train_balanceado.csv", "wb")

	archin = csv.reader(auxin)
	archout = csv.writer(auxout)
	archout.writerow(next(archin))
	i = 0
	for line in archin:
		if ((line[6] == '5') and (i < 70000)):
			archout.writerow(line)
			i += 1
		elif ((line[6] == '5') and (i >= 70000)):
			pass
		elif (line[6] != '5'):
			archout.writerow(line)

balancear_train()