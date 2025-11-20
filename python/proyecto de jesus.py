import colorama
import numpy as np
import random as rn
from colorama import *
from numpy import *
from random import *

init()
# Función para mostrar el encabezado
def encabezado():
    print(Fore.BLUE+"UCAB Elaborado por: ",end="")
    print(Fore.MAGENTA+"Jesus Blanca, Diego García, Alessandro Perez y Eleam Villalta") 
    print("  Proyecto Avance 1  ")
    print()

# Función para mostrar los arreglos con colores
def mostrar_arreglos(f1, f2, f3, titulo=""):
    if titulo:
        print(f"\n{titulo}")

    print("       0   1   2   3") # Índices de columna para referencia

    # Mostrar F1
    print("F1[I]", end="  ")
    for celda in f1:
        color = Fore.BLUE if celda == 1 else Fore.RED
        print(f"{color}{celda}   ", end="")
    print()

    # Mostrar F2
    print("F2[I]", end="  ")
    for celda in f2:
        color = Fore.BLUE if celda == 1 else Fore.RED
        print(f"{color}{celda}   ", end="")
    print()

    # Mostrar F3
    print("F3[I]", end="  ")
    for celda in f3:
        color = Fore.BLUE if celda == 1 else Fore.RED
        print(f"{color}{celda}   ", end="")
    print()
    print()

# Función del Avance 2: Reglas de la Vida
def aplicar_reglas_vida(matriz, i, j):
    filas, cols = matriz.shape
    vecinos = 0
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            if (x == i and y == j) or x < 0 or y < 0 or x >= filas or y >= cols:
                continue
            vecinos += matriz[x, y]
    if matriz[i, j] == 1:
        if vecinos <= 1 or vecinos >= 4:
            return 0
        else:
            return 1
    else:
        if vecinos == 3:
            return 1
        else:
            return 0

def construir_cadena_c1(F1M, F2M, F3M):
    valores = lambda arr: ",".join(str(x) for x in arr)
    return f"F1M,{valores(F1M)},F2M,{valores(F2M)},F3M,{valores(F3M)}"

# Programa principal
if __name__ == "__main__":
    encabezado()

    # AVANCE 1
    # Declarar e inicializar los Arreglos utilizando únicamente Arreglos NUMPY
    # Los arreglos tienen 4 posiciones, como se infiere de las imágenes (0, 1, 2, 3)
    F1 = np.zeros(4, dtype=int)
    F2 = np.zeros(4, dtype=int)
    F3 = np.zeros(4, dtype=int)
    # Almacenar la información de forma Aleatoria, a excepción de F2[1] que debe ser 0 fijo
    for i in range(4):
        F1[i] = np.random.randint(0, 2) # Genera 0 o 1
        F2[i] = np.random.randint(0, 2)
        F3[i] = np.random.randint(0, 2)
    F2[1] = 0 # Requisito fijo para la posición F2[1]

# Mostrar la información del "Caldo Cultivo" inicial
    mostrar_arreglos(F1, F2, F3, titulo="Caldo Cultivo")

   # Aplicar las Reglas de la Vida SOLO sobre F2[1]
    # Crear nuevos arreglos para almacenar el estado modificado (F1M, F2M, F3M)
    F1M = np.copy(F1) # Copia F1 sin cambios para F1M
    F2M = np.copy(F2) # Copia F2 para modificar F2M[1]
    F3M = np.copy(F3) # Copia F3 sin cambios para F3M

    contador_vecinos_vivos = 0
    if F2[0] == 1: contador_vecinos_vivos += 1
    if F2[2] == 1: contador_vecinos_vivos += 1
    if F1[0] == 1: contador_vecinos_vivos += 1
    if F1[1] == 1: contador_vecinos_vivos += 1
    if F1[2] == 1: contador_vecinos_vivos += 1
    if F3[0] == 1: contador_vecinos_vivos += 1
    if F3[1] == 1: contador_vecinos_vivos += 1
    if F3[2] == 1: contador_vecinos_vivos += 1

# Estado actual de F2[1] antes de aplicar las reglas
    estado_actual_f2_1 = F2[1]
    nuevo_estado_f2_1 = estado_actual_f2_1# Por defecto, la celda mantiene su estado
# Aplicar las reglas del Juego de la Vida a F2[1]
    if estado_actual_f2_1 == 1: # Si la celda está viva (1)
        if contador_vecinos_vivos <= 1 or contador_vecinos_vivos >= 4: # REGLA 1: Solitud
            nuevo_estado_f2_1 = 0
        elif 2 <= contador_vecinos_vivos <= 3:
            nuevo_estado_f2_1 = 1
    else: # Si la celda está vacía (0)
        if contador_vecinos_vivos == 3:
            nuevo_estado_f2_1 = 1
    
    # Actualizar la posición F2M[1] con el nuevo estado
    F2M[1] = nuevo_estado_f2_1

# Mostrar la información de los arreglos F1M, F2M y F3M (después de la evolución)
    mostrar_arreglos(F1M, F2M, F3M, titulo="Evolución al cabo de una generación de la celda F2[1]")

    # Mensaje sobre la evolución de la celda F2[1]
    if nuevo_estado_f2_1 == 1 and estado_actual_f2_1 == 0:
        print("Mensaje: Nace una Célula en F2[1]")
    elif nuevo_estado_f2_1 == 0 and estado_actual_f2_1 == 1:
        print("Mensaje: La celda F2[1] muere")
    else: # El estado no cambió o sigue vacía/viva
        print("Mensaje: La celda F2[1] permanece Vacía" if nuevo_estado_f2_1 == 0 else "Mensaje: La celda F2[1] permanece Viva")
        
    # AVANCE 2
    input("\n\nPresione ENTER para mostrar la Primera Generación completa (Avance 2)...\n")
    F1 = np.random.randint(0, 2, 4)
    F2 = np.random.randint(0, 2, 4)
    F3 = np.random.randint(0, 2, 4)

    mostrar_arreglos(F1, F2, F3, titulo="Nuevo Caldo Cultivo para Avance 2")

    M = np.array([F1, F2, F3])
    M1 = np.zeros((3, 4), dtype=int)

    for i in range(3):
        for j in range(4):
            M1[i, j] = aplicar_reglas_vida(M, i, j)

    F1M, F2M, F3M = M1[0], M1[1], M1[2]
    mostrar_arreglos(F1M, F2M, F3M, titulo="Primera Generación")

    c1 = construir_cadena_c1(F1M, F2M, F3M)
    print("Cadena c1:")
    print(c1)
