# -*- coding: utf-8 -*-
import sys

class ComplexNetwork:
    def __init__(self, matrix_file):
        text_matrix = [line.rstrip('\r\n').split() for line in list(open(matrix_file))]
        self.matrix = self.parse_matrix(text_matrix)
        self.vertex_number = len(self.matrix)
        self.grades = {}
        self.edges = 0

    def parse_matrix(self, raw_matrix):
        matrix = []
        for line in raw_matrix:
            matrix.append([int(item) for item in line[0].split(',')])
        return matrix

    def init_grades(self):
        for index, item in enumerate(self.matrix):
            self.grades[index] = sum(item)
    
    def init_edges(self):
        for index, item in enumerate(self.matrix):
            self.edges += self.grades[index]
        self.edges = self.edges / 2

    def get_grades(self):
        return self.grades

    def get_edges(self):
        return self.edges 
            
    def get_vertex_number(self):
        return self.vertex_number

    def print_matrix_detail(self):
        for index, line in enumerate(self.matrix):
            print line, 'Grado : %d\t Centralidad: %.1f\t Distribución de grado: %.4f' \
                % (self.grades[index], self.get_centrality(index), self.grade_distribution(index) )
            
    def get_density(self):
        m = self.get_edges()
        n = self.get_vertex_number()
        numerator = float(2*m)
        denominator = float(n*(n-1))
        return numerator / denominator

    def get_centrality(self, vertex):
       vertex_grade = float(self.grades[vertex])
       n = self.get_vertex_number()
       return vertex_grade / (n-1)

    def grade_distribution(self, vertex):
        vertex_grade = float(self.grades[vertex])
        return vertex_grade / self.get_vertex_number()

if len(sys.argv) != 2:
    print 'Uso: redes.py ARCHIVO'
    exit()

cn = ComplexNetwork(sys.argv[1])
cn.init_grades()
cn.init_edges()

print cn.print_matrix_detail()
print 'Densidad de la red:\t', cn.get_density()
print 'Vertices:\t\t', cn.get_vertex_number()
print 'Aristas:\t\t', cn.get_edges()
