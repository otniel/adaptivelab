# -*- coding: utf-8 -*-
import sys
import random
import copy
from math import e

class AntColonyOptimization:
	
    def __init__(self, matrix_file, ants):
        text_matrix = self.read_info_from_file(matrix_file) 
        self.heuristic_matrix = self.parse_matrix(text_matrix)
        self.total_nodes = len(self.heuristic_matrix)
        self.total_arists = self.total_nodes - 1
        self.pheromon_matrix = self.init_pheromon_matrix()        
        # Factor de decremento de la feromona p (letra griega rho)
        self.P = 0.3
        self.Q = 1.0
        self.used_arist_log = [[int('0') for j in range(self.total_nodes)]
                               for i in range(self.total_nodes)]
        self.ants = ants

    def init_pheromon_matrix(self, value = 1):
        """ Se inicia la matriz con un valor dado, por default 1 """
        # Primero en 0's, para que la diagonal principal quede en 0's
        pheromon_matrix = [[int('0') for j in range(self.total_nodes)] 
                           for i in range(self.total_nodes)]
        for i in range(self.total_nodes):
            for j in range(self.total_nodes):
                if j > i:
                    pheromon_matrix[i][j] = value
                    pheromon_matrix[j][i] = pheromon_matrix[i][j]
        return pheromon_matrix

    def get_heuristic_matrix(self):
        return self.heuristic_matrix

    def get_pheromon_matrix(self):
        return self.pheromon_matrix

    def read_info_from_file(self, file_name):
        return [line.rstrip('\r\n').split() 
                for line in list(open(file_name))]

    def parse_matrix(self, raw_matrix):
        """ Método para convertir la info tomada de un archivo a enteros """
        matrix = []
        for line in raw_matrix:
            matrix.append([int(item) for item in line[0].split(',')])
        return matrix

    def total_cost_tour(self, tour):
        arists = self.arists_from_tour(tour)
        return sum([self.heuristic_matrix[i][j] for i,j in arists])

    def heuristic_info(self, n):
        """ Método para regresar un valor del peso coherente: mayor peso, mejor solución"""
        # Si n es 0, entonces la información heurística del arco Nij es de un mismo nodo
        if n == 0:
            return 0
        return 1.0 / n

    def arists_from_tour(self, arist_list):
        return [tuple(arist_list[n-2:n]) for n in range(2, len(arist_list)+1)]

    def heuristic_info_from_list(self, list_info):
        return [self.heuristic_info(n) for n in list_info]

    def adyacent_nodes(self, node, graph_matrix):
        total_nodes = len(graph_matrix)
        adyacent_nodes = []
        for i in graph_matrix:
            # Mientras el nodo no sea si mismo, es un nodo adyacente 
            if node is not i: 
                adyacent_nodes.append(i)
        return adyacent_nodes
    
    def arist_selecc_probability(self, start_node, end_node):
        phm = self.pheromon_matrix
        # Se convierte la información heurística a un valor coherente 
        hm = [self.heuristic_info_from_list(row) 
              for row in self.heuristic_matrix]
        # http://i.imgur.com/XuvkcLI.png?1
        numerator = phm[start_node][end_node] * hm[start_node][end_node]
        denominator = sum(phm[start_node][posible_node] * hm[start_node][posible_node] 
                          for posible_node in range(0, self.total_nodes))
        return float(numerator) / float(denominator)

    def list_selection_probability(self, adyacent_nodes, ant):
        list_prob = dict()
        for adyacent in adyacent_nodes:
            if ant != adyacent:
                list_prob[ant, adyacent] = self.arist_selecc_probability(ant, adyacent)
        return list_prob
        
    def update_pheromon(self, tour):
        arists = self.arists_from_tour(tour)
        self.update_arist_log(arists)
        for i, j in arists:
            sum_pheromon = sum([self.pheromon_laid() for k in range(self.heuristic_matrix[i][j])])
            self.pheromon_matrix[i][j] = (1 - self.P) * self.pheromon_matrix[i][j] + sum_pheromon

    def pheromon_laid(self):
        return self.Q / self.total_nodes

    def update_arist_log(self, arists):
        for i,j in arists:
            self.used_arist_log[i][j] += 1 

    def best_tour(self, tours):
        tour_cost = {self.total_cost_tour(tour):tour for tour in tours}
        best = min(tour_cost.keys())
        return tour_cost[best], best

    def build_tour(self):        
        tour = []
        V = [node for node in range(self.total_nodes)]
        first = 0
        current = 0
        _sum = 0
        for node in range(self.total_arists):
            # Si el tour está vacío, se selecciona cualquier nodo para empezar. 
            if not tour:
                current = random.choice(V)
                first = current
                tour.append(first)    
            adyacent_nodes = self.adyacent_nodes(current, V)
            V.remove(current)
            list_prob = self.list_selection_probability(adyacent_nodes, current)
            random_probability = random.random()
            for nodes, probability in list_prob.items():
                _sum += probability
                if _sum >= random_probability or (random_probability - _sum) / random_probability < 1e-6:
                    current = nodes[1]
                    tour.append(current)
                    break
        tour.append(first)
        return tour

    def main(self):
        total_tours = []
        for ant in range(self.ants):
            tour = self.build_tour()
            total_tours.append(tour)
            self.update_pheromon(tour)
        for ant, tour in enumerate(total_tours):
            print 'Ant ', ant, ' -> ', tour, 'costo -> ', self.total_cost_tour(tour)
        best = self.best_tour(total_tours)
        print 'best tour founded: ', best[0], 'cost: ', best[1]

if len(sys.argv) != 3:
    print "Uso -> aco.py ARCHIVO_INSTANCIA TOTAL_HORMIGAS"
    exit()

aco = AntColonyOptimization(sys.argv[1], int(sys.argv[2]))
aco.main()
