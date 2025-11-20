import colorama
import numpy as np
import random as rn
from colorama import *
from numpy import *
from random import *

init(autoreset=True)


def generar_matrices_user(filas,columnas):
    matriz = []
    for _ in range(filas):
        fila = []
        for _ in range(columnas):
            valor = np.random.randint(0,2)
            fila.append(valor)
        matriz.append(fila)

    return matriz

def contar_vecinos(matriz,x,y):
    """
    Cuenta cauntas celulas vivas ( valor de 1) hay alrededor de la celda (x,y)
    (fila,columna). considerando los bordes como celulas vacias.
    """
    vecinos = 0
    filas = len(matriz)
    columnas = len(matriz[0])
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
    filas = len(matriz)
    columnas = len(matriz[0])
    nueva_matriz = []
    for i in range(filas):
        fila_nueva = []
        for j in range(columnas):
            vivos = contar_vecinos(matriz,i,j)
            if matriz[i][j] == 1:
                print('no life')
                # Regla 1: soledad
                if vivos <= 1:
                    fila_nueva.append(0)
                # Regla 2: superpoblacion
                elif vivos >= 4:
                    fila_nueva.append(0)
                # Regla 3: Supervivencia
                elif 2 <= vivos <= 3:
                    fila_nueva.append(1)
            else:
                # Regla 4: Nacimiento
                if vivos == 3:
                    fila_nueva.append(1)
                else:
                    fila_nueva.append(0)
        nueva_matriz.append(fila_nueva)
    return nueva_matriz


    
# Función para mostrar el encabezado con los nombres de los integrantes
def encabezado():
    print(Fore.BLUE + "UCAB Elaborado por: ", end="")
    print(Fore.MAGENTA + "Jesus Blanca, Alessandro Perez y Eleam Villalta") 
    print("  Proyecto Avance 2  ")
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

# Programa principal
def main ():
    filas = int(input('Ingrese el numero de filas : '))
    columnas = int(input("Ingrese el numero de columnas:"))
    m1 = generar_matrices_user(filas,columnas)
    print(m1)
    # m1 = [[1, 0, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0]]
    m2 = siguiente_generacion(matriz=m1)
    print('m2',m2)
    for fila in m2:
        print(fila)
    return
    encabezado() # Muestra el encabezado
    
    input("Presione ENTER para iniciar el programa...") 

    # Declarar e inicializar los Arreglos NUMPY (4 posiciones cada uno)
    F1 = np.zeros(4, dtype=int)
    F2 = np.zeros(4, dtype=int)
    F3 = np.zeros(4, dtype=int)

    # Almacenar la información de forma COMPLETAMENTE Aleatoria
    for i in range(4):
        F1[i] = np.random.randint(0, 2) # Genera 0 o 1
        F2[i] = np.random.randint(0, 2)
        F3[i] = np.random.randint(0, 2)
    
    # Ya NO hay requisito fijo para F2[1]

    # Mostrar la información del "Caldo Cultivo" inicial
    mostrar_arreglos(F1, F2, F3, titulo="Caldo Cultivo")

    #Avance 2: Generar la Primera Generación COMPLETA

    # Crear los arreglos para almacenar el estado modificado (F1M, F2M, F3M)
    F1M = np.copy(F1) 
    F2M = np.copy(F2)
    F3M = np.copy(F3)

    matriz = [list(F1M),list(F2M),list(F3M)]

    return
    # Recorrer cada celda del "tablero" conceptual (3 filas x 4 columnas)
    for fila_idx in range(3): # 0 para F1, 1 para F2, 2 para F3
        for col_idx in range(4): # 0, 1, 2, 3 para las columnas

            # Determinar a qué arreglo actual pertenece la celda (F1, F2 o F3)
            # y obtener el estado actual de esa celda.
            if fila_idx == 0:
                arreglo_actual_celda = F1
            elif fila_idx == 1:
                arreglo_actual_celda = F2
            else: # fila_idx == 2
                arreglo_actual_celda = F3
            
            estado_actual_celda = arreglo_actual_celda[col_idx]
            
            # Contar vecinos vivos
            vecinos_vivos = 0
            
            # Recorrer las filas y columnas adyacentes para contar vecinos
            for i_offset in [-1, 0, 1]: # -1: fila superior, 0: misma fila, 1: fila inferior
                for j_offset in [-1, 0, 1]: # -1: columna izquierda, 0: misma columna, 1: columna derecha
                    # No contar la celda central (la celda para la que estamos calculando los vecinos)
                    if i_offset == 0 and j_offset == 0:
                        continue

                    vecino_fila_abs = fila_idx + i_offset
                    vecino_col_abs = col_idx + j_offset

                    # Verificar que la posición del vecino esté dentro de los límites del "tablero" (3 filas, 4 columnas)
                    if 0 <= vecino_fila_abs < 3 and 0 <= vecino_col_abs < 4:
                        # Acceder al valor de la celda vecina según su fila y sumar si está viva (1)
                        if vecino_fila_abs == 0: # Vecino en F1
                            if F1[vecino_col_abs] == 1: # Usamos F1, F2, F3 (el estado inicial)
                                vecinos_vivos += 1
                        elif vecino_fila_abs == 1: # Vecino en F2
                            if F2[vecino_col_abs] == 1: # Usamos F1, F2, F3 (el estado inicial)
                                vecinos_vivos += 1
                        else: # Vecino en F3 (vecino_fila_abs == 2)
                            if F3[vecino_col_abs] == 1: # Usamos F1, F2, F3 (el estado inicial)
                                vecinos_vivos += 1
                                
            # Lógica de aplicar reglas (directamente aquí) ---
            nuevo_estado_celda = estado_actual_celda # Por defecto, la celda mantiene su estado

            if estado_actual_celda == 1: # Si la celda está viva
                if vecinos_vivos <= 1: # REGLA 1: Solitud
                    nuevo_estado_celda = 0 # La celda muere
                elif vecinos_vivos >= 4: # REGLA 2: Sobrepoblación
                    nuevo_estado_celda = 0 # La celda muere
                elif 2 <= vecinos_vivos <= 3: # REGLA 3: Supervivencia
                    nuevo_estado_celda = 1 # La celda sobrevive
            else: # Si la celda está vacía (0)
                if vecinos_vivos == 3: # REGLA 4: Nacimiento
                    nuevo_estado_celda = 1 # Nace una nueva célula
            
            # Almacenar el nuevo estado en el arreglo de la próxima generación (F_M)
            if fila_idx == 0:
                F1M[col_idx] = nuevo_estado_celda
            elif fila_idx == 1:
                F2M[col_idx] = nuevo_estado_celda
            else: # fila_idx == 2
                F3M[col_idx] = nuevo_estado_celda

    # Mostrar los arreglos de la "Primera Generación"
    mostrar_arreglos(F1M, F2M, F3M, titulo="Primera Generación")

    # Generar la cadena de caracteres (string) c1
    c1 = ""
    
    # Información de F1M
    c1 += "F1M," + ",".join(map(str, F1M)) + ","
    
    # Información de F2M
    c1 += "F2M," + ",".join(map(str, F2M)) + ","
    
    # Información de F3M
    c1 += "F3M," + ",".join(map(str, F3M))
    
    print("\nCadena c1 generada:")
    print(c1)

main()