import randomize as rand
import HeuristicConstructor as heu_construct
import math 

# ------------------------------------------------------------------------------------------
#    Alunos:    William Felipe Tsubota      - 2017.1904.056-7
#               Wesley Souza Campagna       - 2014.1907.010-0
#               Alberto Benites             - 2016.1906.026-4
#               Gabriel Chiba Miyahira      - 2017.1904.005-2
# ------------------------------------------------------------------------------------------

class generate:

    def generate_heuristic(self, matriz):
        summ = 0
        self.list_revisor_article_ = heu_construct.Heuristic().generateHeuristic(matriz)
        for value in self.list_revisor_article_: summ += value
        return summ
       

    def get_great_revisor(self):
        return max(self.list_revisor_article)

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
            lines.extend(self.create_element(dimension_obj))
        
        return lines


    # cria um elemento randomico
    def create_element(self, dimension_obj):
        revisores = (dimension_obj['lines'])
        tetolog = self.define_log_element(revisores)
        lista = []

        string_binaria = self.__get_bin(rand.random_int(0, (revisores)), tetolog)
        for i in string_binaria:
            lista.append(int(i))
        return lista


    # retorna [posição revisor, disponibilidade]
    def generate_disp(self, matriz):
        disp = []
        for i in range(len(matriz)):
            disp.append([i, matriz[i][-1]])
        return disp


    def define_log_element(self, great_element_value):
        return math.ceil(math.log(float(great_element_value + 1), 2))


    # transfere para binario um array de entrada
    def to_binary(self, array):
        
        positions = self.define_log_element(max(array))
        binary_format_array = []
        
        for element in array:
            value = self.__get_bin(element, positions)
            
            for el in value:
                binary_format_array.append(int(el))                
        
        return binary_format_array
 

    def __get_bin(self, number, positions):
        set_str = '{0:0' + str(positions) + 'b}'
        return set_str.format(number)


    def replace(self, lista, linha, inicio, fim):
        for i in range(inicio, fim):
            linha[i] = lista[i - inicio]
        pass

    
    def to_int_matriz(self, matriz, tetolog):
        individuals = []

        for line in matriz:
            list = []            
            for i in range(0, len(line), tetolog):
                atual = ''  
                for j in range(i, i + tetolog):
                    atual += str(line[j])
                list.append(int(atual, 2))
            individuals.append(list)
        
        return individuals