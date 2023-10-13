import pandas as pd
import numpy as np
import sys
from time import process_time
from antcolonyprocess import *
from roulette import *

#Integrantes: Jose Macias, Rodrigro Sanchez

#Mejor solución python main.py 43123 80 500 0.1 2.5 0.9 
#Distancia 7544.365901904086

#np.set_printoptions(threshold=sys.maxsize)

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
matriz_coordenadas = np.delete(df, [0,3,4], axis=1)
tamanio = matriz_coordenadas.shape[0]

matrix_distance = calc_matrix_distancia(tamanio, matriz_coordenadas)

matrix_heuristica = gen_matrix_heuristica(matrix_distance)

mejor_hormiga, costo_mejor_hormiga = generar_hormiga_inicial(tamanio, matrix_distance)
matrix_feromona_global = np.zeros((tamanio, tamanio), dtype=float)+1/((tamanio+1)*costo_mejor_hormiga)
print('Hormiga Inicial')
print(mejor_hormiga)
print('Costo: ', costo_mejor_hormiga)
iteraciones = 1
tiempo_inicial_algoritmo = process_time()
while(iteraciones<=set_iteraciones):
    print('Iteracion', iteraciones)
    matrix_feromona = np.copy(matrix_feromona_global)
    colonia_hormigas = generar_colonia_hormigas(tamanio, num_hormigas ,matrix_distance)
    #for i in range(tamanio-1):
    #    for j in range(len(colonia_hormigas)):
    for j in range(len(colonia_hormigas)):
        for i in range(tamanio-1):
            hormiga = colonia_hormigas[j]
            prob = np.random.random()
            ultima_ciudad_visitada = hormiga[i] - 1
            get_feromona = matrix_feromona[:, ultima_ciudad_visitada]
            get_heuristic = np.power(matrix_heuristica[:, ultima_ciudad_visitada], p_valor_heuristica)
            producto_punto = get_feromona * get_heuristic
            if(prob<prob_limite):
                for city in hormiga:
                    if(city!=0):
                        producto_punto[city-1]=-1
                ciudad_seleccionado = np.argmax(producto_punto) + 1
                colonia_hormigas[j][i+1] = ciudad_seleccionado
            else:
                ciudad_seleccionado = roulette(producto_punto,hormiga) + 1
                colonia_hormigas[j][i+1] = ciudad_seleccionado
        matrix_feromona = update_matrix_feromona_local(matrix_feromona, matrix_feromona_global, hormiga, fe_feromona, tamanio)
    mejor_hormiga, costo_mejor_hormiga, costo_mejor_hormiga_anterior = cheq_mejor_hormiga(colonia_hormigas, mejor_hormiga, costo_mejor_hormiga, matrix_distance)
    matrix_feromona_global = update_matrix_feromona_global(matrix_feromona_global, fe_feromona, costo_mejor_hormiga, mejor_hormiga, tamanio)
    iteraciones+=1

print('Mejor Solucion Encontrada:\n',mejor_hormiga)
print('Distancia:',costo_mejor_hormiga)
print('Proceso terminado en '+str(process_time() - tiempo_inicial_algoritmo)+' segundos')