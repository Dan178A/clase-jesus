import numpy as np


def generar_matrices_user(filas, columnas):
    matriz = []
    for _ in range(0, filas, 1):
        fila = []
        for i in range(0, columnas, 1):
            valor = np.random.randint(0, 2)
            fila.append(valor)
        matriz.append(fila)

    return matriz


def recorrido_zigzag_horizontal(matriz):

    recorrido = []
    for i in range(len(matriz)):
        if i % 2 == 0:
            for j in range(len(matriz[0])):
                recorrido.append((i, j))
        else:
            for j in range(len(matriz[0])):
                recorrido.append((i, j))
    return recorrido


def recorrido_zigzag_vertical(matriz) -> tuple[int, int]:

    recorrido = []
    for j in range(len(matriz)):
        if j % 2 == 0:
            # Recorre de arriba a abajo
            for i in range(len(matriz[0])):
                recorrido.append((i, j))
        else:
            # Recorre de abajo a arriba
            for i in range(len(matriz[0])):
                recorrido.append((i, j))
    return recorrido


def contar_vivos_muertos(matriz):

    vivos = 0
    muertos = 0
    for fila in matriz:
        for celda in fila:
            if celda == 1:
                vivos += 1
            else:
                muertos += 1
    return vivos, muertos


def contar_v2(matriz):
    vidas = 0
    for i in range(min(len(matriz), len(matriz[0]))):
        if matriz[i][i] == 1:
            vidas += 1
    return vidas


def milagro_1(matriz):
    filas, columnas = matriz.shape
    recorrido = []
    top = 0
    botton = filas - 1
    left = 0
    rigth = columnas - 1
    # pasos
    # 1 top
    # 2 right
    # 3 bottom
    # 4 left
    while top <= botton and left <= rigth:
        for j in range(left,rigth + 1):
            recorrido.append((top,j))
        top += 1
        for i in range(top,botton + 1):
            recorrido.append((i,rigth))
        rigth -= 1
        if top <= botton:
            for j in range(rigth,left - 1,-1):
                recorrido.append((botton,j))
            botton -=1
        if left <= rigth:
            for i in range(botton,top - 1,-1):
                recorrido.append((i,left))
            left +=1
    
    impares = []
    for pos in recorrido:
        i,j = pos
        if i % 2 == 1 and j % 2 == 1:
            impares.append((i,j))

    libres = []
    for pos in impares:
        i,j = pos
        if matriz[i][j] == 0:
            libres.append(pos)
    
    if len(libres) >= (0.5 * len(impares)) and libres:
        i,j = libres
        matriz[i][j] = 1
        print("¡Ha ocurrido el milagro 1! La celda ", [i, j], "está viva.")

def recorrido_diagonales(matriz):
    return


def milagro2(matriz):
    recorrido = recorrido_diagonales(matriz)
    for pos in recorrido:
        candidatos = []
        i, j = pos
        if j % 2 == 0:
            for pos in [i], [j]:
                if pos in candidatos:
                    total += 1
                    i, j = pos
                    matriz[i][j] = 1
            candidatos.append((i, j))
    if len(candidatos) >= int(0.7 * total):
        matriz[i][j] = 1
        print("¡Ha ocurrido el milagro 2! La celda ", [i, j], "está viva.")
    return matriz


def milagro3(matriz):
    """
        Aplica el milagro 3:
        si en el recorrido zigzag vertical al menos el 60% de celdas es 0 con columna
        impar, nace una celula nueva (valor 1) en la primera posicion libre
        de la celda impar del segunda mitad del recorrido
    """

    recorrido = recorrido_zigzag_vertical(matriz)
    candidatos = []
    total_y_impar = 0

    for pos in recorrido:
        i, j = pos
        if j % 2 == 1:
            total_y_impar += 1
            if matriz[i][j] == 0:
                # saber posicones a reemplazar
                candidatos.append((i, j))

    if len(candidatos) >= int(0.6 * total_y_impar):
        segunda_mitad = recorrido[len(recorrido)//2:]
        for pos in segunda_mitad:
            if pos in candidatos:
                i, j = pos
                matriz[i][j] = 1
                print(f"Milagr 3: nacio celula en ({i},{j})")

    return candidatos


if __name__ == "__main__":
    filas = int(input('Ingrese el numero de filas : '))
    columnas = int(input("Ingrese el numero de columnas:"))

    m1 = generar_matrices_user(filas, columnas)
    # print(f"Recorrido zigzag horizontal: {recorrido_zigzag_horizontal(m1)}")
    # vivos, muertos = contar_vivos_muertos(m1)
    # print(f"Vivos: {vivos},Muertos{muertos}")
    milagro3(m1)
