import numpy as np

def setSeed(getSeed):
    np.random.seed(getSeed)
    return True

def calculate_distances(matrix_distance, ant):
    total_distance = 0
    last_city = ant[0]
    for i in range(1,len(ant)):
        total_distance += matrix_distance[last_city][ant[i]]
        last_city = ant[i]
    total_distance += matrix_distance[0][last_city]
    return total_distance
    
def calculate_distance_ant_colony(matrix_distance, num_hormigas, ants_colony):
    ants_distances = np.zeros(num_hormigas, dtype=float)
    for i in range(len(ants_colony)):
        ants_distances[i] = calculate_distances(matrix_distance, ants_colony[i])
    return ants_distances
        
def set_ants_colony(tamanio, num_hormigas,matrix_distance):
    ants_colony = np.zeros((num_hormigas, tamanio), dtype=int)
    for i in range(len(ants_colony)):
        ants_colony[i][0] = np.random.randint(1,tamanio-1)
    return ants_colony, calculate_distance_ant_colony(matrix_distance, num_hormigas, ants_colony)

def initial_ant(tamanio, matrix_distance):
    set_hormiga = np.arange(0, tamanio)
    np.random.shuffle(set_hormiga)
    return set_hormiga, calculate_distances(matrix_distance, set_hormiga)
    