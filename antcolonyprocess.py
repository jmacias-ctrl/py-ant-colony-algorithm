import numpy as np

def setSeed(getSeed):
    np.random.seed(getSeed)
    return True

def calculate_distances(matrix_distance, ant):
    total_distance = matrix_distance[0][ant[0]]
    last_city = ant[1]
    for i in range(2,len(ant)):
        total_distance += matrix_distance[last_city][ant[i]]
        last_city = ant[i]
    total_distance += matrix_distance[0][last_city]
    return total_distance

def initial_ant(tamanio, matrix_distance):
    set_hormiga = np.arange(1, tamanio)
    np.random.shuffle(set_hormiga)
    return set_hormiga, calculate_distances(matrix_distance ,set_hormiga)
    