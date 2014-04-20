import random
import sys

def instance_generator(length):
    matrix = [[int('0') for j in range(length)] for i in range(length)]

    for i in range(0, length):
        for j in range(0, length):
            if j > i:
                matrix[i][j] = random.randint(0, 1)
                matrix[j][i] = matrix[i][j]
    for i in matrix:
        print i

    instance = open('matriz_generada.txt', 'w')
    for i in matrix:
        instance.write(','.join(str(e) for e in i))
        instance.write('\n')
    print 'Instancia generada en el archivo "matriz_generada.txt"'

if len(sys.argv) != 2:
    print 'Uso -> python instance_generator.py TAMANO_MATRIZ'
    exit()

instance_generator(int(sys.argv[1]))
