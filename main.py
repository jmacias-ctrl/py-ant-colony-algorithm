import pandas as pd
import numpy as np
import sys
from time import process_time
from antcolonyprocess import *
from roulette import *

#Mejor solucion python main.py 3 100 250 0.1 2.5 0.9

np.set_printoptions(threshold=sys.maxsize)

if((len(sys.argv)-1)<6):
    sys.exit("Faltan argumentos \nEjecute: python main.py [semilla] [numero_hormiagas] [numero_iteraciones] [factor_evaporacion_feromona] [peso_heuristica] [probabilidad_limite]")


#crear la matriz de distancia D, calcular la distancias entre todos los nodos
seed = int(sys.argv[1])
num_hormigas = int(sys.argv[2])
set_iteraciones = int(sys.argv[3])
fe_feromona = float(sys.argv[4])
p_valor_heuristica = float(sys.argv[5])
prob_limite = float(sys.argv[6])

setSeed(seed)

df = pd.read_csv('berlin52.tsp.txt', sep=" ", header=None, names=["a", "b", "c", "d", 'e']).to_numpy()
df = np.delete(df, df.shape[0]-1, axis=0)
values = np.delete(df, [0,3,4], axis=1)
tamanio = values.shape[0]

matrix_distance = np.zeros((tamanio, tamanio), dtype=float)

for i in range(tamanio):
    for j in range(tamanio):
        coordinates_1 = values[i]
        coordinates_2 = values[j]
        radicante = ((coordinates_2[0]-coordinates_1[0])*(coordinates_2[0]-coordinates_1[0]))+((coordinates_2[1]-coordinates_1[1])*(coordinates_2[1]-coordinates_1[1]))
        matrix_distance[i][j] = radicante
        
matrix_distance = np.sqrt(matrix_distance)

#generar la matriz de la heuristica, es el inverso de la matriz de distancia (1/D)
matrix_heuristic = 1/matrix_distance
matrix_heuristic[matrix_heuristic>1e308]=0
#generar la matriz de feromona de tamaño de la matriz D, se debe dar un valor inicial Tij0=1/(n°variable/costo(primera solucion)) y el resto 0
mejor_hormiga, costo_mejor_hormiga = initial_ant(tamanio, matrix_distance)

matrix_feromona_global = np.zeros((tamanio, tamanio), dtype=float)+1/((tamanio+1)*costo_mejor_hormiga)

iteraciones = 1
t1_start = process_time()
while(iteraciones<=set_iteraciones):
    print('Iteracion', iteraciones)
    matrix_feromona = np.copy(matrix_feromona_global)
    ants_colony = set_ants_colony(tamanio, num_hormigas ,matrix_distance)
    for i in range(tamanio-1):
        for j in range(len(ants_colony)):
            ant = ants_colony[j]
            prob = np.random.random()
            ultima_ciudad = ant[i] - 1
            get_feromona = matrix_feromona[:, ultima_ciudad]
            get_heuristic = np.emath.power(matrix_heuristic[:, ultima_ciudad], p_valor_heuristica)
            producto_punto = get_feromona * get_heuristic
            if(prob<prob_limite):
                for city in ant:
                    if(city!=0):
                        producto_punto[city-1]=0
                ciudad_seleccionado = np.argmax(producto_punto) + 1
                ants_colony[j][i+1] = ciudad_seleccionado
                calc_feromona = calc_feromona_local(matrix_feromona[ultima_ciudad][ciudad_seleccionado-1],matrix_feromona_global[ultima_ciudad][ciudad_seleccionado-1],t1_start,fe_feromona)
                matrix_feromona[ultima_ciudad][ciudad_seleccionado-1] = calc_feromona
                matrix_feromona[ciudad_seleccionado-1][ultima_ciudad] = calc_feromona
            else:
                sum_producto_punto = np.sum(producto_punto)
                prob_eligir_nodo = producto_punto/sum_producto_punto
                for k in range(len(prob_eligir_nodo)):
                        if(k>0):
                            prob_eligir_nodo[k]+=prob_eligir_nodo[k-1]
                for city in ant:
                    if(city!=0):
                        prob_eligir_nodo[city-1]=0
                ciudad_seleccionado = roulette(tamanio, prob_eligir_nodo) + 1
                ants_colony[j][i+1] = ciudad_seleccionado
                calc_feromona = calc_feromona_local(matrix_feromona[ultima_ciudad][ciudad_seleccionado-1],matrix_feromona_global[ultima_ciudad][ciudad_seleccionado-1],t1_start,fe_feromona)
                matrix_feromona[ultima_ciudad][ciudad_seleccionado-1] = calc_feromona
                matrix_feromona[ciudad_seleccionado-1][ultima_ciudad] = calc_feromona

    for ant in ants_colony:
        solution_ant = calculate_distances(matrix_distance, ant)
        if(solution_ant<costo_mejor_hormiga):
            costo_mejor_hormiga = solution_ant
            mejor_hormiga = ant

    print('Mejor hormiga:\n', mejor_hormiga)
    print('Distancia:', costo_mejor_hormiga,'\n')

    for i in range(len(matrix_feromona_global)):
        for j in range(len(matrix_feromona_global[i])):
            matrix_feromona_global[i][j] = calc_feromona_global(matrix_feromona_global[i][j], t1_start, fe_feromona, costo_mejor_hormiga)
    iteraciones+=1

print('Mejor Solucion:\n',mejor_hormiga)
print('Distancia:',costo_mejor_hormiga)
print('Proceso terminado en '+str(process_time() - t1_start)+' segundos')