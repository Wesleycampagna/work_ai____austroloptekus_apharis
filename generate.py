import randomize as rand

class generate:

    def operationMatriz(matriz):
        linhaRevisor = len(matriz)
        colunaArtigo = len(matriz[0])
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


    ''' 
    ==============================================================================
    Por hora retorna uma solução ótima sem nada para chegar nisto - simulado - ini
    ==============================================================================
    '''
    def genStaticHeuristic(self):
        return [1, 0, 0, 1, 0, 0, 1, 1, 1, 1]  # compor a heuristica

    ''' 
    ==============================================================================
    Por hora retorna uma solução ótima sem nada para chegar nisto - simulado - fim
    ==============================================================================
    '''


    # append line inteira: [[element11, element21, element31, ..., elementN1], ...
    def generate_population(self, dimension_obj):
        matriz = [] 
        for iterator in range(dimension_obj['number_of_individuals']):
            matriz.append(self.create_lines(dimension_obj))
        return matriz


    # append elemento para uma linha unica:  [element1, element2, element3, ..., elementN]
    def create_lines(self, dimension_obj):
        lines = []

        for line in range(dimension_obj['collumn']):
            lines.append(self.create_element(dimension_obj))
        
        return lines


    # cria um elemento randomico
    def create_element(self, dimension_obj):
        return rand.random_bin()


    # retorna [posição revisor, disponibilidade]
    def generate_disp(self, matriz):
        disp = []
        for i in range(len(matriz)):
            disp.append([i, matriz[i][-1]])
        return disp


    """  Matriz = [ [1, 2, 3], [3, 4 , 1], [2, 3, 1] ]
        operationMatriz(Matriz) """


