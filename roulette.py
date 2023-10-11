import random
from datetime import datetime   
import numpy as np

#Entrada:
#-size: En este contexto, es el tamaño de la poblacion
#-items: En este contexto, es el array de los fitness de la poblacion
#-sum_items: En este contexto, es el fitness total, que es la suam de todos los fitness de la poblacion
#Salida:
#El fitness es un array de tamaño poblation_size, por lo tanto cada indice representa una fila del array 2d poblation
#que es el conjunto de cromosomas que son las posibles posiciones de table_size reinas
#Lo que hace esta ruleta es dividir todos los valores del array fitness por el total de fitness, dando una proporcion
#Luego recorremos el array y sumamos el valor de la proporcion n con el valor de la proporcion anterior n-1
#Esto nos da una probabilidad de 0 a 1
#Luego sacamos un numero aleatorio entre 0 y 1 y buscamos dentro del array el valor mas cercano al obtenido y obtenemos su indice
#lo hacemos por segunda vez y estos seran los dos indices padres de la poblacion y se retornan estos

def buscar_rng_cercano(matrix_probabilidades, valor_rng):
    matrix_probabilidades = np.asarray(matrix_probabilidades)
    index = (np.abs(matrix_probabilidades - valor_rng)).argmin()
    return index

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