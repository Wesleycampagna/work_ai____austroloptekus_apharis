import re as regex

# ------------------------------------------------------------------------------------------
#    Alunos:    William Felipe Tsubota      - 2017.1904.056-7
#               Wesley Souza Campagna       - 2014.1907.010-0
#               Alberto Benites             - 2016.1906.026-4
#               Gabriel Chiba Miyahira      - 2017.1904.005-2
# ------------------------------------------------------------------------------------------

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