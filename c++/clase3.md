-----

# 📘 Guía de Estudio Visual: Montículos, Merkle y Grafos

-----

## 🧠 Introducción

necesito que visualices estas tres estructuras.

1.  **Montículos (Heaps):** Ordenamiento militar estricto.
2.  **Merkle:** Árboles para verificar seguridad (Cripto).
3.  **Grafos:** Redes libres (sin jefes).

-----

## 🌳 PARTE 1: Árboles Montículo (Heaps) y Heapsort

*(Semana 2: Árboles Avanzados y Montículos [cite: 14])*

### 1\. ¿Qué es un Montículo (Heap)?

Olvida la libertad de los árboles normales. Un **Montículo Binario** es un árbol estricto que cumple dos reglas sagradas:

1.  **La Regla del Orden:**
      * **Max-Heap:** El Padre es **MAYOR** que los hijos. (El jefe siempre es el más fuerte).
      * **Min-Heap:** El Padre es **MENOR** que los hijos.
2.  **La Regla de la Forma:** El árbol se llena de arriba a abajo y de izquierda a derecha. **No pueden quedar huecos**.

**👀 Visualización (Max-Heap):**
El 100 es el jefe. 90 y 80 son sus tenientes. Nadie abajo es mayor que los de arriba.

```text
       [100]  <-- Raíz (MÁXIMO)
      /     \
    [90]    [80]
    /  \    /
  [40][50][10]
```

### 2\. ¿Cómo se programa? (El Truco del Vector)

Aunque se dibuja como árbol, **en C++ se usa un Arreglo (Vector)**. Es más rápido y no necesitas punteros complejos.

  * Si el padre está en la posición `i`:
      * Hijo Izquierdo = `(2 * i) + 1`
      * Hijo Derecho = `(2 * i) + 2`

### 3\. Algoritmo Heapsort

Es una estrategia para ordenar datos[cite: 14].

1.  Conviertes tu lista en un **Max-Heap** (el mayor sube a la raíz).
2.  Sacas la raíz y la mandas al final (ya está ordenada).
3.  Reparas el árbol (el siguiente más fuerte sube).
4.  Repites.

-----

## 🔒 PARTE 2: Caso de Estudio - Árbol de Merkle

*(Semana 2: Árbol de Merkle y relación con el hashing [cite: 14])*

### 1\. ¿Qué es?

Es un "Árbol Detective". No guarda datos en las ramas, guarda **Hash** (huellas digitales). Es la base de las criptomonedas.

### 2\. ¿Cómo funciona?

Si modificas un solo dato abajo (una hoja), su huella cambia. Eso cambia la huella del padre, y así hasta la raíz. Si la raíz cambia, sabemos que el archivo es falso o fue modificado.

**👀 Visualización:**

```text
           [HASH RAÍZ]  <-- Firma maestra
           /         \
     [Hash AB]     [Hash CD]
      /     \       /     \
  [Hash A][Hash B][Hash C][Hash D]  <-- Hojas (Huellas de los datos)
     |       |       |       |
   [Dato]  [Dato]  [Dato]  [Dato]
```

-----

## 🌐 PARTE 3: Grafos - La Red

*(Semana 3: Grafos, recorridos y algoritmos [cite: 16, 17])*

### 1\. Diferencia con los Árboles

En los árboles hay jerarquía (Padre-Hijo). En los grafos **NO**.
Es un conjunto de **Nodos (Vértices)** conectados por **Aristas (Líneas)**.

  * Puede haber ciclos (puedes dar vueltas en círculo).
  * Todos pueden conectarse con todos.

### 2\. Tipos Clave

  * **Dirigido:** Las líneas son flechas (calle de un solo sentido). A → B.
  * **No Dirigido:** Las líneas son simples (doble sentido). A — B.
  * **Ponderado:** La línea tiene un valor (distancia, precio, peso).

-----

## 📝 PARTE 4: Representación de Grafos (C++)

*(Semana 3: Matriz de adyacencia, lista de adyacencia [cite: 18])*

Para programar un grafo, tienes dos opciones principales. Como te gustan las listas, la segunda será tu favorita.

### A. Matriz de Adyacencia (La Tabla)

Una tabla de `N x N`.

  * `1` = Hay conexión.
  * `0` = No hay conexión.

| | A | B | C |
|---|---|---|---|
| **A** | 0 | 1 | 0 |
| **B** | 0 | 0 | 1 |
| **C** | 1 | 0 | 0 |

  * *Uso:* Rápido para consultar, pero gasta mucha memoria si hay pocos caminos.

### B. Lista de Adyacencia (Tu favorita)

Un arreglo donde cada posición guarda una **Lista Enlazada** de vecinos.

  * Ideal para ahorrar espacio y recorrer caminos.

**Estructura Visual:**

```text
[A] -> [B] -> NULL       (A conecta con B)
[B] -> [C] -> NULL       (B conecta con C)
[C] -> [A] -> [B] -> NULL (C conecta con A y B)
```

-----

## 🚀 Tarea Práctica (Pre-Clase)

haz esto para "soltar la mano":

1.  **Dibuja un Max-Heap** insertando estos números en orden: `50, 30, 20, 15, 10, 8`. (Recuerda: ¡sin huecos\!).
2.  **Simula un cambio en Merkle:** Dibuja un árbol pequeño. Cambia un dato en una hoja y traza con rojo qué nodos de arriba cambiarían su hash.
3.  **El Reto del Grafo:**
      * Dibuja 5 nodos (ciudades).
      * Conéctalos como quieras (con flechas).
      * **Escribe su Lista de Adyacencia** al lado.

-----
