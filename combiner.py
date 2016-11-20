import csv

def combiner(predictBayes,predictKmeans,confiBayes,confiKmeans,archivoSalida):
	"""Combina predicciones de dos clasificadores segun su numero de confiabilidad
	Para hacer un promedio comun, indicar 0.5 en ambos numeros de confiabilidad
	El formato de los archivos de entrada debe ser el de subida para kaggle"""
	bayes = open(predictBayes)
	kmeans = open(predictKmeans)
	encabezado = next(bayes)
	next(kmeans)
	salida = open(archivoSalida,"w")
	salida.write(encabezado)
	prediccionesBayes = []
	bayesCsv = csv.reader(bayes)
	kmeansCsv = csv.reader(kmeans)
	for linea in bayesCsv:
		prediccionesBayes.append(int(linea[1]))
	i = 0
	for linea in kmeansCsv:
		salida.write(linea[0])
		promedio = (int(linea[1]) * confiKmeans) + (prediccionesBayes[i] * confiBayes)
		salida.write(",")
		salida.write(str(promedio))
		salida.write("\n")
		i += 1
	bayes.close()
	kmeans.close()
	salida.close()

def distancia_predicciones(archivoPredicciones,archivoOriginal):
	"""Devuelve el la distancia entre una prediccion y el puntaje verdadero
	El archivo de predicciones debe ser el archivo para subir a kaggle
	El archivo original es la porcion del train que se uso para predecir (trainChico)"""
	predicciones = open(archivoPredicciones)
	original = open(archivoOriginal)
	next(predicciones)
	next(original)
	prediccionesCsv = csv.reader(predicciones)
	originalCsv = csv.reader(original)
	listaPredicciones = []
	for linea in prediccionesCsv:
		listaPredicciones.append(int(linea[1]))
	i = 0
	diferenciaTotal = 0
	for linea in originalCsv:
		diferencia = abs(listaPredicciones[i] - int(linea[6]))
		diferencia = diferencia**2
		diferenciaTotal = diferenciaTotal + diferencia
		i += 1
	return diferenciaTotal

def confiabilidades(distanciaBayes, distanciaKmeans):
	"""Toma la distancia entre una prediccion y el puntaje real de dos clasificadores
	devuelve los numeros de confiabilidad de cada uno en la forma (confiBayes, confiKmeans)"""
	suma = distanciaBayes + distanciaKmeans
	confiBayes = float(distanciaKmeans) / float(suma)
	confiKmeans = float(distanciaBayes) / float(suma)
	return (confiBayes, confiKmeans)

distBayes = distancia_predicciones("prediccionesBayes.csv", "trainChico.csv")
distKmeans = distancia_predicciones("prediccionesKmeans.csv", "trainChico.csv")
confi = confiabilidades(distBayes, distKmeans)
combiner("predictBayes.csv", "predictKmeans.csv", confi[0],confi[1],"prediccionesCombinadas.csv")

#prediccionesBayes.csv son las predicciones que se hicieron sobre el trainChico para obtener el confidence number
#predictBayes.csv son las predicciones reales que se hicieron sobre el test