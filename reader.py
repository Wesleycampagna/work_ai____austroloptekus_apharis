import re as regex

class reader:

	def createMatrix(self, file_path):
		
		arq = open(file_path, 'r')
		texto = arq.read()
		textoarray = texto.split("\n")
		matriz = []
		
		for texto in textoarray:

  			lista = regex.findall('(\d+)', texto)
  			for i in range(len(lista)):
				  lista[i] = int(lista[i])
  			if len(lista) > 0:
				  matriz.append(lista)

		arq.close()
		return matriz
""" 

	matriz2 = createMatrix()

	for element in matriz2:
		print (element) """