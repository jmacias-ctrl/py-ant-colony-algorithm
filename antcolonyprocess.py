import numpy as np
from time import process_time

#Deja configurado la semilla para la aleatoriedad de los numeros generados
def setSeed(getSeed):
    np.random.seed(getSeed)
    return True

#Calcula y crea la matriz de distancia, aplicando distancia euclidiana en todos las coordenadas con todas las ciudades
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

#Actualiza la matriz de la feromona global, realizando los calculos respectivos en los segmentos de ciudades que ha visitado la hormiga con mejor solucion
#y reduciendo la feromona en el resto de los segmentos donde la hormiga no ha visitado
def update_matrix_feromona_global(matrix_feromona_global, fe_feromona, costo_mejor_hormiga, mejor_hormiga, tamanio):
    matrix_feromona_global = matrix_feromona_global*(1-fe_feromona)
    ciudad_1 = mejor_hormiga[0]-1
    for i in range(1, len(mejor_hormiga)):
        ciudad_2 = mejor_hormiga[i]-1
        matrix_feromona_global[ciudad_1][ciudad_2] = matrix_feromona_global[ciudad_1][ciudad_2] + fe_feromona*(1/costo_mejor_hormiga)
        matrix_feromona_global[ciudad_2][ciudad_1] = matrix_feromona_global[ciudad_1][ciudad_2] + fe_feromona*(1/costo_mejor_hormiga)
        ciudad_1 = ciudad_2
    matrix_feromona_global[mejor_hormiga[0]-1][mejor_hormiga[tamanio-1]-1] = matrix_feromona_global[mejor_hormiga[0]-1][mejor_hormiga[tamanio-1]-1] + fe_feromona*(1/costo_mejor_hormiga)
    matrix_feromona_global[mejor_hormiga[tamanio-1]-1][mejor_hormiga[0]-1] = matrix_feromona_global[mejor_hormiga[tamanio-1]-1][mejor_hormiga[0]-1] + fe_feromona*(1/costo_mejor_hormiga)

    #print(matrix_feromona_global)
    return matrix_feromona_global

#Actualiza la matriz de la feromona local, realiznado los calculos respectivos de reduccion de feromona de los segmentos no visitados por la hormiga y aumento de la feromona por
#los segmentos visitados por la hormiga
def update_matrix_feromona_local(matrix_feromona_local, matrix_feromona_global, hormiga, fe_feromona, tamanio):
    matrix_feromona_local = matrix_feromona_local*(1-fe_feromona)
    ciudad_1 = hormiga[0]-1
    for i in range(1, len(hormiga)):
        ciudad_2 = hormiga[i]-1
        matrix_feromona_local[ciudad_1][ciudad_2] = matrix_feromona_local[ciudad_1][ciudad_2] + fe_feromona*matrix_feromona_global[ciudad_1][ciudad_2]
        matrix_feromona_local[ciudad_2][ciudad_1] = matrix_feromona_local[ciudad_1][ciudad_2] + fe_feromona*matrix_feromona_global[ciudad_1][ciudad_2]
        ciudad_1 = ciudad_2
    matrix_feromona_local[hormiga[0]-1][hormiga[tamanio-1]-1] = matrix_feromona_local[hormiga[0]-1][hormiga[tamanio-1]-1] + fe_feromona*matrix_feromona_global[hormiga[0]-1][hormiga[tamanio-1]-1]
    matrix_feromona_local[hormiga[tamanio-1]-1][hormiga[0]-1] = matrix_feromona_local[hormiga[tamanio-1]-1][hormiga[0]-1] + fe_feromona*matrix_feromona_global[hormiga[tamanio-1]-1][hormiga[0]-1]
    return matrix_feromona_local

#Chequea si se encontro una mejor hormiga, se retornara la mejor hormiga encontrada, el costo de este y el costo de la mejor hormiga anterior
#Para que pueda ser utilizada para verificar si se ha encontrado una mejor hormiga o no
def cheq_mejor_hormiga(ants_colony, mejor_hormiga, costo_mejor_hormiga, matrix_distance):
    costo_mejor_hormiga_anterior = costo_mejor_hormiga
    for ant in ants_colony:
        solution_ant = calculate_distances(matrix_distance, ant)
        if(solution_ant<costo_mejor_hormiga):
            costo_mejor_hormiga = solution_ant
            mejor_hormiga = ant
    print('Mejor hormiga:\n', mejor_hormiga)
    print('Distancia:', costo_mejor_hormiga,'\n')
    return mejor_hormiga, costo_mejor_hormiga, costo_mejor_hormiga_anterior

#Genera la matriz de heuristica
def gen_matrix_heuristica(matrix_distance):
    matrix_heuristic = 1/matrix_distance
    matrix_heuristic[matrix_heuristic>1e308]=0
    return matrix_heuristic

#Calcula la distancia de las ciudades visitadas por una hormiga, hasta volver a la ciudad inicial que estuvo la hormiga
def calculate_distances(matrix_distance, ant):
    total_distance = 0
    last_city = ant[0] - 1
    for i in range(1,len(ant)):
        next_city = ant[i]-1
        total_distance += matrix_distance[last_city][next_city]
        last_city = next_city
    total_distance += matrix_distance[last_city][ant[0]-1]
    return total_distance

#Realiza el calculo de la feromona local
def calc_feromona_local(nivel_feromona, nivel_feromona_global, factor_evaporacion):
    return (1-factor_evaporacion)*nivel_feromona+ (factor_evaporacion*nivel_feromona_global) 

#Genera la colonia de hormigas de tamaño num_hormigas, donde la posicion inicial es escogido de manera aleatoria
def generar_colonia_hormigas(tamanio, num_hormigas,matrix_distance):
    ants_colony = np.zeros((num_hormigas, tamanio), dtype=int)
    for i in range(len(ants_colony)):
        ants_colony[i][0] = np.random.randint(1,tamanio+1)    
    return ants_colony

#Genera la hormiga inical que es un a solucion aleatoria de ciudades visitados
def generar_hormiga_inicial(tamanio, matrix_distance):
    set_hormiga = np.arange(1, tamanio+1)
    np.random.shuffle(set_hormiga)
    return set_hormiga, calculate_distances(matrix_distance, set_hormiga)


