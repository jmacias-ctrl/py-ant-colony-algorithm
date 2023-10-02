import pandas as pd
import numpy as np
import sys
import time
from antcolonyprocess import *

#np.set_printoptions(threshold=sys.maxsize)

if((len(sys.argv)-1)<6):
    sys.exit("Faltan argumentos \nEjecute: python main.py [semilla] [numero_hormiagas] [numero_iteraciones] [factor_evaporacion_feromona] [peso_heuristica] [probabilidad_limite]")
#crear la matriz de distancia D, calcular la distancias entre todos los nodos
seed = int(sys.argv[1])
num_hormigas = int(sys.argv[2])
iteraciones = int(sys.argv[3])
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
        if(radicante==0):
            radicante = 1
        matrix_distance[i][j] = radicante
matrix_distance = np.sqrt(matrix_distance)

#generar la matriz de la heuristica, es el inverso de la matriz de distancia (1/D)
matrix_heuristic = 1/matrix_distance

#generar la matriz de feromona de tamaño de la matriz D, se debe dar un valor inicial Tij0=1/(n°variable/costo(primera solucion)) y el resto 0
hormiga_inicial, costo_hormiga_inicial = initial_ant(tamanio, matrix_distance)
matrix_feromona_inicial = np.zeros((tamanio, tamanio), dtype=float)+1/((tamanio+1)*costo_hormiga_inicial)
print(matrix_feromona_inicial)