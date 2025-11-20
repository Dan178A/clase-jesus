
import random
import os

CEL_VIVA = "O"
CEL_ANGEL = "A"
CEL_MUERTA = "."

# ------------------ CARGA Y GUARDADO DE ARCHIVOS ------------------ #

def leer_archivo_entrada(nombre_archivo="acaentra.txt"):
    if not os.path.exists(nombre_archivo):
        print("Archivo de entrada no encontrado.")
        return None, None, []

    with open(nombre_archivo, "r") as file:
        lineas = file.readlines()
        n, m = map(int, lineas[0].strip().split(","))
        tablero = [[CEL_MUERTA for _ in range(m)] for _ in range(n)]

        for linea in lineas[1:]:
            i, j = map(int, linea.strip().split(","))
            tablero[i][j] = CEL_VIVA
    return n, m, tablero

def guardar_archivo_salida(tablero, nombre_archivo="acasali.txt"):
    with open(nombre_archivo, "w") as file:
        for i in range(len(tablero)):
            for j in range(len(tablero[0])):
                if tablero[i][j] in (CEL_VIVA, CEL_ANGEL):
                    file.write(f"{i},{j}\n")

# ------------------ UTILIDADES ------------------ #

def mostrar_tablero(tablero):
    print("\n".join("".join(f"{celda:2}" for celda in fila) for fila in tablero))

def contar_vecinos(tablero, x, y):
    vivos = 0
    n, m = len(tablero), len(tablero[0])
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and tablero[nx][ny] in (CEL_VIVA, CEL_ANGEL):
                vivos += 1
    return vivos

def crear_tablero_aleatorio(n, m, cantidad=None):
    total_celdas = n * m
    if cantidad is None:
        cantidad = random.randint(n, total_celdas)
    elif cantidad < n or cantidad > total_celdas:
        raise ValueError("Cantidad fuera del rango permitido")

    tablero = [[CEL_MUERTA for _ in range(m)] for _ in range(n)]
    posiciones = [(i, j) for i in range(n) for j in range(m)]
    random.shuffle(posiciones)

    for i, j in posiciones[:cantidad]:
        tablero[i][j] = CEL_VIVA

    return tablero

# ------------------ REGLAS DE VIDA ------------------ #

def evolucionar(tablero):
    n, m = len(tablero), len(tablero[0])
    nuevo = [[CEL_MUERTA for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            vecinos = contar_vecinos(tablero, i, j)
            if tablero[i][j] in (CEL_VIVA, CEL_ANGEL):
                if vecinos <= 1 or vecinos >= 4:
                    nuevo[i][j] = CEL_MUERTA
                else:
                    nuevo[i][j] = CEL_VIVA
            else:
                if vecinos == 3:
                    nuevo[i][j] = CEL_VIVA
    return nuevo

# ------------------ MILAGROS ------------------ #

def ejecutar_milagro_1(tablero):
    n, m = len(tablero), len(tablero[0])
    recorrido = [(i, j) for i in range(n) for j in range(m)]
    coordenadas_impares = [(x, y) for (x, y) in recorrido if x % 2 == 1 and y % 2 == 1]
    libres = [coord for coord in coordenadas_impares if tablero[coord[0]][coord[1]] == CEL_MUERTA]

    if len(libres) >= len(coordenadas_impares) // 2:
        i, j = libres[0]
        tablero[i][j] = CEL_ANGEL
        print("Milagro 1 ejecutado.")

def ejecutar_milagro_2(tablero):
    n, m = len(tablero), len(tablero[0])
    recorrido = [(i, m - 1 - i) for i in range(n) if 0 <= m - 1 - i < m]
    coordenadas_xpar = [(x, y) for (x, y) in recorrido if x % 2 == 0]
    libres = [coord for coord in coordenadas_xpar if tablero[coord[0]][coord[1]] == CEL_MUERTA]

    if len(libres) >= len(coordenadas_xpar) * 7 // 10:
        i, j = libres[-1]
        tablero[i][j] = CEL_ANGEL
        print("Milagro 2 ejecutado.")

def ejecutar_milagro_3(tablero):
    n, m = len(tablero), len(tablero[0])
    recorrido = [(i, j) for j in range(m) for i in range(n)]
    mitad = len(recorrido) // 2
    segunda_mitad = recorrido[mitad:]
    coordenadas_yimpar = [(x, y) for (x, y) in segunda_mitad if y % 2 == 1]
    libres = [coord for coord in coordenadas_yimpar if tablero[coord[0]][coord[1]] == CEL_MUERTA]

    if len(libres) >= len(coordenadas_yimpar) * 6 // 10:
        i, j = libres[0]
        tablero[i][j] = CEL_ANGEL
        print("Milagro 3 ejecutado.")

# ------------------ SIMULADOR ------------------ #

def simular_generaciones(tablero, generaciones):
    for gen in range(1, generaciones + 1):
        print(f"\nGeneración {gen}:")
        mostrar_tablero(tablero)
        if all(celda == CEL_MUERTA for fila in tablero for celda in fila):
            print("Todas las células han muerto.")
            return tablero
        tablero = evolucionar(tablero)
    return tablero

# ------------------ MENÚ PRINCIPAL ------------------ #

def menu_principal():
    tablero = []
    n = m = 0

    while True:
        print("\n--- Menú ACA ---")
        print("1. Cargar caldo inicial desde archivo")
        print("2. Generar caldo inicial aleatorio")
        print("3. Agregar célula")
        print("4. Eliminar célula")
        print("5. Mostrar caldo actual")
        print("6. Simular N generaciones")
        print("7. Ejecutar Milagro")
        print("8. Guardar caldo final")
        print("9. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            n, m, tablero = leer_archivo_entrada()
        elif opcion == "2":
            n = int(input("Filas: "))
            m = int(input("Columnas: "))
            cantidad = input("Cantidad de células vivas (ENTER para aleatorio): ")
            cantidad = int(cantidad) if cantidad else None
            tablero = crear_tablero_aleatorio(n, m, cantidad)
        elif opcion == "3":
            i, j = map(int, input("Coordenadas i,j: ").split(","))
            tablero[i][j] = CEL_VIVA
        elif opcion == "4":
            i, j = map(int, input("Coordenadas i,j: ").split(","))
            tablero[i][j] = CEL_MUERTA
        elif opcion == "5":
            mostrar_tablero(tablero)
        elif opcion == "6":
            generaciones = int(input("¿Cuántas generaciones? "))
            tablero = simular_generaciones(tablero, generaciones)
        elif opcion == "7":
            milagro = input("Milagro (1, 2 o 3): ")
            if milagro == "1":
                ejecutar_milagro_1(tablero)
            elif milagro == "2":
                ejecutar_milagro_2(tablero)
            elif milagro == "3":
                ejecutar_milagro_3(tablero)
        elif opcion == "8":
            guardar_archivo_salida(tablero)
            print("Guardado en acasali.txt.")
        elif opcion == "9":
            break
        else:
            print("Opción no válida.")

# ------------------ EJECUCIÓN ------------------ #

if __name__ == "__main__":
    menu_principal()
