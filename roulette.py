import random
from datetime import datetime   
import numpy as np

#Busca el indice (Ciudad) mas cercano a un numero aleatorio de probabilidad dado
def buscar_rng_cercano(matrix_probabilidades, valor_rng):
    matrix_probabilidades = np.asarray(matrix_probabilidades)
    index = (np.abs(matrix_probabilidades - valor_rng)).argmin()
    return index


#Entrada:
#-producto_punto: el producto punto entre la matriz de heuristica y la feromona local
#-ant: Hormiga de la mejor solucion
#Salida:
#Retorna una ciudad aleatoria mediante el metodo de la ruleta
def roulette(producto_punto, ant):
    index = -1
    sum_producto_punto = np.sum(producto_punto)
    prob_eligir_nodo = producto_punto/sum_producto_punto
    for k in range(len(prob_eligir_nodo)):
            if(k>0):
                prob_eligir_nodo[k]+=prob_eligir_nodo[k-1]
    for city in ant:
        if(city!=0):
            prob_eligir_nodo[city-1]=-1
    while(index==-1):
        rng = np.random.random()
        index = buscar_rng_cercano(prob_eligir_nodo, rng)
    return index