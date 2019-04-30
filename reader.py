import re as regex

class reader:
	def createMatrix():
		
		arq = open('inputpath', 'r')
		texto = arq.read()
		textoarray = texto.split("\n")
		matriz = []
		
		for texto in textoarray:
  			lista = regex.findall('(\d+)', texto)
  			for i in range(len(lista)):
  				lista[i] = int(lista[i])
  			matriz.append(lista)
		print(matriz)
		arq.close()
		return matriz
	matriz2 = createMatrix()

	print (matriz2)