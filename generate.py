import randomize as rand
import ObjectiveConstructor as obj_construct
import math 

class generate:

    def generate_objective(self, matriz):
        self.list_revisor_article = obj_construct.Objective().generateObjective(matriz)
        return self.to_binary(self.list_revisor_article)


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


    def define_log_element(self, great_element_value):
        return math.ceil(math.log(float(great_element_value), 2))


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

# obj = generate()

# obj.to_binary([2, 1, 3, 3, 0])