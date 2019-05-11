import generate as gen
import randomize as rand


class Genetic:
                
    population = 6             
    ceil_floor = 1             # garante que o corte seja realizado da posição 1 a len-1
    penalty = 3
    amount_gen_to_verify = 10


    def __init__(self, matriz, crossoverrate, mutationrate, maxgen):

        self.__isEnd = False
        self.generate = gen.generate()
        self.__heuristic_sum = self.generate.generate_heuristic(matriz)    
        self.__heuristic_bit = self.generate.generate_objective(matriz)    
        self.__soma_mean_atual = 0   # usado para verificar convergencia
        self.__soma_med_anterior = 0   # usado para verificar convergencia
        self.__soma_gen = 0   # se totalizar 10 geracoes, entao verifica se ha convergencia

        print('sum_h: ',self.__heuristic_sum)
        
        self.crossoverrate = crossoverrate
        self.mutationrate = mutationrate
        self.maxgen = maxgen
        self.mat = matriz

        print('obj: ', self.__heuristic_bit)
        
        self.__obj = {
            'number_of_individuals': Genetic.population,
            'lines': len(matriz),
            'tetolog': self.generate.define_log_element(self.generate.get_great_revisor()),
            # -1 para tirar a disposição de correção, x tetoLog (representação binária)
            'elements': (len(matriz[0]) -1) * 
                self.generate.define_log_element(self.generate.get_great_revisor()), 
            # @disp: array das disponibilidades
            'disp': self.generate.generate_disp(matriz),
            'collumn': (len(matriz[0]) -1)
        }

        # gera aleatoriamente individuos para a populacao
        self.population = self.generate.generate_population(self.__obj)

        self.mean = []
        self.generations = []
        self.best_individual = []

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
       
        # print __heuristica baseado no que se obteve
        print('obj: ', self._Genetic__heuristic_sum)

        # print population
        self.print_matriz(self.population)

        # calular fitness de cada individuo 
        print('\n\t\t ## FITNESS ##\n')
        fitness = self.calculate_fitness(self.population)
        print('fitness: ', fitness)

        #obter média dos individuos dessa geração
        print('\n\t\t ## MÉDIA FITNESS ##\n')
        mean = self.get_mean(fitness, generation)
        print('média fitness: ', mean)

        self.mean.append(mean)
        
        self.__soma_mean_atual += mean   # usado para verificar convergencia
        print(' to rodando aqui rapaz')
        self.__soma_gen += 1   # usado para verificar convergencia
        print(self.__soma_gen)

        # se algum individuo alcancar o fitness ideal, cancelar recursao
        if not self.__isEnd and generation < self.maxgen:            

            # determinar roleta atraves do fitness individual
            print('\n\t\t ## ROULETE ##\n')
            roulette = self.get_roulette(fitness)
            print('roulette: ', roulette)

            #seleciona valores randomicos para 'seleção' na roleta 
            print('\n\t ## ROULETE RAFFLE PORCENT ##\n')
            raffle_roulette = self.randomic_porcentual_roulette()
            print('raffle_roulette: ', raffle_roulette)

            # sortear individuos para a nova populacao && lhe atribuir esses novos individuos sorteados 
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

            # incrementar generation && rechamar o método
            generation += 1
            return self.recursive_genetic(generation)
        
        # ** caso alguma condição seja atingida salvar melhor generation (atual) **
        if generation < self.maxgen:
            print('\n\t enter')
            self.best_generation['index'] = generation
            self.best_generation['value'] = mean

        value = ("\n\t\t## FIM POR OBJETIVO", "\n\t\t## FIM POR MAXGEN")[generation >= self.maxgen]
        
        print(value)


    def calculate_fitness(self, population):  

        tetolog = self.__obj['tetolog']
        new_population = self.generate.to_int_matriz(population, tetolog)
        fitness = []
        best_individual = 0

        for individuals in new_population:
            sum_individual = 0
            i = 0
            for individual in individuals:
                sum_individual += self.mat[individual][i]
                i += 1

            # avalia se o algoritmo parará a execução dada a atual geração
            self.evaluate_stop(sum_individual)                      # analise de convergencia

            # avalia em relação a disponibilidade e valores, podendo dar penalidades
            self.evaluate_fitness(individuals, sum_individual)      # penalidades para disponibilidades incoerentes

            # não ter o risco de um fitness zerado ou negativo
            if sum_individual <= 0:
                sum_individual = 1

            # append fitness do individuo a lista de fitness já com penalidade
            fitness.append(sum_individual)

            if sum_individual > best_individual:
                best_individual = sum_individual
            
        self.best_individual.append(best_individual)

        return fitness


    def evaluate_stop(self, sum_individual): # condição de parada do if la encima
        if self.__heuristic_sum == sum_individual:
            self.__isEnd = True

        elif self.__soma_gen == Genetic.amount_gen_to_verify:
            mediaAtual = self.__soma_mean_atual / Genetic.amount_gen_to_verify
            mediaAnterior = self.__soma_med_anterior / Genetic.amount_gen_to_verify

            # a media da geracao atual pode ser menor q a media da geracao anterior? sim. Aplicar heuristica
            if abs(mediaAtual - mediaAnterior) < 2 and self.__soma_med_anterior != 0: 
                 self.__isEnd = True

            print(mediaAtual, mediaAnterior, ' toma aew')
            self.__soma_med_anterior = self.__soma_mean_atual
            self.__soma_mean_atual = 0
            self.__soma_gen = 0

        
    def evaluate_fitness(self, individuals, sum_individual):
        disponibilidade = []
        disponibilidade.extend(self.__obj['disp'])
        
        punicao = Genetic.penalty # definir punicao
        
        for i in range(len(individuals)):
            disponibilidade[individuals[i]][1] = disponibilidade[individuals[i]][1] - 1
            if(disponibilidade[individuals[i]][1] < 0):
                sum_individual = sum_individual - punicao
                break
        pass


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

        print('\npositions: ', positions, '\n')
        
        return select


    def crossover(self):

        # um array de n posições o corte acontece apenas a partir de 'ceil_floor' e 'ceil_floor
        # antes do final do vetor, se ceil_floor = 2 um vetor de 6 posição pode ser cortado 
        # apenas nas posições 2, 3 e 4. Multiplica-se tetolog para não corromper o numero do revisor.
        cp = (rand.random_int(Genetic.ceil_floor, self.__obj['collumn'] - Genetic.ceil_floor) 
            * self.__obj['tetolog'])

        for line in range(0, len(self.population), 2):

            coefficient = rand.random_porcentual()

            if (coefficient > self.crossoverrate):

                first_array = self.population[line]
                second_array = self.population[line+1]

                self.population[line] = self.cross(first_array, second_array, cp)
                self.population[line+1] = self.cross(second_array, first_array, cp)
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
                if rand.random_porcentual() <= self.mutationrate:
                    print('MUTATION: [ ' + str(line) + ' ][ ' + str(collumn) + ' ]')
                    lista = self.generate.create_element(self.__obj)
                    self.generate.replace(lista,matriz[line], collumn, collumn + tetolog)

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


# +======================================================================================================+
#                   antigos para bits
# +======================================================================================================+

    def calculate_fitness2(self, population):  # *** nao sera usado ***

        fitness = []
        best_individual = 0
        
        for line in population:
            quant_right_bits = 0
            for iterator in range(len(line)):
                if line[iterator] == self.__heuristic_bit[iterator]:
                    quant_right_bits += 1
            
            self.evaluate_fitness_(quant_right_bits)

            # não ter o risco de um fitness onde todos os bits estejam errado
            if quant_right_bits == 0:
                quant_right_bits = 1
            
            # verifica se ainda é o melhor individuo da população 
            if quant_right_bits > best_individual:
                best_individual = quant_right_bits

            fitness.append(quant_right_bits)
        
        self.best_individual.append(best_individual)
            
        return fitness   # *** modify final ***
    

    def evaluate_fitness_(self, quant_right_bits): 
        if self.__obj['elements'] == quant_right_bits:
            self.__isEnd = True