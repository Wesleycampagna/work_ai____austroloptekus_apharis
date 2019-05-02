import generate as gen
import randomize as rand
import matplotlib.pyplot as plt
import numpy as np

class alocacaoArtigo:

    crossoverrate = 0.6
    mutationrate = 0.05
    maxgen = 10                   
    population = 6
    ceil_floor = 1             # garante que o corte seja realizado da posição 1 a len-1

    def __init__(self, matriz):

        self.__isEnd = False
        self.generate = gen.generate()
        self.__objective = self.generate.generate_objective(matriz)


        print ('obj: ', self.__objective)
        
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

        self.best_generation = {
            'index': 0,
            'value': 0
        }

        print('disp: ', self.__obj['disp'])
        pass


    def print_matriz(self, matriz_):
        for i in matriz_:
            print(i)


    def recursive_genetic(self, generation):
        
        # print da geração atual
        print('\n+ ======================================+')
        print('+\t\tgeneration: ', generation)
        print('+ ======================================+\n')

        self.generations.append(generation)
       
        # print __objetivo baseado no que se obteve
        print ('obj: ', self.__objective)

        # print population
        self.print_matriz(self.population)

        # calular fitness de cada individuo 
        print('\n\t\t ## FITNESS ##\n')
        fitness = self.calculate_fitness(self.population)
        print('fitness: ', fitness)

        print('\n\t\t ## MÉDIA FITNESS ##\n')
        mean = self.get_mean(fitness, generation)
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
            return self.recursive_genetic(generation)
        
        if generation < alocacaoArtigo.maxgen:
            print ('\n\t enter')
            self.best_generation['index'] = generation
            self.best_generation['value'] = mean

        value = ("\n\t\t## FIM POR OBJETIVO", "\n\t\t## FIM POR MAXGEN")[generation >= alocacaoArtigo.maxgen]
        
        print(value)


    def calculate_fitness(self, population):  # penalisar falta

        fitness = []
        
        for line in population:
            quant_right_bits = 0
            for iterator in range(len(line)):
                if line[iterator] == self.__objective[iterator]:
                    quant_right_bits += 1
            
            self.evaluate_fitness(quant_right_bits)

            # não ter o risco de um fitness onde todos os bits estejam errado
            if quant_right_bits == 0:
                quant_right_bits = 1
            
            fitness.append(quant_right_bits)
            
        return fitness


    def evaluate_fitness(self, quant_right_bits):
        if self.__obj['collumn'] == quant_right_bits:
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

            coefficient = rand.random_porcentual()

            if (coefficient > alocacaoArtigo.crossoverrate):

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
           
        return genetic_process


    def mutation(self, matriz):

        for line in range(len(matriz)):
            for collumn in range(len(matriz[line])): 
                if rand.random_porcentual() <= alocacaoArtigo.mutationrate:
                    print('MUTATION: [ ' + str(line) + ' ][ ' + str(collumn) + ' ]')
                    if matriz[line][collumn] == 0: matriz[line][collumn] = 1
                    elif matriz[line][collumn] == 1: matriz[line][collumn] = 0

        return matriz


    def get_mean(self, array, gen):
        values = 0

        for element in array:
            values += element

        mean = values/len(array)

        if mean > self.best_generation['value']:
            self.best_generation['index'] = gen
            self.best_generation['value'] = mean

        return mean

# ------------------------------------------------------------------------------------------
#                                      inicia aqui por hora
# ------------------------------------------------------------------------------------------
generation = 0
repeat = 10
best_generations = []
best_gen = 0

# obs: matriz_p deve ser lida de um arquivo, suposta aqui
matriz_p =  [[0, 0, 3, 4, 4, 1],
            [3, 3, 0, 0, 1, 2],
            [4, 0, 0, 1, 0, 1],
            [2, 2, 2, 3, 2, 2]]

for i in range(repeat):
    aloca = alocacaoArtigo(matriz_p)
    aloca.recursive_genetic(generation)

    best_generations.append(aloca.best_generation['index'])
    print ('best generation: ', aloca.best_generation['index'], ' - ', aloca.best_generation)

    if aloca.best_generation['index'] > best_gen:
        best_gen = aloca.best_generation['index']
    print('\n----------------------------------------\n\t\tvez: ', i + 1, '\n----------------------------------------\n\n')

mean_all_gen = np.mean(best_generations)

print ('mean: ', mean_all_gen)
y_best_gen = [best_gen] * repeat
y_mean_gen = [mean_all_gen] * repeat

plt.plot(np.linspace(0, repeat, repeat), best_generations, marker='o', 
    linestyle='none', markersize=2.5, color='#777777', label='melhor valor por repetição')

plt.plot(np.linspace(0, repeat, repeat), y_best_gen, linewidth=0.5, color='red',
    label='maior geração')

plt.plot(np.linspace(0, repeat, repeat), y_mean_gen, 
    linewidth=0.5, color='blue', label='media de todas repetições')

plt.title('Observação melhor geração x repetição')
plt.ylabel('generation')
plt.xlabel('repeat')
plt.legend()
plt.savefig('geneticFiles/out_' + str(rand.random_int(0, 300)) + '.png')
# plt.savefig('geneticFiles/out_.png')
plt.show()
plt.close()
