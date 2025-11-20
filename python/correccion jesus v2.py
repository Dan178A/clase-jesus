import colorama
import numpy as np
import random as rn
import os
from colorama import *
from numpy import *
from random import *

init(autoreset=True)

def leer_archivo(nombre:str):
    if not os.path.exists(nombre):
        return []
    with open(nombre,'r') as file:
        lineas = file.read().splitlines()
    filas,columnas = map(int,lineas[0].split(','))
    matriz = np.full((filas,columnas),0,dtype=int)
    for linea in lineas[1:]:
        i,j = map(int,linea.split(','))
        matriz[i][j] = 1
    return matriz

def guardar_salida(matriz,nombre_del_archivo="ACASALI.TXT"):
    with open(nombre_del_archivo,'w') as file:
        columna = len(matriz)
        fila = len(matriz[0])
        for i in range(columna):
            for j in range(fila):
                if matriz[i][j] == 1:
                    file.write(f'{i},{j}\n')
    print(f"Resultado final guardado en {nombre_del_archivo}")

def encabezado():
    print(Fore.BLUE+"UCAB Elaborado por: ",end="")
    print(Fore.MAGENTA+"Jesus Blanca, Diego García, Alessandro Perez y Eleam Villalta") 
    print("  Proyecto Avance 1  ")
    print()

def simular_generaciones(matriz, gen_total):
    for gen in range(gen_total):
        if not any(1 in fila for fila in matriz):
            print(Fore.LIGHTRED_EX + "Todas las células murieron en la generación {gen}.")
            break
        print(Fore.LIGHTMAGENTA_EX + "Generación:", (gen+1))
        matriz = siguiente_generacion(matriz)
        mostrar_arreglo(matriz)
    return matriz

def generar_matrices_user(filas,columnas):
    matriz = []
    for i in range(0,filas):
        fila = []
        for i in range(0,columnas):
            valor = np.random.randint(0,2)
            fila.append(valor)
        matriz.append(fila)
    return matriz

def mostrar_arreglo(Matriz):
    for i in range(len(Matriz)):
        fila = ""
        for j in range(len(Matriz[i])):
            if Matriz[i][j] == 1:
                fila += Fore.LIGHTGREEN_EX + "1 "
            elif Matriz[i][j] == 0:
                fila += Fore.LIGHTRED_EX + "0 "
            elif Matriz[i][j] == 2:
                fila += Fore.LIGHTYELLOW_EX + "A "
        print(fila)
    print()

def aplicar_reglas_vida(matriz, i, j):
    filas, cols = np.shape(matriz)
    vecinos = 0
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            if (x == i and y == j) or (x < 0) or (y < 0) or (x >= filas) or (y >= cols):
                continue
            vecinos += matriz[x][y]
    if matriz[i][j] == 1:
        if (vecinos <= 1) or (vecinos >= 4):
            return 0
        else:
            return 1
    else:
        if (vecinos == 3) or (vecinos == 2):
            return 1
        else:
            return 0

def siguiente_generacion(matriz):
    filas, columnas = np.shape(matriz)
    nueva_matriz = []
    for i in range(filas):
        nueva_fila = []
        for j in range(columnas):
            nueva_fila.append(aplicar_reglas_vida(matriz, i, j))
        nueva_matriz.append(nueva_fila)
    return nueva_matriz

def recorrido_espiral(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    recorrido = []
    top, bottom = 0, filas - 1
    left, right = 0, columnas - 1
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            recorrido.append((top, j))
        top += 1
        for i in range(top, bottom + 1):
            recorrido.append((i, right))
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                recorrido.append((bottom, j))
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                recorrido.append((i, left))
            left += 1
    return recorrido

def recorrido_diagonal(matriz):
    recorrido = []
    filas, columnas = len(matriz), len(matriz[0])
    for s in range(columnas-2,-1,-1): 
        i = 0
        j = s
        while i < filas and j >= 0:
            recorrido.append((i, j))
            i += 1
            j -= 1
    return recorrido

def recorrido_zigzag(matriz):
    recorrido = []
    for j in range(len(matriz)):
        if j % 2 == 0:
            for i in range(len(matriz[0])):
                recorrido.append((i, j))
        else:
            for i in range(len(matriz[0])):
                recorrido.append((i, j))
    return recorrido

def milagro_1(matriz): 
    recorrido = recorrido_espiral(matriz)
    impares = []

    for i, j in recorrido:
        if i % 2 == 1 and j % 2 == 1:
            impares.append((i, j))

    libres = []
    for i, j in impares:
        if matriz[i][j] == 0:
            libres.append((i, j))

    if len(libres) >= int(0.5 * len(impares)) and libres:
        i, j = libres[0]
        matriz[i][j] = 2
        print(Fore.LIGHTMAGENTA_EX+"¡Milagro! Nació célula ángel en la posición", (i,j))
        mostrar_arreglo(matriz)
    else:
        print(Fore.LIGHTRED_EX+"No ocurrió ningún milagro.")

def milagro2(matriz):
    recorrido = recorrido_diagonal(matriz)
    nueva_matriz = matriz.copy()
    candidatos = []
    total_x_par = 0

    for i, j in recorrido:
        if i % 2 == 0:
            total_x_par += 1
            if matriz[i][j] == 0:
                candidatos.append((i, j))

    if len(candidatos) >= int(0.7 * total_x_par):
        i, j = candidatos[-1]
        nueva_matriz[i][j] = 2
        print(Fore.LIGHTMAGENTA_EX+"¡Milagro! Nació célula ángel en", (i,j))
        mostrar_arreglo(nueva_matriz)
    else:
        print(Fore.LIGHTRED_EX+"No ocurrió ningún milagro.")

def milagro3(matriz):
    nueva_matriz = matriz.copy()
    recorrido = recorrido_zigzag(matriz)
    candidatos = []
    total_y_impar = 0
    for i, j in recorrido:
        if j % 2 == 1:
            total_y_impar += 1
            if matriz[i][j] == 0:
                candidatos.append((i, j))
    if len(candidatos) >= int(0.6 * total_y_impar):
        segunda_mitad = recorrido[len(recorrido)//2:]
        for i, j in segunda_mitad:
            if (i, j) in candidatos:
                nueva_matriz[i][j] = 2
                print(Fore.LIGHTMAGENTA_EX+"¡Milagro! Nació célula ángel en", (i,j))
                mostrar_arreglo(nueva_matriz)
                break
    else:
        print(Fore.LIGHTRED_EX+"No ocurrió ningún milagro.")

def generar_caldo_aleatorio(filas:int,columnas:int,vivas:int):
    matrix = np.full((filas,columnas),0,dtype=int)
    posiciones = []
    for i in range(filas):
        for j in range(columnas):
            posiciones.append((i,j))
    rn.shuffle(posiciones)
    for i in range(min(vivas,(len(posiciones)))):
        x,y = posiciones[i]
        matrix[x][y] = 1
    return matrix

def menu():
    filas,columnas = 0,0
    file_name = "ACAENTRA.txt"
    tablero_actual = []
    opcion = 0
    while True:
        print('\n --- Automata Celular ---')
        print("1. Cargar caldo inicial desde archivo")
        print("2. Generar caldo inicial aleatorio")
        print("0. Salir")
        opcion = input("Elige una opción: ")

        if opcion == '1':
            tablero_actual = leer_archivo(file_name)
            filas = len(tablero_actual[0])
            columnas = len(tablero_actual)
        elif opcion == '2':
            modo = input("deseas crear aleatorias(A) o persolizadas(B) ?").strip().upper()
            if modo == 'A':
                filas = rn.randint(0,21)
                columnas = rn.randint(0,21)
                vivas = int(input("Cantidad de celulas vivas:"))
                tablero_actual = generar_caldo_aleatorio(filas,columnas,vivas)
            else:
                filas = int(input(Fore.LIGHTBLACK_EX+"Introduce la cantidad de filas de una matriz: "))
                columnas = int(input(Fore.LIGHTBLACK_EX+"Introduce la cantidad de columnas de una matriz: "))
                tablero_actual = generar_matrices_user(filas,columnas)
    
            

def main():
    encabezado()
    filas = int(input(Fore.LIGHTBLACK_EX+"Introduce la cantidad de filas de una matriz: "))
    columnas = int(input(Fore.LIGHTBLACK_EX+"Introduce la cantidad de columnas de una matriz: "))
    if (filas > 20) or (columnas > 20):
        print(Fore.RED+"¡ERROR! ¡DIMENSIONES MUY GRANDES!")
    else:
        M = generar_matrices_user(filas,columnas)
        print(Fore.LIGHTBLACK_EX+"La matriz:")
        mostrar_arreglo(M)
        generaciones = int(input(Fore.LIGHTBLACK_EX+"¿Cuántas generaciones quiere que se simulen?: "))
        M2 = simular_generaciones(M,generaciones)
        print(Fore.LIGHTBLACK_EX+"¿Quieres aplicar un milagro?")
        print(Fore.MAGENTA+"      1. Si")
        print(Fore.MAGENTA+"      2. No")
        Sel=int(input())
        if Sel==1:
            print(Fore.LIGHTBLACK_EX+"¿Cuál quieres aplicar?")
            print(Fore.MAGENTA+"      Milagro 1")
            print(Fore.MAGENTA+"      Milagro 2")
            print(Fore.MAGENTA+"      Milagro 3")
            Opt=int(input())
            if Opt==1:
                milagro_1(M2)
            elif Opt==2:
                milagro2(M2)
            elif Opt==3:
                milagro3(M2)
            else:
                print(Fore.LIGHTRED_EX+"ERROR. OPCIÓN INVÁLIDA.")
        elif Sel==2:
            print(Fore.CYAN+"Fin del programa")
        else:
            print(Fore.LIGHTRED_EX+"ERROR. OPCIÓN INVÁLIDA.")
# # main()
if __name__ == "__main__":
    menu()

#     matriz = leer_archivo('ACAENTRA.txt')
#     guardar_salida(matriz)