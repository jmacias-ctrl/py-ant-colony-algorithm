import numpy as np
from time import process_time

def setSeed(getSeed):
    np.random.seed(getSeed)
    return True

def calc_matrix_distancia(tamanio, matriz_coordenadas):
    matrix_distance = np.zeros((tamanio, tamanio), dtype=float)
    for i in range(tamanio):
        for j in range(tamanio):
            coordinates_1 = matriz_coordenadas[i]
            coordinates_2 = matriz_coordenadas[j]
            radicante = ((coordinates_2[0]-coordinates_1[0])*(coordinates_2[0]-coordinates_1[0]))+((coordinates_2[1]-coordinates_1[1])*(coordinates_2[1]-coordinates_1[1]))
            matrix_distance[i][j] = radicante
    matrix_distance = np.sqrt(matrix_distance)
    return matrix_distance

def update_matrix_feromona_global(matrix_feromona_global, tiempo_inicial, fe_feromona, costo_mejor_hormiga):
    t = (process_time() - tiempo_inicial) - 1
    matrix_feromona_global = np.power(matrix_feromona_global, t)
    matrix_feromona_global = matrix_feromona_global * (1-  fe_feromona)
    matrix_feromona_global = matrix_feromona_global + fe_feromona*(1/costo_mejor_hormiga)
    return matrix_feromona_global

def update_matrix_feromona_local(matrix_feromona_local, matrix_feromona_global,nodo_1, nodo_2, tiempo_inicial, fe_feromona):
    calc_feromona = calc_feromona_local(matrix_feromona_local[nodo_1][nodo_2],matrix_feromona_global[nodo_1][nodo_2],tiempo_inicial,fe_feromona)
    matrix_feromona_local[nodo_1][nodo_2] = calc_feromona
    matrix_feromona_local[nodo_2][nodo_1] = calc_feromona
    return matrix_feromona_local

def cheq_mejor_hormiga(ants_colony, mejor_hormiga, costo_mejor_hormiga, matrix_distance):
    for ant in ants_colony:
        solution_ant = calculate_distances(matrix_distance, ant)
        if(solution_ant<costo_mejor_hormiga):
            costo_mejor_hormiga = solution_ant
            mejor_hormiga = ant
    print('Mejor hormiga:\n', mejor_hormiga)
    print('Distancia:', costo_mejor_hormiga,'\n')
    return mejor_hormiga, costo_mejor_hormiga

def gen_matrix_heuristica(matrix_distance):
    matrix_heuristic = 1/matrix_distance
    matrix_heuristic[matrix_heuristic>1e308]=0
    return matrix_heuristic

def calculate_distances(matrix_distance, ant):
    total_distance = 0
    last_city = ant[0] - 1
    for i in range(1,len(ant)):
        next_city = ant[i]-1
        total_distance += matrix_distance[last_city][next_city]
        last_city = next_city
    total_distance += matrix_distance[last_city][ant[0]-1]
    return total_distance

def calc_feromona_local(nivel_feromona, nivel_feromona_global,tiempo_inicial, factor_evaporacion):
    t = (process_time() - tiempo_inicial)-1
    update_feromona = ((1-factor_evaporacion)*pow(nivel_feromona,t)) + (factor_evaporacion*nivel_feromona_global)
    return update_feromona

def generar_colonia_hormigas(tamanio, num_hormigas,matrix_distance):
    ants_colony = np.zeros((num_hormigas, tamanio), dtype=int)
    for i in range(len(ants_colony)):
        ants_colony[i][0] = np.random.randint(1,tamanio+1)    
    return ants_colony

def generar_hormiga_inicial(tamanio, matrix_distance):
    set_hormiga = np.arange(1, tamanio+1)
    np.random.shuffle(set_hormiga)
    return set_hormiga, calculate_distances(matrix_distance, set_hormiga)
    