import numpy as np
import reader as read
import genetic as gn
import matplotlib.pyplot as plt
import numpy as np
import time
import writer as write

# ------------------------------------------------------------------------------------------
#    Alunos:    William Felipe Tsubota      - 2017.1904.056-7
#               Wesley Souza Campagna       - 2014.1907.010-0
#               Alberto Benites             - 2016.1906.026-4
#               Gabriel Chiba Miyahira      - 2017.1904.005-2
# ------------------------------------------------------------------------------------------

class alocacaoArtigo:
 
    def __init__(self, crossoverrate=0.5, mutationrate=0.01, maxgen=100, inputpath='inputpath'):
        self.outputpath = 'saida-genetico.txt'
        self.generation = 0
        self.repeat = 10
        self.best_individual_by_generation_in_ten_repeat = []
        self.mean_individuals_generation_in_ten_repeat = []
        self.best_gen = maxgen
        self.best_generations = [] 
        self.best_all_individual = []

        # get matriz from reader.py > inputpath
        reader = read.reader()
        self.matriz_p = reader.createMatrix(inputpath)
        
        # calculo do tempo para o método que desencadeia o algoritmo e seus resultados
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

            print('best individual: ', genetic.best_individual)

            self.best_individual_by_generation_in_ten_repeat.append(genetic.best_individual_by_generation)
            self.mean_individuals_generation_in_ten_repeat.append(genetic.mean)

            self.plot_generation(i, genetic.mean, genetic.best_individual_by_generation)

            if len(self.best_all_individual) == 0:
                self.best_all_individual = genetic.best_individual

            elif len(genetic.best_individual) != 0:
                if self.best_all_individual[-1] < genetic.best_individual[-1]:
                    self.best_all_individual = genetic.best_individual
                
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

        # writer here. subi uma casa e tira a ultima

        writer = write.writer()
        del self.best_all_individual[-1]
        self.best_all_individual = map(lambda x:x+1, self.best_all_individual)
        writer.writeArchive(self.best_all_individual, self.outputpath)


    def uniform(self, matriz, maxgen):
        # [[ n0[k0=3,2],  n0[k1=3,4],  n0[k2=2,7]]        
        #  [ n1[k0=2,5],  n1[k1=5.0],  n1[k2=2,5]]        
        #             ....
        #  [ nn[k0=3.0],  nn[k1=4.0],  nn[k2=1.6]] ]  

        # a idéia é selecionar um n fixo e fazer média dos k. ex = ((3.2 + 2.5 + 3.0) / 3) => 2.9

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

aloca = alocacaoArtigo(crossoverrate=0.7, mutationrate=0.02, maxgen=100)
#aloca = alocacaoArtigo(crossoverrate=0.3, mutationrate=0.08, maxgen=300)
#aloca = alocacaoArtigo(crossoverrate=0.2, mutationrate=0.05, maxgen=50)