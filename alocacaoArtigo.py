import numpy as np
import reader as read
import genetic as gn
import matplotlib.pyplot as plt
import numpy as np
import time

# ------------------------------------------------------------------------------------------
#    Alunos:    William Felipe Tsubota      - 201
#               Wesley Souza Campagna       - 2014.1907.010-0
#               Alberto                     - 201
#               Gabriel                     - 201
# ------------------------------------------------------------------------------------------

class alocacaoArtigo:
 
    def __init__(self, crossoverrate=0.5, mutationrate=0.01, maxgen=100, inputpath='inputpath'):
        self.generation = 0
        self.repeat = 10
        self.best_individual_by_generation_in_ten_repeat = []
        self.mean_individuals_generation_in_ten_repeat = []
        self.best_gen = maxgen
        self.best_generations = [] 

        # get matriz from reader.py > inputpath
        reader = read.reader()
        self.matriz_p = reader.createMatrix(inputpath)
        
        inicio = time.time()
        self.run(crossoverrate, mutationrate, maxgen)
        fim = time.time()
        print((fim - inicio), 'segundos')
        

    def run(self, crossoverrate, mutationrate, maxgen):
        for i in range(self.repeat):
            genetic = gn.Genetic(self.matriz_p, crossoverrate, mutationrate, maxgen)
            genetic.recursive_genetic(self.generation)

            self.best_generations.append(genetic.best_generation['index'])
           
            if genetic.best_generation['index'] < self.best_gen:
                self.best_gen = genetic.best_generation['index']

            self.best_individual_by_generation_in_ten_repeat.append(genetic.best_individual)
            self.mean_individuals_generation_in_ten_repeat.append(genetic.mean)

            self.plot_generation(i, genetic.mean, genetic.best_individual)

            print('\n----------------------------------------\n\t\trepeat: ', i + 1, '\n----------------------------------------\n\n')

        # best_ind... ten_repeat = [
        # [ 4, 3, 2]        <- repetição 1 melhor individuo (fitness) em cada geração x repetição [posição: geração: 1, 2, 3 ..]
        # [ 5, 2, 1]        <- repetição 2 melhor individuo (fitness) em cada geração x repetição [posição: geração: 1, 2, 3 ..]
        # ....
        # [n1, n2, n3]
        # ]

        mean_all_repeat = self.uniform(self.mean_individuals_generation_in_ten_repeat, maxgen)
        best_all_repeat = self.uniform(self.best_individual_by_generation_in_ten_repeat, maxgen)

        self.plot_generation(i, mean_all_repeat, best_all_repeat, ox=False)

        mean_all_gen = np.mean(self.best_generations)
        self.plot_repeat(mean_all_gen)


    def uniform(self, matriz, maxgen):
        # [[ 00, 01, 02]        
        # [ 10, 11, 12]        
        # ....
        # [n1, n2, n3]
        # ]  
        # a idéia é selecionar [x][n de interesse]

        mean = []

        for i in range(maxgen):
            all_el = 0
            count = 0
            for j in range(len(matriz)):
                if i < len(matriz[j]):
                    
                    all_el += matriz[j][i]
                    count += 1

            if count > 0:
                med = (all_el / count)
                #print('c: ', count, ' all_el: ', all_el, ' i: ', i, ' med: ', med)
                mean.append(med)
       
        return mean


    def plot_generation(self, repeat, means, best_individual, ox=True):
        gens = np.linspace(0, len(means), len(means))
        plt.plot(gens, means, linewidth=0.4, color='#777777')
        plt.plot(gens, best_individual, linewidth=0.4, color='lightgreen')
        plt.ylabel('mean')
        plt.xlabel('generation')

        plt.title('Observação fitness médio e fitness melhor individuo x generation')        
        plt.title('fitness médio de todas as repetições e  maior fitness médio de todas as repetições x gerações')
        
        if ox: plt.savefig('geneticFiles/repeat-' + str(repeat + 1) + '.png')
        else: plt.savefig('geneticFiles/fitness.png')
        #plt.show()
        plt.close()
        pass


    def plot_repeat(self, mean_all_gen):
        y_best_gen = [self.best_gen] * self.repeat
        y_mean_gen = [mean_all_gen] * self.repeat

        plt.plot(np.linspace(0, self.repeat, self.repeat), self.best_generations, marker='o', 
            linestyle='none', markersize=2.5, color='#777777', label='melhor valor por repetição')

        plt.plot(np.linspace(0, self.repeat, self.repeat), y_best_gen, linewidth=0.5, color='red',
            label='melhor geração em todas repetições')

        plt.plot(np.linspace(0, self.repeat, self.repeat), y_mean_gen, 
            linewidth=0.5, color='blue', label='media de todas repetições')

        plt.title('Observação melhor geração x repetição')
        plt.ylabel('generation')
        plt.xlabel('repeat')
        plt.legend()
        plt.savefig('geneticFiles/graph.png')
        #plt.show()
        plt.close()




aloca = alocacaoArtigo(crossoverrate=0.7, mutationrate=0.03, maxgen=100)