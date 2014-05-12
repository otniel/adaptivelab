import random
import sys

def instance_generator(size, max_distance):
    """ Recibe como argumento el tamano de la matriz y la distancia maxima entre cada nodo """

    # Se inicializa la matriz llena de ceros
    matrix = [[int('0') for j in range(size)] for i in range(size)]

    # Se llena con numeros aleatorios entre 1 y la distancia maxima
    for x in range(0, size):
        for y in range(0, size):
            # Para que la matriz sea simetrica.
            # Se llena la mitad partiendo de la diagonal principal 
            if y > x:
                matrix[x][y] = random.randint(1, max_distance)
                # Despues el valor simetrico de la otra mitad se iguala al anterior
                matrix[y][x] = matrix[x][y]

    # Imprime matriz en forma legible
    for row in matrix:
        print row

    # Se escribe en un archivo
    file_name = 'tsp_'+str(size)+'_1.dat'
    instance = open(file_name, 'w')
    for row in matrix:
        instance.write(','.join(str(item) for item in row))
        instance.write('\n')
    print 'Instancia generada en el archivo "'+file_name+'"'
            
    
if len(sys.argv) != 3:
    print 'Uso-> instance_generator TAMANO MAX_DISTANCIA_NODOS'
    exit()

instance_generator(int(sys.argv[1]), int(sys.argv[2]))
