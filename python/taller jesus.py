import numpy as np
def mostrar_matriz(matriz, titulo):
    print(titulo)
    print()
    for fila in matriz:
        print(' '.join(fila))
    input("Presiona ENTER para continuar")

def Alcantarillas(matriz):
    A = set()
    while len(A) < 3:
        i = np.random.randint(1, 3) 
        j = np.random.randint(0, 5)  
        if (i, j) not in A:
            A.add((i, j))
            matriz[i][j] = 'A'
    return A

def Pasajero(matriz, Alc):
    while True:
        i = np.random.randint(1, 4)
        j = np.random.randint(1, 4)
        if (i, j) not in Alc:
            matriz[i][j] = "P"
            return (i, j)

def recorrido_zigzgag(matriz, alcantarillas, pasajeros):
    metros=0
    for j in range (0,5,1):
        if j % 2==0:
            rango=range(5)
        else:
            rango= range(5,0, -1)
            for i in rango:
                metros+=25
                if (i,j) in alcantarillas:
                    matriz[i][j]="X"
                    return False, metros
                if (i,j) == pasajeros:
                    matriz[i][j]="!"
                    return True, metros
    return False, metros

def maquillaje(matriz):
    for i in range (0,len(matriz),1):
        for j in range (0,len(matriz),1):
            if matriz[i][j]=="C":
                matriz[i][j]="🛣️"
            if matriz[i][j]=="A":
                matriz[i][j]="🕳️"
            if matriz[i][j]=="P":
                matriz[i][j]="👤"
            if matriz[i][j]=="T":    
                matriz[i][j]="🚉"
            if matriz[i][j]=="!":
                matriz[i][j]="🚕"
            if matriz[i][j]=="X":
                matriz[i][j]="💥"
    return matriz

def main():
    M=np.full((6,6), "C")
    M[0,0]="T"
    M1=np.full((6,6), "C")
    M[0,0]="T"
    O="He aquí la matriz"
    mostrar_matriz(M,O)
    maquillaje(M1)
    mostrar_matriz(M1,O)
    A = Alcantarillas(M)
    Z = Alcantarillas(M1)
    mostrar_matriz(M,O)
    maquillaje(M1)
    mostrar_matriz(M1,O)
    P = Pasajero(M, A)
    Q = Pasajero(M1,Z)
    mostrar_matriz(M,O)
    maquillaje(M1)
    mostrar_matriz(M1,O)
    exito, metros = recorrido_zigzgag(M, A, P)
    exito1, metros= recorrido_zigzgag(M1, Z, Q)
    if exito and exito1:
        titulo = "¡Carrera Exitosa!"
        mostrar_matriz(M,O)
        maquillaje(M1)
        mostrar_matriz(M1,O)

    else:
        titulo = "¡Carrera Fallida!"
        maquillaje(M1)
        mostrar_matriz(M, titulo + f"\nMetros recorridos: {metros} mts")
        mostrar_matriz(M1,O)
main()