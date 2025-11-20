# listas y matrices en Python
import random
# Lista de aspectos a calificar en una encuesta
aspectos = ["Atención", "Comida", "Precio", "Ambiente"]

# Creamos una matriz de 5 filas (clientes) y 4 columnas (aspectos), inicializada en ceros
calificaciones = [[0]*4 for _ in range(5)]

# Ingreso de notas por cada cliente y cada aspecto
for cliente in range(len(calificaciones)):
    for aspecto in range(len(aspectos)):
        # Pedimos al usuario que ingrese la calificación para cada aspecto
        nota = int(random.random() * 10)
        calificaciones[cliente][aspecto] = nota

print("Calificaciones de los clientes:")

# Calculamos el promedio de cada aspecto
promedios = []
for aspecto in range(len(aspectos)):
    suma = 0
    for cliente in range(5):
        suma += calificaciones[cliente][aspecto]
    promedio = suma / 5
    # Guardamos el nombre del aspecto y su promedio en una tupla
    promedios.append((aspectos[aspecto], promedio))

promedios.sort(key=lambda x: x[1], reverse=True)
print(promedios)


# matriz de letras y conteo de vocales por columna

matriz = [
    ['A', 'E', 'I'],
    ['O', 'U', 'E'],
    ['I', 'A', 'O'],
    ['E', 'O', 'I']
]

conteo = {"A": 0, "E": 0, "I": 0, "O": 0, "U": 0}
for col in range(3):
    # Diccionario para contar cuantas veces aparece cada vocal
    for fila in range(len(matriz)):
        letra = matriz[fila][col]
        if letra in conteo:
            conteo[letra] += 1
    # Encontrar la vocal mas repetida en la columna
    mas_repetida = max(conteo, key=conteo.get)
    print(f"Columna {col}: vocal mas repetida = {mas_repetida}")

tablero = [
    [0, 1, 0],
    [1, 1, 0],
    [0, 0, 1]
]
x = 1
y = 0
tablero[x][y]

def contar_vecinos(tablero, x: int, y: int):
    """
    Cuenta cuántas células vivas (valor 1) hay alrededor de la celda (x, y)
    en una matriz (tablero) que representa un autómata celular.
    """
    # Lista de desplazamientos para las 8 posiciones vecinas
    direcciones = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                   (0, 1), (1, -1), (1, 0), (1, 1)]
    vivos = 0

    for dx, dy in direcciones:
        mov_x = x+dx
        mov_y = y+dy
        if 0 <= mov_x < len(tablero) and 0 <= mov_y < len(tablero[0]):
            vivos += tablero[mov_x][mov_y]
    return vivos

print(contar_vecinos(tablero=tablero, x=1, y=1))
