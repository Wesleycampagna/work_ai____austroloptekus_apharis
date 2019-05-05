class writer:
	def convertToVetorDec(vetorBin, tetoLog):
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
	def writeArchive(listaInt):
		
		arq = open('saida-genetico.txt', 'w')
		listaStr = list(map(str, listaInt))
		separator = ' '
		result = [separator.join(listaStr)]
		result = [r.replace(' ', ',') for r in result]
		arq.writelines(result)
		arq.close()
	
	texto = []
	texto.append(1)
	texto.append(2)
	texto.append(3)
	writeArchive(texto)
	print(convertToVetorDec([1,1,0,1,0,0], 3))