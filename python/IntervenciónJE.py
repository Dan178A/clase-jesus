import numpy as np
import random
def generar(a,b,X):
    for a in range (0,4,1):
        for b in range (0,4,1):
            num=random.randint(0,2)
            if num==0:
                X[a,b] = "A"
            elif num==1:
                X[a,b] = "Z"
            else:
                X[a,b] = "R"
    return(X)


def conteo(pos,Y):
    cantidad = 0
    for c in range (0,4,1):
        for d in range (0,4,1):
            if Y[c,d]==pos:
                cantidad += 1
    return cantidad


def main():
    CP1 = np.array([["  "]*4,["  "]*4,["  "]*4,["  "]*4])
    CP2 = np.array([["  "]*4,["  "]*4,["  "]*4,["  "]*4])
    CS2 = np.array([["  "]*4,["  "]*4,["  "]*4,["  "]*4])
    i:int
    j:int
    i = 0
    j = 0
    A = 'A'
    Z = 'Z'
    R = 'R'
    N = 'N'
    V = 'V'
    M = 'M'
    generar(i,j,CP1)
    generar(i,j,CP2)
    for i in range (0,4,1):
        for j in range (0,4,1):
            if CP1[i,j]=='A' and CP2[i,j]=='A':
                CS2[i,j]='A'
            elif CP1[i,j]=='Z' and CP2[i,j]=='Z':
                CS2[i,j]='Z'
            elif CP1[i,j]=='R' and CP2[i,j]=='R':
                CS2[i,j]='R'
            elif (CP1[i,j]=='A' and CP2[i,j]=='Z') or (CP1[i,j]=='Z' and CP2[i,j]=='A'):
                CS2[i,j]='V'
            elif (CP1[i,j]=='A' and CP2[i,j]=='R') or (CP1[i,j]=='R' and CP2[i,j]=='A'):
                CS2[i,j]='N'
            elif (CP1[i,j]=='Z' and CP2[i,j]=='R') or (CP1[i,j]=='R' and CP2[i,j]=='Z'):
                CS2[i,j]='M'
    Primarios = conteo(A,CS2)+conteo(Z,CS2)+conteo(R,CS2)
    N2 = conteo(N,CS2)
    V2 = conteo(V,CS2)
    M2 = conteo(M,CS2)
    Sec = (N2+V2+M2)
    Mayor = 0
    if max(N2,V2,M2)==N2:
        Mayor='el naranja'
    elif max(N2,V2,M2)==V2:
        Mayor='el verde'
    else:
        Mayor='el morado'
    print("La matriz de colores primarios 1 es...")
    print(CP1)
    print("La matriz de colores primarios 2 es...")
    print(CP2)
    print("Matriz de colores secundarios:")
    print(CS2)
    print("Cantidad de naranjas:", N2)
    print("Cantidad de verdes:", V2)
    print("Cantidad de morados:", M2)
    print("Cantidad de colores primarios:", Primarios)
    print("Cantidad de colores secundarios", Sec)
    print("Color secundario más repetido:", Mayor)
    print("Leyenda:")
    print("    A: Amarillo")
    print("    Z: Azul")
    print("    C: Rojo")
    print("    V: Verde")
    print("    N: Naranja")
    print("    M: Morado")
main()