import csv
from HTMLParser import HTMLParser

STOPWORDS = {'a': 0, 'aboard': 0, 'about': 0, 'above': 0, 'across': 0, 'after': 0, 'against': 0, 'all': 0,
			'along': 0, 'an': 0, 'and': 0, 'and': 0, 'another': 0, 'any': 0, 'are': 0, 'around': 0,
			'as': 0,
			'at': 0, 'be': 0, 'been': 0, 
			'before': 0, 'behind': 0, 'below': 0, 'beneath': 0, 'beside': 0,
			'between': 0, 'beyond': 0, 'but': 0, 'by': 0, 'certain': 0, 'down': 0, 'during': 0,
			'each': 0, 'every': 0, 'except': 0, 'following': 0, 'for': 0, 'from': 0, 'had': 0,
			'have': 0, 'has': 0,
			'her': 0, 'his': 0, 'i': 0, 'if': 0, 'in': 0, 'inside': 0, 'into': 0, 'is': 0, 'it': 0, 'its': 0,
			'just': 0, 'my': 0, 'near': 0, 'next': 0, 'nor': 0, 'of': 0, 'on': 0, 'one': 0, 'onto': 0,
			'or': 0, 'our': 0, 'outside': 0, 'past': 0, 'since': 0, 'so': 0, 'some': 0, 'than': 0,
			'that': 0, 'the': 0, 'their': 0, 'them': 0, 'these': 0, 'they': 0, 'this': 0, 'through': 0,
			'to': 0, 'toward': 0, 'under': 0, 'underneath': 0, 'until': 0, 'upon': 0, 'was': 0, 'we': 0,
			'were':0,
			'with': 0, 'what':0, 'when': 0, 'where': 0, 'which':0, 'will': 0, 'yet': 0, 'you': 0,
			'your': 0}

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

def limpiarTexto(texto):
	espaciado = ''
	for char in texto:
		if char in ('.', ',', '>', '!', '?', ';', '/', ')', '-'):
			espaciado = espaciado + char + ' '
		else:
			espaciado += char
	sinHTML = strip_tags(espaciado) #Saco html
	sinCaracteresEspeciales = ''.join(char for char in sinHTML if char.isalpha() or char == " ") #Saco caracteres espciales
	minuscula = sinCaracteresEspeciales.lower() #Paso a minuscula
	sinStopwords = ' '.join(palabra for palabra in minuscula.split() if palabra not in STOPWORDS) #Saco conectores
	negacionUnida = ''
	ultimaPalabra = ''
	for palabra in sinStopwords.split(): #Si la ultima palabra era not, la uno con la proxima palabra
		if ultimaPalabra in ('not', 'wasnt', 'arent', 'isnt' ,'werent','dont', 'doesnt', 'aint'):
			negacionUnida += palabra
		else:
			negacionUnida += " "+palabra
		ultimaPalabra = palabra
	return negacionUnida

def limpiarTrain(entrada, salida):
	entrada = open(entrada)
	salida = open(salida, 'w')
	salida.write(entrada.next())
	entradaCSV = csv.reader(entrada)
	for linea in entradaCSV:
		resumen = linea[8]
		resumenLimpio = limpiarTexto(resumen)
		texto = linea[9]
		textoLimpio = limpiarTexto(texto)
		for i in range(8):
			if i in (1,2):
				salida.write('"' + linea[i] + '",')
			elif i == 3:
				user = "".join(char for char in linea[i] if char.isalpha() or char == " ") #Saco las comas al usuario
				salida.write('"' + user + '",')
			else:
				salida.write(linea[i] + ',')
		salida.write('"' + resumenLimpio + '",')
		salida.write('"' + textoLimpio + '"\r\n')
	entrada.close()
	salida.close()


def limpiarTest(entrada, salida):
	entrada = open(entrada)
	salida = open(salida, 'w')
	salida.write(entrada.next())
	entradaCSV = csv.reader(entrada)
	for linea in entradaCSV:
		resumen = linea[7]
		resumenLimpio = limpiarTexto(resumen)
		texto = linea[8]
		textoLimpio = limpiarTexto(texto)
		for i in range(7):
			if i in (1,2):
				salida.write('"' + linea[i] + '",')
			elif i == 3:
				user = "".join(char for char in linea[i] if char.isalpha() or char == " ") #Saco las comas al usuario
				salida.write('"' + user + '",')
			else:
				salida.write(linea[i] + ',')
		salida.write('"' + resumenLimpio + '",')
		salida.write('"' + textoLimpio + '"\r\n')
	entrada.close()
	salida.close()

def clean_text():
	limpiarTrain('train.csv', 'train_clean.csv')
	limpiarTest('test.csv', 'test_clean.csv')