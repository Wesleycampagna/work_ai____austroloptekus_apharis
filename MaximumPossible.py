# ------------------------------------------------------------------------------------------
#    Alunos:    William Felipe Tsubota      - 2017.1904.056-7
#               Wesley Souza Campagna       - 2014.1907.010-0
#               Alberto Benites             - 2016.1906.026-4
#               Gabriel Chiba Miyahira      - 2017.1904.005-2
# ------------------------------------------------------------------------------------------

class Maximum:
	def generateMax(self, matriz):
		linhasRevisor = len(matriz)
		colunasArtigo = len(matriz[0])
		
		listaArtigosParaCorrigir = []
		listaResultado = [None] * (colunasArtigo - 1) # Lista que portara o resultado
		DicQtdArtigosParaCadaRevisor = {}
		
		for i in range(0, colunasArtigo - 1): # Menos um pq a ultima posicao eh o numero de quantos artigos os corretores corrigem
			listaArtigosParaCorrigir.append(i)

		for i in range(0, linhasRevisor): # O dicionario a ser criado esta na estrutura REVISOR : QTD ARTIGOS QUE O REVISOR CORRIGE
			if(matriz[i][colunasArtigo - 1] > 0): # Se o revisor corrige mais do que 0 entao eu coloco na lista
				DicQtdArtigosParaCadaRevisor.update({i : matriz[i][colunasArtigo - 1]})

		while(listaArtigosParaCorrigir != [] and DicQtdArtigosParaCadaRevisor != {}): # Enquanto a lista nao for vazia
			artigoASerCorrigido = listaArtigosParaCorrigir[0]

			posRevisorMaiorAfinidade = -1
			MaiorAfinidade = -1

			for i in DicQtdArtigosParaCadaRevisor: 
				if(matriz[i][artigoASerCorrigido] > MaiorAfinidade):
					posRevisorMaiorAfinidade = i
					MaiorAfinidade = matriz[i][artigoASerCorrigido]

			RevisorACorrigir = posRevisorMaiorAfinidade # Reutilizarei a variavel posRev mais tarde

			if(len(DicQtdArtigosParaCadaRevisor) == 1): # Se eu tenho um unico corretor disponivel
				listaResultado[artigoASerCorrigido] = RevisorACorrigir # entao entrego o artigo para o revisor
				DicQtdArtigosParaCadaRevisor[RevisorACorrigir] -= 1
				if(DicQtdArtigosParaCadaRevisor[RevisorACorrigir] == 0): # Se o revisor ja corrigiu tudo
					del(DicQtdArtigosParaCadaRevisor[RevisorACorrigir]) # entao remove da lista
				listaArtigosParaCorrigir.remove(artigoASerCorrigido)

			elif(DicQtdArtigosParaCadaRevisor[RevisorACorrigir] > 1): # Se a disponiblidade eh maior que 1, 
				listaResultado[artigoASerCorrigido] = RevisorACorrigir # entao entrego o artigo para o revisor
				DicQtdArtigosParaCadaRevisor[RevisorACorrigir] -= 1
				if(DicQtdArtigosParaCadaRevisor[RevisorACorrigir] == 0): # Se o revisor ja corrigiu tudo
					del(DicQtdArtigosParaCadaRevisor[RevisorACorrigir]) # entao remove da lista
				listaArtigosParaCorrigir.remove(artigoASerCorrigido)

			else:
				DicionarioMelhorRevisorPorArtigo = {} # Dicionario Artigo : Revisor
				Dicionario2MelhorRevisorPorArtigo = {} # Dicionario Artigo : Revisor


				
				for i in range(0, len(listaArtigosParaCorrigir)): # i travado na coluna, que representa UM artigo
					indiceArtigo = listaArtigosParaCorrigir[i]
					
					posRevisorMaiorAfinidade = list(DicQtdArtigosParaCadaRevisor.items())[0][0] # Pego a chave da primeira tupla
					MaiorAfinidade = matriz[posRevisorMaiorAfinidade][indiceArtigo]
					posRevisor2MaiorAfinidade = list(DicQtdArtigosParaCadaRevisor.items())[1][0] # "***REVISOR***" : QTD ARTIGOS
					SegundaMaiorAfinidade = matriz[posRevisor2MaiorAfinidade][indiceArtigo]

					if(MaiorAfinidade < SegundaMaiorAfinidade):
						troca = MaiorAfinidade
						MaiorAfinidade = SegundaMaiorAfinidade
						SegundaMaiorAfinidade = troca
						troca = posRevisorMaiorAfinidade
						posRevisorMaiorAfinidade = posRevisor2MaiorAfinidade
						posRevisor2MaiorAfinidade = troca
					
					for j in range(2, len(DicQtdArtigosParaCadaRevisor.keys())): # Qual revisor tem a maior afinidade para o artigo
						indiceRevisor = list(DicQtdArtigosParaCadaRevisor.items())[j][0]
						if(matriz[indiceRevisor][indiceArtigo] > MaiorAfinidade):
							SegundaMaiorAfinidade = MaiorAfinidade
							posRevisor2MaiorAfinidade = posRevisorMaiorAfinidade
							MaiorAfinidade = matriz[indiceRevisor][indiceArtigo]
							posRevisorMaiorAfinidade = indiceRevisor
						elif(matriz[indiceRevisor][indiceArtigo] > SegundaMaiorAfinidade):
							SegundaMaiorAfinidade = matriz[indiceRevisor][indiceArtigo]
							posRevisor2MaiorAfinidade = indiceRevisor
					DicionarioMelhorRevisorPorArtigo.update({indiceArtigo : posRevisorMaiorAfinidade})
					Dicionario2MelhorRevisorPorArtigo.update({indiceArtigo : posRevisor2MaiorAfinidade})
				
				ListaArtQRevEhMelhor = [] 
				for i in DicionarioMelhorRevisorPorArtigo:
					if(DicionarioMelhorRevisorPorArtigo[i] == RevisorACorrigir):
						ListaArtQRevEhMelhor.append(i)
				
				if(len(ListaArtQRevEhMelhor) == 1): # Se o artigo que o corretor eh bom no que ja vimos
					listaResultado[artigoASerCorrigido] = RevisorACorrigir # entao so damos o artigo a ele
					DicQtdArtigosParaCadaRevisor[RevisorACorrigir] -= 1
					if(DicQtdArtigosParaCadaRevisor[RevisorACorrigir] == 0): # Se o revisor ja corrigiu tudo
						del(DicQtdArtigosParaCadaRevisor[RevisorACorrigir]) # entao remove da lista
					listaArtigosParaCorrigir.remove(artigoASerCorrigido)

				elif(len(ListaArtQRevEhMelhor) > 1): # Se o revisor em questao eh melhor em outros artigos tambem
					PosMaiorDiferenca = -1; # Entao eu calculo a diferenca com o segundo melhor nos artigos
					MaiorDiferenca = -1; # E dou para o revisor o artigo com a maior diferenca
					
					for i in range(0, len(ListaArtQRevEhMelhor)):
						PosAnalisada = ListaArtQRevEhMelhor[i]
						MelhorValor = matriz[DicionarioMelhorRevisorPorArtigo[PosAnalisada]][PosAnalisada]
						SegundoMelhorValor = matriz[Dicionario2MelhorRevisorPorArtigo[PosAnalisada]][PosAnalisada]
						diferenca = MelhorValor - SegundoMelhorValor
						
						if(diferenca > MaiorDiferenca):
							MaiorDiferenca = diferenca
							PosMaiorDiferenca = PosAnalisada

					artigoASerCorrigido = PosAnalisada

					listaResultado[artigoASerCorrigido] = RevisorACorrigir
					DicQtdArtigosParaCadaRevisor[RevisorACorrigir] -= 1
					if(DicQtdArtigosParaCadaRevisor[RevisorACorrigir] == 0): # Se o revisor ja corrigiu tudo
						del(DicQtdArtigosParaCadaRevisor[RevisorACorrigir]) # entao remove da lista
					listaArtigosParaCorrigir.remove(artigoASerCorrigido)


		if(None not in listaResultado):
			#return (list(map(lambda x: x + 1, listaResultado)))
			return listaResultado
		else:
			print("HOUVE UM PROBLEMA COM A SAIDA")
			return([])