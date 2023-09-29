import pandas as pd
import numpy as np
import sys
import time
#np.set_printoptions(threshold=sys.maxsize)

#crear la matriz de distancia D, calcular la distancias entre todos los nodos
df = pd.read_csv('berlin52.tsp.txt', sep=" ", header=None, names=["a", "b", "c", "d", 'e']).to_numpy()
df = np.delete(df, df.shape[0]-1, axis=0)
values = np.delete(df, [0,3,4], axis=1)
matrix_distance = np.zeros((values.shape[0], values.shape[0]), dtype=float)
for i in range(values.shape[0]):
    for j in range(values.shape[0]):
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
matrix_feromona_inicial = np.zeros((values.shape[0], values.shape[0]), dtype=float)
for i in range(values.shape[0]):
    matrix_feromona_inicial[i][i] = 1/(values.shape[0]*1)
print(matrix_feromona_inicial)