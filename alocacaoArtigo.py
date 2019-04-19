class alocacaoArtigo:

    crossoverrate = 0.6
    mutationrate = 0.2
    maxgen = 100

    def recursiveGenetic(self, matriz, numInteractions):
        generations = []
        #self.numInteractions = 0
        
        print(numInteractions)
        # primeiro achar o estado final 

        # gerar aleatoriamente individuos para a populacao

        # calular fitness de cada individuo 

        # se algum individuo alcancar o fitness ideal, cancelar recursao

        if numInteractions < alocacaoArtigo.maxgen:

            # determinar roleta atraves do fitness individual

            # sortear individuos para a nova populacao 

            # atribuir esses novos individuos sorteados a populacao 

            # realizar crossover

            # realizar mutation 

            numInteractions += 1
            return self.recursiveGenetic(matriz, numInteractions)
        
        pass


aloca = alocacaoArtigo()

aloca.recursiveGenetic(4, 0)