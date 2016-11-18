######################### IMPORTANTE ##########################
#### Deben usarse los archivos sinStop.csv y testLimpio.csv ###
#### que los genera el script limpiarTexto.py 				###
###############################################################

############# imports #################
import csv
import mmap
import pyspark
from nltk.corpus import wordnet as wn
#######################################

#############  pyspark sc ############# 
try: 
    type(sc)
except NameError:
    sc = pyspark.SparkContext('local[*]')
#######################################

#############   TRAIN ############# 

listaAdj = {}	#creo diccionario

listaNegaciones = ['not', 'wasnt', 'arent', 'isnt' ,'werent',"aren't", "isn't", "wasn't"]
### en el diccionario pongo todos los adjetivos con un 1 como valor
### esto lo hago para poder buscar en O(1)
for synset in list(wn.all_synsets('a')):
	for lemma in synset.lemmas():
		palabra = lemma.name()
		for word in listaNegaciones:
			listaAdj[word+lemma.name()] = 1
		listaAdj[lemma.name()] = 1

with open("sinStop.csv","rb") as src:
	file= csv.reader( src )
	with open("trainLimpioSinCol.csv","wb") as result:
		fileDst= csv.writer( result )
		file.next()	# salteo la primer linea que tiene los nombres
		listaPalabras = []
		for row in file:
			for word in row[9].split(): #para cada palabra de la columna TEXT
				if word in listaAdj:
					#fileDst.writerow( (row[6], word) )  		#si esta en la lista de adjetivos
					listaPalabras.append((int(row[6]), word)) 	#la escribo tipo Puntaje, Palabra

		listaRDD = sc.parallelize(listaPalabras, 8)
		listaRDD = listaRDD.map(lambda x: (x[1],(1, x[0])))		#(palabra, (1, puntaje))
		#print listaRDD.take(10)
		listaRDD = listaRDD.reduceByKey(lambda x,y: (x[0] + y[0], x[1] + y[1]))
		#print listaRDD.take(10)
		listaRDD = listaRDD.map(lambda x: (x[0], float(x[1][1]) / float(x[1][0]))) #(palabra, promedio_puntaje)
		print listaRDD.take(2000)
#######################################



########### TEST ################
with open("testLimpio.csv", "rb") as src:
	test = csv.reader (src)
	test.next()
	listaTest = []
	for row in test:
		listaTest.append((row[0], row[8].split())) #(id, [texto])

	listaTestRDD = sc.parallelize(listaTest, 8)
	print listaTestRDD.take(1)
	
	listaTestRDD = listaTestRDD.flatMapValues(lambda x: x) #(id, palabra)
	listaTestRDD = listaTestRDD.map(lambda x: (x[1], x[0])) #(palabra, id)
	listaTestRDD = listaTestRDD.leftOuterJoin(listaRDD) #(palabra, (id, puntaje)) si existe,
														#(palabra,(id, NONE)) si no existe
	
	listaTestRDD = listaTestRDD.values() #(id, puntaje) o (id, NONE)

	#aca si no tiene puntaje, es decir, no se encuentra en la lista de palabras del train, no se 
	#tiene en cuenta y si tiene puntaje se le asigna ese mismo.
	#queda (id, (puntaje, 1))
	listaTestRDD = listaTestRDD.map(lambda x: (int(x[0]), (x[1], 1) if x[1] is not None else (0, 0)))

	listaTestRDD = listaTestRDD.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1])) #(id, (sumaPuntaje, sumaPalabras))
	listaTestRDD = listaTestRDD.mapValues(lambda x: x[0] / float(x[1]) if x[1] else 3.0) #(id, promedio)
	
#############################################

######### guardo en archivo para subir a kaggle #############
listaTest = listaTestRDD.sortByKey().collect()

with open("predicciones.txt", "wb") as out:
	csvOut = csv.writer(out)
	csvOut.writerow(['Id','Prediction'])
	for linea in listaTest:
		csvOut.writerow(linea)
		
#############################################################



 



