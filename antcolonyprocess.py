import numpy as np
from time import process_time

def setSeed(getSeed):
    np.random.seed(getSeed)
    return True

def calculate_distances(matrix_distance, ant):
    total_distance = 0
    last_city = ant[0] - 1
    for i in range(1,len(ant)):
        total_distance += matrix_distance[last_city][ant[i]-1]
        last_city = ant[i] - 1
    return total_distance

def calc_feromona_global(nivel_feromona, tiempo_inicial, factor_evaporacion, costo_mejor_solucion):
    t = (process_time() - tiempo_inicial)-1
    if(t<0):
        t = t*-1
    nivel_feromona = ((1-factor_evaporacion)*pow(nivel_feromona,t)) + (factor_evaporacion*(1/costo_mejor_solucion))
    return nivel_feromona

def calc_feromona_local(nivel_feromona, nivel_feromona_global,tiempo_inicial, factor_evaporacion):
    t = (process_time() - tiempo_inicial)-1
    if(t<0):
        t = t*-1
    nivel_feromona = ((1-factor_evaporacion)*pow(nivel_feromona,t)) + (factor_evaporacion*nivel_feromona_global)
    return nivel_feromona

def set_ants_colony(tamanio, num_hormigas,matrix_distance):
    ants_colony = np.zeros((num_hormigas, tamanio), dtype=int)
    for i in range(len(ants_colony)):
        ants_colony[i][0] = np.random.randint(1,tamanio+1)
    return ants_colony

def initial_ant(tamanio, matrix_distance):
    set_hormiga = np.arange(1, tamanio+1)
    np.random.shuffle(set_hormiga)
    return set_hormiga, calculate_distances(matrix_distance, set_hormiga)
    