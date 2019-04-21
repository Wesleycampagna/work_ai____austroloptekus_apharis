class generate:
    
    def operationMatriz(linhaRevisor, colunaArtigo, matriz):
        soma = 0
        for i in range(0, linhaRevisor):
            maior = matriz[i][0] #primeira posicao da linha
            menorDosMaiores = maior
            for j in range(1, colunaArtigo):
                print(matriz[i][j])
                if maior < matriz[i][j]:
                    maior = matriz[i][j]
            if menorDosMaiores > maior:
                menorDosMaiores = maior
            soma = soma + maior
        soma = soma - (5 - menorDosMaiores)
        print ('a soma eh:' , soma, '\n')
        return soma

    def retornaListaQtdArtRevisor(linha, matriz):
        listaQtdArtRevisor = matriz[linha]
        return listaQtdArtRevisor

    Matriz = [ [1, 2, 3], [3, 4 , 1], [2, 3, 1] ]
    operationMatriz(3, 3, Matriz)

