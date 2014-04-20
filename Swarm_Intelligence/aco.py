# -*- coding: utf-8 -*-
import sys
import random

class AntColonyOptimization:
	
    def __init__(self, matrix_file):
        text_matrix = self.read_info_from_file(matrix_file) 
        self.heuristic_matrix = self.parse_matrix(text_matrix)
        self.total_nodes = len(self.heuristic_matrix)
        self.feromon_matrix = self.init_feromon_matrix()
        
        # Factor de decremento de la feromona p (letra griega rho)
        self.p = 0.3
        
    def get_heuristic_matrix(self):
        return self.heuristic_matrix

    def get_feromon_matrix(self):
        return self.feromon_matrix

    def read_info_from_file(self, file_name):
        return [line.rstrip('\r\n').split() for line in list(open(file_name))]

    def parse_matrix(self, raw_matrix):
        """ Método para convertir la info tomada de un archivo a enteros """
        matrix = []
        for line in raw_matrix:
            matrix.append([int(item) for item in line[0].split(',')])
        return matrix

    def heuristic_info(self, n):
        """ Método para regresar un valor del peso coherente: mayor peso, mejor solución"""

        # Si n es 0, entonces la información heurística del arco Nij es de un mismo nodo
        if n == 0:
            return 0
        return 1.0 / n

    def heuristic_info_from_list(self, list_info):
        return [self.heuristic_info(n) for n in list_info]

    def init_feromon_matrix(self, value = 1):
        """ Se inicia la matriz con un valor dado, por default 1 """
        
        # Primero en 0's, para que la diagonal principal quede en 0's
        feromon_matrix = [[int('0') for j in range(self.total_nodes)] for i in range(self.total_nodes)]
        
        for i in range(self.total_nodes):
            for j in range(self.total_nodes):
                if j > i:
                    feromon_matrix[i][j] = value
                    feromon_matrix[j][i] = feromon_matrix[i][j]
        return feromon_matrix

    def adyacent_arists(self, node, graph_matrix):
        total_nodes = len(graph_matrix)
        
        adyacent_arists = []
        for i in range(0, total_nodes):
            # Mientras el nodo no sea si mismo, hay una arista adyacente 
            if node is not i: 
                adyacent_arists.append(graph_matrix[node][i])
        return adyacent_arists

    
    def arist_selecc_probability(self, start_node, end_node):
        fm = self.feromon_matrix
        # Se convierte la información heurística a un valor coherente 
        hm = [self.heuristic_info_from_list(row) for row in self.heuristic_matrix]

        numerator = fm[start_node][end_node] * hm[start_node][end_node]
        denominator = sum(fm[start_node][posible_node] * hm[start_node][posible_node] for posible_node in range(0, self.total_nodes))

        return float(numerator) / float(denominator)

    def select_path(self):
        """ Mecanismo estocástico que sirve para seleccionar la arista a cruzar """
        pass

    
if len(sys.argv) != 2:
    print "Uso -> aco.py ARCHIVO_INSTANCIA"
    exit()

aco = AntColonyOptimization(sys.argv[1])

print 'Matriz feromona\tMatriz heurística(costo de aristas)'
for index, i in enumerate(aco.feromon_matrix):
    print i, '\t',  aco.heuristic_matrix[index]

