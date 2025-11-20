import numpy as np
import random

# -------------------------------
# Función para leer ACAENTRA.TXT
# -------------------------------
def leer_archivo(nombre:str):
    with open(nombre, 'r') as f:
        lineas = f.read().splitlines()
    filas, columnas = map(int, lineas[0].split(","))
    matriz = np.full((filas, columnas), 0, dtype=int)
    for linea in lineas[1:]:
        i, j = map(int, linea.split(","))
        matriz[i][j] = 1
    return matriz

# -------------------------------
# Función para guardar en ACASALI.TXT
# -------------------------------
def guardar_salida(matriz:np.ndarray, nombre_archivo="ACASALI.TXT"):
    with open(nombre_archivo, "w") as f:
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                if matriz[i][j] == 1:
                    f.write(f"{i},{j}\n")
    print(f"Resultado final guardado en {nombre_archivo}")

# -------------------------------
# Visualizar matriz (coordenadas vivas)
# -------------------------------
def imprimir_posiciones(matriz:np.ndarray):
    print("Coordenadas con células vivas:")
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == 1:
                print(f"({i},{j})")

# -------------------------------
# Contar vecinos
# -------------------------------
def contar_vecinos(matriz:np.ndarray, x:int, y:int):
    vecinos = 0
    filas, columnas = matriz.shape
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                vecinos += matriz[nx][ny]
    return vecinos

# -------------------------------
# Reglas del autómata
# -------------------------------
def siguiente_generacion(matriz:np.ndarray):
    filas, columnas = matriz.shape
    nueva = np.full((filas, columnas), 0, dtype=int)
    for i in range(filas):
        for j in range(columnas):
            vecinos = contar_vecinos(matriz, i, j)
            if matriz[i][j] == 1:
                if vecinos == 2 or vecinos == 3:
                    nueva[i][j] = 1
            else:
                if vecinos == 3:
                    nueva[i][j] = 1
    return nueva

# -------------------------------
# Milagro 1 - Espiral
# -------------------------------
def milagro_1(matriz:np.ndarray):
    filas, columnas = matriz.shape
    recorrido = []
    top, bottom, left, right = 0, filas - 1, 0, columnas - 1

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

    impares = [(i, j) for i, j in recorrido if i % 2 == 1 and j % 2 == 1]
    libres = [pos for pos in impares if matriz[pos[0]][pos[1]] == 0]

    if len(libres) >= int(0.5 * len(impares)) and libres:
        x, y = libres[0]
        matriz[x][y] = 1
        print(f"🌟 Milagro 1: nació en ({x},{y})")

# -------------------------------
# Milagro 2 - Diagonal secundaria inferior
# -------------------------------
def milagro_2(matriz:np.ndarray):
    filas, columnas = matriz.shape
    recorrido = []
    for k in range(filas + columnas - 1):
        for i in range(filas):
            j = columnas - 1 - k + i
            if 0 <= j < columnas:
                recorrido.append((i, j))

    pares_x = [(i, j) for i, j in recorrido if i % 2 == 0]
    libres = [pos for pos in pares_x if matriz[pos[0]][pos[1]] == 0]

    if len(libres) >= int(0.7 * len(pares_x)) and libres:
        x, y = libres[-1]
        matriz[x][y] = 1
        print(f"🌟 Milagro 2: nació en ({x},{y})")

# -------------------------------
# Milagro 3 - Zigzag vertical
# -------------------------------
def milagro_3(matriz:np.ndarray):
    filas, columnas = matriz.shape
    recorrido = []
    for j in range(columnas):
        if j % 2 == 0:
            for i in range(filas):
                recorrido.append((i, j))
        else:
            for i in reversed(range(filas)):
                recorrido.append((i, j))

    impar_y = [(i, j) for i, j in recorrido if j % 2 == 1]
    libres = [pos for pos in impar_y if matriz[pos[0]][pos[1]] == 0]

    if len(libres) >= int(0.6 * len(impar_y)) and libres:
        segunda_mitad = recorrido[len(recorrido)//2:]
        for x, y in segunda_mitad:
            if (x, y) in libres:
                matriz[x][y] = 1
                print(f"🌟 Milagro 3: nació en ({x},{y})")
                break

# -------------------------------
# Aplicar todos los milagros
# -------------------------------
def aplicar_milagros(matriz:np.ndarray):
    milagro_1(matriz)
    milagro_2(matriz)
    milagro_3(matriz)

# -------------------------------
# Generar configuración aleatoria
# -------------------------------
def generar_caldo_aleatorio(filas, columnas, vivas):
    matriz = np.full((filas, columnas), 0, dtype=int)
    posiciones = []
    for i in range(filas):
        for j in range(columnas):
            posiciones.append((i, j))
    random.shuffle(posiciones)
    for i in range(min(vivas, len(posiciones))):
        x, y = posiciones[i]
        matriz[x][y] = 1
    return matriz

# -------------------------------
# Menú principal
# -------------------------------
def menu():
    print("Bienvenido al Proyecto ACA - ALIVE")
    modo = input("¿Deseas cargar desde archivo (A) o generar aleatorio (R)? ").strip().upper()
    
    if modo == "A":
        matriz = leer_archivo("ACAENTRA.TXT")
    else:
        filas = int(input("Número de filas: "))
        columnas = int(input("Número de columnas: "))
        vivas = int(input("Cantidad de células vivas iniciales: "))
        matriz = generar_caldo_aleatorio(filas, columnas, vivas)

    generaciones = int(input("¿Cuántas generaciones desea simular?: "))

    for turno in range(generaciones):
        print(f"\nGeneración {turno}:")
        imprimir_posiciones(matriz)
        aplicar_milagros(matriz)
        matriz = siguiente_generacion(matriz)

        if not np.any(matriz == 1):
            print("☠️  Todas las células murieron. Fin de la simulación.")
            break

    guardar_salida(matriz)

if __name__ == "__main__":
    menu()
