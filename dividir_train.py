import csv

def partir_train(archivoTrain, salidaTrainGrande, salidaTrainChico, i):
	"""Toma un archivo de train y lo divide. i es el numero que indica la proporcion.
	i: cada i lineas del train, una se va a escribir en el chico, el resto en el grande."""
	trainOriginal = open(archivoTrain)
	encabezado = next(trainOriginal)
	trainGrande = open(salidaTrainGrande, "w")
	trainChico = open(salidaTrainChico, "w")
	trainGrande.write(encabezado)
	trainChico.write(encabezado)
	x = 0
	for linea in trainOriginal:
		if x % i == 0:
			trainChico.write(linea)
		else:
			trainGrande.write(linea)
		x += 1
	trainOriginal.close()
	trainGrande.close()
	trainChico.close()

def sacar_puntaje(archivoTrain, archivoSalida):
	"""Toma un archivo de train y escribe uno nuevo pero sin el puntaje
	Sirve para poder hacer predicciones como si fuera un set de test"""
	train = open(archivoTrain)
	encabezado = next(train)
	salida = open(archivoSalida, "w")
	salida.write(encabezado)
	trainCsv = csv.reader(train)
	for linea in trainCsv:
		for i in range(9):
			if i == 6:
				continue
			if i in (1,2,8):
				salida.write('"' + linea[i] + '",')
			elif i == 3:
				user = "".join(char for char in linea[i] if char.isalpha() or char == " ") #Saco las comas al usuario
				salida.write('"' + user + '",')
			else:
				salida.write(linea[i] + ',')
		salida.write('"' + linea[9] + '"\n')
	train.close()
	salida.close()

partir_train("trainLimpio.csv","trainGrande.csv","trainChico.csv",5)
sacar_puntaje("trainChico.csv", "trainChicoSinPuntaje.csv")