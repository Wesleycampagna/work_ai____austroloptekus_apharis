import generate as gen
import randomize as rand
import math

# ------------------------------------------------------------------------------------------
#    Alunos:    William Felipe Tsubota      - 2017.1904.056-7
#               Wesley Souza Campagna       - 2014.1907.010-0
#               Alberto Benites             - 2016.1906.026-4
#               Gabriel Chiba Miyahira      - 2017.1904.005-2
# ------------------------------------------------------------------------------------------

class Genetic:
                
    population = 6            
    ceil_floor = 1             # garante que o corte seja realizado da posição 1 a len-1
    amount_gen_to_verify = 10


    def __init__(self, matriz, crossoverrate, mutationrate, maxgen):

        # variaveis para controle interno
        self.__isEnd = False
        self.__generate = gen.generate()         
        self.__melhor_atual = 0             # usado para verificar convergencia
        self.__melhor_anterior = 0          # usado para verificar convergencia
        self.__individuo_atual = []         # usado para verificar convergencia
        self.__individuo_anterior = []      # usado para verificar convergencia
        self.__soma_gen = 0                 # se totalizar 10 geracoes, entao verifica se ha convergencia
        self.__best_fitness = 0
        
        # função heuristica e valores para para função de avaliação
        self.__heuristic_sum = self.__generate.generate_heuristic(matriz)    
        # self.__heuristic_bit = self.__generate.maximos_determinado_por_busca_gulosa(matriz)   
        self.__converg = (self._Genetic__heuristic_sum * 0.20)
        self.__penalty = self._Genetic__heuristic_sum / 5.1

        # parametros do algoritmo genético        
        self.__crossoverrate = crossoverrate
        self.__mutationrate = mutationrate
        self.__maxgen = maxgen
        self.__mat = matriz
        
        self.__obj = {
            # quantidade de individuos na população
            'number_of_individuals': Genetic.population,
            # quantidade de revisores
            'lines': len(matriz) - 1,
            # como se está usando conversão binaria e do contrario, tetolog é responsavel pelas casas binarias
            'tetolog': self.__generate.define_log_element(len(matriz) - 1),
            # -1 para tirar a disposição de correção, x tetoLog (representação binária)
            'elements': (len(matriz[0]) -1) * 
                self.__generate.define_log_element(len(matriz) - 1), 
            # @disp: array das disponibilidades
            'disp': self.__generate.generate_disp(matriz),
            # collumn do array de entrada - a disponibilidade
            'collumn': (len(matriz[0]) -1)
        }

        # gera aleatoriamente individuos para a populacao
        self.__population = self.__generate.generate_population(self.__obj)

        # vetores e variaveis transportadas para alocação para geração de graficos e afins
        self.mean = []
        self.generations = []
        self.best_individual_by_generation = []       # pelo fitness assim: [8.3, 8.7, 11, ... 16.0]
        self.best_individual = []                     # deve salvar algo assim: [3, 2, 1, 4, 4]
        
        self.best_generation = {
            'index': 0,
            'value': 0
        }
        pass


    def print_matriz(self, matriz_):
        for i in matriz_:
            print(i)


    def recursive_genetic(self, generation):
        
        # print da geração atual
        #print('\n+ ======================================+')
        #print('+\t\tgeneration: ', generation)
        #print('+ ======================================+\n')

        self.generations.append(generation)
       
        # print __heuristica baseado no que se obteve
        #print('obj: ', self._Genetic__heuristic_sum)

        # print population
        #self.print_matriz(self.__generate.to_int_matriz(self.__population, self.__obj['tetolog']))
        #self.print_matriz(self.__population)

        # calular fitness de cada individuo 
        #print('\n\t\t ## FITNESS ##\n')
        fitness = self.calculate_fitness(self.__population)
        #print('fitness: ', fitness)

        #obter média dos individuos dessa geração
        #print('\n\t\t ## MÉDIA FITNESS ##\n')
        mean = self.get_mean(fitness, generation)
        #print('média fitness: ', mean)

        self.mean.append(mean)
        
        self.__soma_gen += 1   # usado para verificar convergencia

        # se algum individuo alcancar o fitness ideal, cancelar recursao
        if not self.__isEnd and generation < self.__maxgen:            

            # determinar roleta atraves do fitness individual
            #print('\n\t\t ## ROULETE ##\n')
            roulette = self.get_roulette(fitness)
            #print('roulette: ', roulette)

            #seleciona valores randomicos para 'seleção' na roleta 
            #print('\n\t ## ROULETE RAFFLE PORCENT ##\n')
            raffle_roulette = self.randomic_porcentual_roulette()
            #print('raffle_roulette: ', raffle_roulette)

            # sortear individuos para a nova populacao && lhe atribuir esses novos individuos sorteados 
            #print('\n\t\t ## SELECT ##\n')
            self.__population = self.selected_to_crossover_and_set(raffle_roulette, roulette, self.__population)
            #self.print_matriz(self.__population)
            
            # realizar crossover
            #print('\n\t\t ## CROSSOVER ##\n')
            self.crossover()
            #self.print_matriz(self.__population)

            # realizar mutation
            self.__population = self.mutation(self.__population) 
            #print('\n\t\t ## MUTATION ##\n')
            #self.print_matriz(self.__population)

            # incrementar generation && rechamar o método
            generation += 1
            return self.recursive_genetic(generation)
        
        # ** caso alguma condição seja atingida salvar melhor generation (atual) **
        if generation < self.__maxgen:
            #print('\n\t enter')
            self.best_generation['index'] = generation
            self.best_generation['value'] = mean

        value = ("\n\t\t## FIM POR OBJETIVO", "\n\t\t## FIM POR MAXGEN")[generation >= self.__maxgen]
        
        print(generation, 'geracoes')
        #print(value)


    def calculate_fitness(self, population):  

        tetolog = self.__obj['tetolog']
        new_population = self.__generate.to_int_matriz(population, tetolog)
        fitness = []
        best_individual_by_generation = 0
        array_best_individual_by_generation = []

        for individual in new_population:
            sum_individual = 0
            i = 0
            for revisor in individual:
                sum_individual += self.__mat[revisor][i]
                i += 1


            # avalia em relação a disponibilidade e valores, podendo dar penalidades
            sum_individual = self.evaluate_fitness(individual, sum_individual)      # penalidades para disponibilidades incoerentes



            # não ter o risco de um fitness zerado ou negativo, causa problemas
            if sum_individual <= 0:
                sum_individual = 1

            # append fitness do individuo a lista de fitness já com penalidade
            fitness.append(sum_individual)

            if sum_individual > best_individual_by_generation:
                best_individual_by_generation = sum_individual
                array_best_individual_by_generation = individual

                if self.__best_fitness < sum_individual:
                    self.__best_fitness = sum_individual
                    # se o numero sum_individual vier quebrado não adicionar em best_individual (-1 disp)
                    if sum_individual == math.ceil(sum_individual):
                        self.best_individual = individual
                        self.best_individual.append(sum_individual)

            # avalia se o algoritmo parará a execução dada a atual geração
            self.evaluate_stop(sum_individual)                      # analise de convergencia

            
        self.best_individual_by_generation.append(best_individual_by_generation)
        if(best_individual_by_generation > self.__melhor_atual):
            self.__melhor_atual = best_individual_by_generation
            self.__individuo_atual = array_best_individual_by_generation
            #self.__individuo_atual.append(self.__melhor_atual)        # duvida >> pq se deixar essa linha 

        return fitness


    def evaluate_stop(self, sum_individual): # condição de parada do if la encima
        if self.__heuristic_sum == sum_individual:
            self.__isEnd = True

        elif self.__soma_gen == Genetic.amount_gen_to_verify:
            
            # a media da geracao atual pode ser menor q a media da geracao anterior? sim. Aplicar heuristica
            if (abs(self.__melhor_atual - self.__melhor_anterior) < self.__converg 
                and self.__melhor_atual > (self.__heuristic_sum - self.__converg) 
                    and self.__melhor_anterior != 0): 
                #if self.__melhor_atual > self.__melhor_anterior:
                    #self.best_individual = self.__melhor_atual
                #else:
                    #self.best_individual = self.__melhor_anterior
                self.__isEnd = True

            self.__melhor_anterior = self.__melhor_atual
            self.__melhor_atual = 0
            self.__individuo_anterior = self.__individuo_atual
            self.__individuo_atual = []
            self.__soma_gen = 0
        
    def evaluate_fitness(self, individual, sum_individual):

        disponibilidade = []
        for item in self.__obj['disp']: disponibilidade.append(item[1])
        punicao = self.__penalty # definir punicao

        
        for i in range(len(individual)):
            disponibilidade[individual[i]] = disponibilidade[individual[i]] - 1
            
            # a punição ocorre por meio de disponibilidade excedida e 1/5 da heuristica 
            # sofrendo ainda mais quando o valor obstrui em grau maior
            if disponibilidade[individual[i]] == -1:
                sum_individual = sum_individual - punicao
            elif disponibilidade[individual[i]] == -2:
                sum_individual = sum_individual - (punicao * 2)
            elif disponibilidade[individual[i]] <= -3:
                sum_individual = sum_individual - (punicao * 4)
            

        return sum_individual


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

        #print('\npositions: ', positions, '\n')
        
        return select


    # se cp for jogado para dentro do for a quebra das casas acontece diferente para cada par selecionado
    def crossover(self):

        # um array de n posições o corte acontece apenas a partir de 'ceil_floor' e 'ceil_floor -
        # final do vetor', se ceil_floor = 2 um vetor de 6 posição pode ser cortado 
        # apenas nas posições 2, 3 e 4. Multiplica-se tetolog para não corromper o numero do revisor 
        # que está em binario - puramente para otimização.
        cp = (rand.random_int(Genetic.ceil_floor, self.__obj['collumn'] - Genetic.ceil_floor) 
            * self.__obj['tetolog'])

        for line in range(0, len(self.__population), 2):

            coefficient = rand.random_porcentual()

            if (coefficient > self.__crossoverrate):

                first_array = self.__population[line]
                second_array = self.__population[line+1]

                self.__population[line] = self.cross(first_array, second_array, cp)
                self.__population[line+1] = self.cross(second_array, first_array, cp)
        pass


    def cross(self, first_piece, second_piece, cp):
        genetic_process = []
        for i in range(self.__obj['elements']):
            if i < cp: genetic_process.append(first_piece[i])
            else: genetic_process.append(second_piece[i])
           
        return genetic_process


    def mutation(self, matriz):
        tetolog = self.__obj['tetolog']
        for line in range(len(matriz)):
            for collumn in range(0, len(matriz[line]), tetolog): 
                if rand.random_porcentual() <= self.__mutationrate:
                    #print('MUTATION: [ ' + str(line) + ' ][ ' + str(collumn) + ' ]')
                    lista = self.__generate.create_element(self.__obj)
                    self.__generate.replace(lista,matriz[line], collumn, collumn + tetolog)

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