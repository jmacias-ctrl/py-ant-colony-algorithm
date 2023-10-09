import pandas as pd
import numpy as np
import sys
from time import process_time
from antcolonyprocess import *
from roulette import *

#Mejor solución python main.py 5 60 150 0.1 2.5 0.9

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

matrix_distance = calc_matrix_distancia(tamanio, values)

matrix_heuristica = gen_matrix_heuristica(matrix_distance)

mejor_hormiga, costo_mejor_hormiga = generar_hormiga_inicial(tamanio, matrix_distance)

matrix_feromona_global = np.zeros((tamanio, tamanio), dtype=float)+1/((tamanio+1)*costo_mejor_hormiga)

iteraciones = 1
tiempo_inicial = process_time()
while(iteraciones<=set_iteraciones):
    print('Iteracion', iteraciones)
    matrix_feromona = np.copy(matrix_feromona_global)
    ants_colony = generar_colonia_hormigas(tamanio, num_hormigas ,matrix_distance)
    for i in range(tamanio-1):
        for j in range(len(ants_colony)):
            ant = ants_colony[j]
            prob = np.random.random()
            ultima_ciudad = ant[i] - 1
            get_feromona = matrix_feromona[:, ultima_ciudad]
            get_heuristic = np.emath.power(matrix_heuristica[:, ultima_ciudad], p_valor_heuristica)
            producto_punto = get_feromona * get_heuristic
            if(prob<prob_limite):
                #print('transicion')
                for city in ant:
                    if(city!=0):
                        producto_punto[city-1]=0
                ciudad_seleccionado = np.argmax(producto_punto) + 1
                #print('ciudad_seleccionado: \n',ciudad_seleccionado )
                ants_colony[j][i+1] = ciudad_seleccionado
                matrix_feromona = update_matrix_feromona_local(matrix_feromona, matrix_feromona_global,ultima_ciudad, ciudad_seleccionado-1, tiempo_inicial, fe_feromona)
            else:
                #print('ruleta')
                ciudad_seleccionado = roulette(producto_punto,ant) + 1
                ants_colony[j][i+1] = ciudad_seleccionado
                matrix_feromona = update_matrix_feromona_local(matrix_feromona, matrix_feromona_global,ultima_ciudad, ciudad_seleccionado-1, tiempo_inicial, fe_feromona)
            #print(ant)

    mejor_hormiga, costo_mejor_hormiga = cheq_mejor_hormiga(ants_colony, mejor_hormiga, costo_mejor_hormiga, matrix_distance)

    matrix_feromona_global = update_matrix_feromona_global(matrix_feromona_global, tiempo_inicial, fe_feromona, costo_mejor_hormiga)
    iteraciones+=1

print('Mejor Solucion:\n',mejor_hormiga)
print('Distancia:',costo_mejor_hormiga)
print('Proceso terminado en '+str(process_time() - tiempo_inicial)+' segundos')