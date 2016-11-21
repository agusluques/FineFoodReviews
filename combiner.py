import csv
from sys import *

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
	prediccionesBayes = {}
	bayesCsv = csv.reader(bayes)
	kmeansCsv = csv.reader(kmeans)
	for linea in bayesCsv:
		prediccionesBayes[int(linea[0])] = float(linea[1])
	for linea in kmeansCsv:
		salida.write(linea[0])
		promedio = (float(linea[1]) * confiKmeans) + (prediccionesBayes[int(linea[0])] * confiBayes)
		salida.write(",")
		salida.write(str(promedio))
		salida.write("\n")
	bayes.close()
	kmeans.close()
	salida.close()

def diferencia_cuadrada(archivoPredicciones,archivoOriginal):
	"""Devuelve la distancia entre una prediccion y el puntaje verdadero
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
		listaPredicciones.append(float(linea[1]))
	i = 0
	diferenciaTotal = 0
	for linea in originalCsv:
		diferencia = abs(listaPredicciones[i] - float(linea[6]))
		diferencia = diferencia**2
		diferenciaTotal = diferenciaTotal + diferencia
		i += 1
	return diferenciaTotal

def distancia_a_confiabilidad(distanciaBayes, distanciaKmeans):
	"""Toma la distancia entre una prediccion y el puntaje real de dos clasificadores
	devuelve los numeros de confiabilidad de cada uno en la forma (confiBayes, confiKmeans)"""
	suma = distanciaBayes + distanciaKmeans
	confiBayes = float(distanciaKmeans) / float(suma)
	confiKmeans = float(distanciaBayes) / float(suma)
	return (confiBayes, confiKmeans)

def distancia_predicciones(archivoPredicciones,archivoOriginal):
	"""Devuelve la division entre aciertos y reviews totales
	El archivo de predicciones debe ser el archivo para subir a kaggle
	El archivo original es la porcion del train que se uso para predecir (trainChico)"""
	predicciones = open(archivoPredicciones)
	original = open(archivoOriginal)
	next(predicciones)
	next(original)
	prediccionesCsv = csv.reader(predicciones)
	originalCsv = csv.reader(original)
	listaPredicciones = {}
	for linea in prediccionesCsv:
		listaPredicciones[int(linea[0])] = float(linea[1])
	total = 0
	aciertos = 0
	for linea in originalCsv:
		diferencia = abs(listaPredicciones[int(linea[0])] - float(linea[6]))
		if diferencia <= 1.0:
			aciertos += 1
		total += 1
	return float(aciertos) / float(total)


combiner("prediccionesBayes.csv", "prediccionesKmeans.csv", float(argv[1]), float(argv[2]), "prediccionesCombinadas.csv")