import generate as gen
import randomize as rand
import matplotlib.pyplot as plt


class alocacaoArtigo:

    crossoverrate = 0.6
    mutationrate = 0.05
    maxgen = 100                # a pilha pode até 900 meu pc [0, 0, 0, 0, 0, 0]
                                                            # [1, 0, 0, 0, 0, 0]        
    population = 8
    ceil_floor = 1              # garante que o corte seja realizado da posição 1 a len-1

    def __init__(self, matriz):

        self.__isEnd = False
        self.generate = gen.generate()
        self.__objective = self.generate.genStaticHeuristic()
        
        self.__obj = {
            'number_of_individuals': alocacaoArtigo.population,
            'lines': len(matriz),
            # -1 para tirar a disposição de correção
            'collumn': (len(matriz[0]) -1) * 2,   # vai ter que mexer no 2 (tem que ser dinamico na quantidade de revisores)
            # @disp: array das disponibilidades
            'disp': self.generate.generate_disp(matriz)
        }

        # gera aleatoriamente individuos para a populacao
        self.population = self.generate.generate_population(self.__obj)
        self.mean = []
        self.generations = []

        print('disp: ', self.__obj['disp'])
        pass

    def print_matriz(self, matriz_):
        for i in matriz_:
            print(i)


    def recursiveGenetic(self, generation):
        
        # print da geração atual
        print('\n+ ======================================+')
        print('+\t\tgeneration: ', generation)
        print('+ ======================================+\n')

        self.generations.append(generation)
       
        # print __objetivo baseado no que se obteve
        print (self.__objective)

        # print population
        self.print_matriz(self.population)

        # calular fitness de cada individuo 
        print('\n\t\t ## FITNESS ##\n')
        fitness = self.calculate_fitness(self.population)
        print('fitness: ', fitness)

        print('\n\t\t ## MÉDIA FITNESS ##\n')
        mean = self.get_meania(fitness)
        print('média fitness: ', mean)
        self.mean.append(mean)

        # se algum individuo alcancar o fitness ideal, cancelar recursao
        if not self.__isEnd and generation < alocacaoArtigo.maxgen:

            # determinar roleta atraves do fitness individual
            print('\n\t\t ## ROULETE ##\n')
            roulette = self.get_roulette(fitness)
            print('roulette: ', roulette)

            #determina valores randomicos da roleta 
            print('\n\t ## ROULETE RAFFLE PORCENT ##\n')
            raffle_roulette = self.randomic_porcentual_roulette()
            print('raffle_roulette: ', raffle_roulette)

            # sortear individuos para a nova populacao && atribuir esses novos individuos sorteados a populacao 
            print('\n\t\t ## SELECT ##\n')
            self.population = self.selected_to_crossover_and_set(raffle_roulette, roulette, self.population)
            self.print_matriz(self.population)
            
            # realizar crossover
            print('\n\t\t ## CROSSOVER ##\n')
            self.crossover()
            self.print_matriz(self.population)


            # realizar mutation
            self.population = self.mutation(self.population) 
            print('\n\t\t ## MUTATION ##\n')
            self.print_matriz(self.population)

            generation += 1
            return self.recursiveGenetic(generation)
        
        value = ("\n\t\t## FIM POR OBJETIVO", "\n\t\t## FIM POR MAXGEN")[generation >= alocacaoArtigo.maxgen]
        print(value)

    def calculate_fitness(self, population):  # penalisar falta

        fitness = []
        
        for line in population:
            equal = 0
            for iterator in range(len(line)):
                if line[iterator] == self.__objective[iterator]:
                    equal += 1
            
            self.evaluate_fitness(equal)

            # não ter o risco de um fitness onde todos os bits estejam errado
            if equal == 0:
                equal = 1
            
            fitness.append(equal)
            
        return fitness

    def evaluate_fitness(self, equal):
        if self.__obj['collumn'] == equal:
            self.__isEnd = True

    def get_roulette(self, fitness_array):
        pieces_of_roulette = []
        total_fitness = 0
        porcentual = 0

        # somatorio dos fitness 
        for value in fitness_array:
            total_fitness += value

        # porcentua de um unico fitness em relação ao total numa roleta de 360 graus
        for value in fitness_array:
            porcentual += (value * 360) / total_fitness 
            pieces_of_roulette.append(round(porcentual, 4))
        
        return pieces_of_roulette

    
    def randomic_porcentual_roulette(self): 
        roulette = []

        for iterator in range(self.__obj['number_of_individuals']):
            roulette.append(rand.random_float(360))
        
        return roulette
            
    def selected_to_crossover_and_set(self, raffle, roulette, matriz):
        select = []
        positions = []

        for element in raffle:
            position = 0

            for value in roulette:
                # se o valor do 'element' sorteado for >= que um pedaço da roleta 
                # incremento até o valor achar qual posição da roleta se refere
                if value < element:
                    position += 1
                    
            positions.append(position)
            select.append(matriz[position])

        print('---->>>')
        print(positions)
        print('---->>>*')

        return select


    def crossover(self):

        for line in range(0, len(self.population), 2):

            coeficiente = rand.random_porcentual()

            if (coeficiente > alocacaoArtigo.crossoverrate):
                print('\t\tenter coeficiente')
                first_array = self.population[line]
                second_array = self.population[line+1]

                # um array de n posições o corte acontece apenas a partir de 'ceil_floor' e 'ceil_floor
                # antes do final do vetor, se ceil_floor = 2 um vetor de 6 posição pode ser cortado 
                # apenas nas posições 2, 3 e 4 
                cp = rand.random_int(alocacaoArtigo.ceil_floor, self.__obj['collumn'] - alocacaoArtigo.ceil_floor)

                self.population[line] = self.cross(first_array, second_array, cp)
                self.population[line+1] = self.cross(second_array, first_array, cp)
        pass

    def cross(self, first_piece, second_piece, cp):
        genetic_process = []
        for i in range(self.__obj['collumn']):
            if i < cp: genetic_process.append(first_piece[i])
            else: genetic_process.append(second_piece[i])
           
        #print (genetic_process)
        return genetic_process
        #pass
    
    def mutation(self, matriz):

        for line in range(len(matriz)):
            for collumn in range(len(matriz[line])): 
                if rand.random_porcentual() <= alocacaoArtigo.mutationrate:
                    print('MUTATION: [ ' + str(line) + ' ][ ' + str(collumn) + ' ]')
                    if matriz[line][collumn] == 0: matriz[line][collumn] = 1
                    elif matriz[line][collumn] == 1: matriz[line][collumn] = 0

        return matriz

    def get_meania(self, array):
        meania = 0

        for element in array:
            meania += element

        return meania/len(array)

""" inicia aqui por hora """
generation = 0

""" obs: matriz_p deve ser lida de um arquivo, suposta aqui """
matriz_p =  [[0, 0, 3, 4, 4, 1],
            [3, 3, 0, 0, 1, 2],
            [4, 0, 0, 1, 0, 1],
            [2, 2, 2, 3, 2, 2]]

for i in range(1):
    aloca = alocacaoArtigo(matriz_p)
    aloca.recursiveGenetic(generation)

    print('\n----------------------------------------\n\t\tvez: ', i + 1, '\n----------------------------------------\n\n')

# plt.subplot(1, 2, 1)
plt.plot(aloca.generations, aloca.mean)
plt.ylabel('meania')
plt.xlabel('geração')
plt.show()
