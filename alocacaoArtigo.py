import numpy as np
import reader as read
import genetic as gn
import matplotlib.pyplot as plt
import numpy as np

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
        self.best_generations = []
        self.best_gen = 100

        # get matriz from reader.py > inputpath
        reader = read.reader()
        self.matriz_p = reader.createMatrix(inputpath) 
        self.run(crossoverrate, mutationrate, maxgen)
        

    def plot_generation(self, repeat, generations, means, best_individual):
        plt.plot(generations, means, linewidth=0.4, color='#777777')
        plt.plot(generations, best_individual, linewidth=0.4, color='lightgreen')
        plt.ylabel('mean')
        plt.xlabel('generation')

        plt.title('Observação fitness médio e fitness melhor individuo x generation')
        
        plt.title('analise na repetição: ' + str(repeat + 1))
        plt.savefig('geneticFiles/repeat-' + str(repeat + 1) + '.png')
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
        #plt.savefig('geneticFiles/out_' + str(rand.random_int(0, 300)) + '.png')
        plt.savefig('geneticFiles/fitness.png')
        #plt.show()
        plt.close()


    def run(self, crossoverrate, mutationrate, maxgen):
        for i in range(self.repeat):
            genetic = gn.Genetic(self.matriz_p)
            genetic.recursive_genetic(self.generation)

            self.best_generations.append(genetic.best_generation['index'])
            print ('best generation: ', genetic.best_generation['index'], ' - ', genetic.best_generation)

            if genetic.best_generation['index'] < self.best_gen:
                self.best_gen = genetic.best_generation['index']

            self.plot_generation(i, genetic.generations, genetic.mean, genetic.best_individual)
            print('\n----------------------------------------\n\t\tvez: ', i + 1, '\n----------------------------------------\n\n')

        mean_all_gen = np.mean(self.best_generations)

        self.plot_repeat(mean_all_gen)


aloca = alocacaoArtigo()