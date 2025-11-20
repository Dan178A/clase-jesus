"""
ACA_demo.py

Simulación básica del autómata celular "ALIVE".
Este script implementa un autómata celular simple que simula la evolución de un
caldo de cultivo de células vivas. El tablero se representa como una lista de listas,
donde cada celda puede estar viva (1) o muerta (0). El autómata sigue las reglas de
la vida de Conway, donde las células nacen, mueren o sobreviven en función de
el número de vecinos vivos.

"""

import random

# =========================
# FUNCIONES DEL AUTÓMATA
# =========================

def mostrar(tablero):
    """Imprime el tablero en pantalla."""
    for fila in tablero:
        fila_str = ''
        for c in fila:
            fila_str += str(c) + ' '
        print(fila_str.strip())
    print()

def contar_vecinos(tablero, x, y):
    """Cuenta las células vivas alrededor de la celda (x, y)."""
    vecinos = 0
    dx = [-1, -1, -1, 0, 0, 1, 1, 1]
    dy = [-1, 0, 1, -1, 1, -1, 0, 1]
    for k in range(8):
        nx = x + dx[k]
        ny = y + dy[k]
        if 0 <= nx < len(tablero) and 0 <= ny < len(tablero[0]):
            vecinos += tablero[nx][ny]
    return vecinos

def siguiente_generacion(tablero):
    """Calcula la siguiente generación del caldo de cultivo."""
    filas = len(tablero)
    columnas = len(tablero[0])
    nueva = []
    for i in range(filas):
        nueva_fila = []
        for j in range(columnas):
            vecinos = contar_vecinos(tablero, i, j)
            if tablero[i][j] == 1:
                if vecinos == 2 or vecinos == 3:
                    nueva_fila.append(1)  # sobrevive
                else:
                    nueva_fila.append(0)  # muere
            else:
                if vecinos == 3:
                    nueva_fila.append(1)  # nace nueva célula
                else:
                    nueva_fila.append(0)  # permanece vacía
        nueva.append(nueva_fila)
    return nueva

def generar_tablero(filas, columnas, num_celulas):
    """Crea un tablero con células vivas aleatorias."""
    tablero = []
    for _ in range(filas):
        fila = []
        for _ in range(columnas):
            fila.append(0)
        tablero.append(fila)

    posiciones = []
    for i in range(filas):
        for j in range(columnas):
            posiciones.append((i, j))

    random.shuffle(posiciones)

    for i in range(min(num_celulas, filas * columnas)):
        x, y = posiciones[i]
        tablero[x][y] = 1

    return tablero

# =========================
# EJECUCIÓN PRINCIPAL
# =========================

if __name__ == "__main__":
    filas = 6
    columnas = 6
    vivas_iniciales = 10
    generaciones = 5

    tablero = generar_tablero(filas, columnas, vivas_iniciales)

    for turno in range(generaciones):
        print(f"Generación {turno}:")
        mostrar(tablero)
        tablero = siguiente_generacion(tablero)




# =========================
# EJERCICIO DE LÓGICA EXTRA
# =========================

# Similar a la lógica de transformación

datos = ['10C', '20F', '-5C', '100F', '37C', '75F', '0C', '212F']
# Regla: si termina en 'C', convertir a Fahrenheit: F = C * 9/5 + 32
#        si termina en 'F', convertir a Celsius:    C = (F - 32) * 5/9

transformados = []
for d in datos:
    valor = int(d[:-1])
    unidad = d[-1]
    if unidad == 'C':
        f = valor * 9 / 5 + 32
        f_redondeado = round(f, 2)
        transformados.append(f_redondeado)
    elif unidad == 'F':
        c = (valor - 32) * 5 / 9
        c_redondeado = round(c, 2)
        transformados.append(c_redondeado)

print("Valores transformados:", transformados)