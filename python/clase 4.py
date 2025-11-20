import colorama
import numpy as np
import random as rn
from colorama import *
from numpy import *
from random import *


def imprimir_pos(matrizx):
    """
        matrizx: la matriz de numpy
        imprimir las posiciones donde hay vida
    """
    posiciones = []
    for i in range(len(matrizx)):
        for j in range(len(matrizx[0])):
            if matrizx[i][j] == 1:
                posiciones.append((i, j))
                print(f"({i},{j})")
    return posiciones


def generar_matrices_user(filas,columnas):
    matriz = []
    for _ in range(0,filas,1):
        fila = []
        for i in range(0,columnas,1):
            valor = np.random.randint(0,2)
            fila.append(valor)
        matriz.append(fila)

    return matriz

def contar_vecinos(matriz,x,y):
    """
    Cuenta cuantas celulas vivas ( valor de 1) hay alrededor de la celda (x,y)
    (fila,columna). considerando los bordes como celulas vacias.
    """
    vecinos = 0
    # shape son las dimensiones de la matriz
    filas,columnas = matriz.shape
    # Desplazamiento en filas y columnas
    desplazamiento = [-1, 0, 1] 
    # recorrer las posiciones vecinas (inclyendo diagonales)
    for dx in desplazamiento: # Desplazamiento en filas
        for dy in desplazamiento: # Desplazamiento en columnas
            if dx == 0 and dy == 0:
                continue # saltar la celda central (x,y)
            else:
                nx = x + dx # fila vecina
                ny = y + dy # columna vecina
                # verificar si la posicion esta dentro de los limites
                if 0 <= nx < filas and 0 <= ny < columnas:
                    if matriz[nx][ny] == 1:
                        vecinos += 1
    return vecinos 

def siguiente_generacion(matriz):
    """
    Aplica las reglas y devuelve la nueva matriz
    """
    # Asegurarse que sea un arreglo de NUMPY
    matriz=np.array(matriz)
    filas,columnas = matriz.shape
    nueva_matriz = np.zeros((filas, columnas), dtype=int)    
    for i in range(filas):
        for j in range(columnas):
            vivos = contar_vecinos(matriz,i,j)
            if matriz[i][j] == 1:
                # Regla 1: soledad
                if vivos <= 1:
                    nueva_matriz[i,j]=0
                # Regla 2: superpoblacion
                elif vivos >= 4:
                    nueva_matriz[i,j]=0
                # Regla 3: Supervivencia
                elif 2 <= vivos <= 3:
                    nueva_matriz[i,j]=1
            else:
                # Regla 4: Nacimiento
                if vivos == 3:
                    nueva_matriz[i,j]=1
                else:
                    nueva_matriz[i,j]=0

    # retornar un arreglo de listas de numpy
    return nueva_matriz.tolist()


if __name__ == "__main__":
    filas = int(input('Ingrese el numero de filas : '))
    columnas = int(input("Ingrese el numero de columnas:"))

    m1 = generar_matrices_user(filas,columnas)
    m2 = siguiente_generacion(matriz=m1)
    print("Estas son las posiciones donde SÍ hay vida:")
    print(imprimir_pos(m1))
    print(imprimir_pos(m2))