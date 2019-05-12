# ------------------------------------------------------------------------------------------
#    Alunos:    William Felipe Tsubota      - 2017.1904.056-7
#               Wesley Souza Campagna       - 2014.1907.010-0
#               Alberto Benites             - 2016.1906.026-4
#               Gabriel Chiba Miyahira      - 2017.1904.005-2
# ------------------------------------------------------------------------------------------

class writer:
	
	def convertToVetorDec(self, vetorBin, tetoLog):
		resultado = 0
		posicao = 0
		vetorDec = []
		while(posicao < len(vetorBin)):
			for i in range(0, tetoLog):
				resultado = (resultado * 10) + vetorBin[posicao]
				posicao += 1
			vetorDec.append(int(str(resultado), 2))
			resultado = 0
		print(vetorDec)
		return vetorDec


	def writeArchive(self, listaInt, file_path):
		
		arq = open(file_path, 'w')
		listaStr = list(map(str, listaInt))
		separator = ' '
		result = [separator.join(listaStr)]
		result = [r.replace(' ', ',') for r in result]
		arq.writelines(result)
		arq.close()
		pass
#	texto = []
#	texto.append(1)
#	texto.append(2)
#	texto.append(3)
#	writeArchive(texto)
#	print(convertToVetorDec([1,1,0,1,0,0], 3))