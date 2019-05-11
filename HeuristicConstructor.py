class Heuristic:
	def generateHeuristic(self, matriz):
		linhasRevisor = len(matriz)
		colunasArtigo = len(matriz[0])
		
		listaResultado = [] # Lista que portara o resultado
		
		for i in range(0, colunasArtigo - 1): # Menos um pq a ultima posicao eh o numero de quantos artigos os corretores corrigem
			maior = matriz[0][i]
			posMaior = 0
			for j in range(1, linhasRevisor):
				if(maior < matriz[j][i]):
					maior = matriz[j][i]
					posMaior = j
			listaResultado.append(matriz[posMaior][i])

		return listaResultado