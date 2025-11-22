-----

# 📘 Guía de Clase: Dominando los Grafos en C++

**Unidad V: Estructuras Dinámicas Jerárquicas**
**Enfoque:** Visualización → Estructura → Algoritmo

-----

## 1\. ¿Qué es realmente un Grafo? (Tema 1)

Hasta ahora hemos trabajado con **Árboles**. En un árbol existe una jerarquía estricta: un nodo raíz y nodos hijos. Un **Grafo** rompe esa regla; es una estructura no lineal que representa relaciones libres entre objetos.

  * **Nodos (Vértices):** Los puntos que contienen la información (Ej: Ciudades, Personas).
  * **Aristas:** Las líneas que unen a los nodos (Ej: Carreteras, Amistad).

**Diferencia Visual Clave:**

  * **Árbol:** Solo hay un camino único entre la raíz y un nodo. No existen ciclos.
  * **Grafo:** Pueden existir múltiples caminos entre dos nodos y se permiten ciclos (salir de un nodo y regresar al mismo).

![Image of graph data structure vs tree diagram](binary_graphas.jfif)

### 🚦 Tipos de Conexiones

1.  **No Dirigido:** La relación es bidireccional. Si A conecta con B, B conecta con A (Ej: `A — B`).
2.  **Dirigido (Dígrafo):** La relación tiene un sentido específico. A apunta a B, pero B no necesariamente apunta a A (Ej: `A → B`).

-----

## 2\. Representación en C++ (Tema 2)

Para almacenar un grafo en la memoria, existen dos métodos principales. Nos enfocaremos en el más eficiente para grafos dinámicos: las **Listas de Adyacencia**.

### Opción A: La Matriz de Adyacencia (Estática)

Se utiliza una matriz cuadrada `N x N`.

  * `1`: Existe conexión.
  * `0`: No existe conexión.

### Opción B: Lista de Adyacencia (Dinámica) ⭐ *Recomendada*

Es la opción más eficiente en memoria. Se utiliza un **Arreglo de Punteros**, donde cada posición del arreglo almacena la "cabeza" de una **Lista Enlazada** con sus vecinos.

**Estructura del Nodo (El Vecino):**

```cpp
struct Nodo {
    int destino;       // A qué nodo apunta la arista
    Nodo* siguiente;   // Puntero al siguiente vecino en la lista
};
```

**Construcción del Grafo (Arreglo de Listas):**

```cpp
// Función para crear un nuevo nodo de lista
Nodo* crearNodo(int v) {
    Nodo* nuevo = new Nodo;
    nuevo->destino = v;
    nuevo->siguiente = NULL;
    return nuevo;
}

int main() {
    int numNodos = 5;
    // Un arreglo donde cada posición es una CABEZA de lista
    Nodo* grafo[5]; 

    // Inicializar todo en NULL (Limpieza de memoria)
    for(int i=0; i<numNodos; i++) {
        grafo[i] = NULL; 
    }

    // EJEMPLO: Conectar Nodo 0 con Nodo 1 (0 -> 1)
    Nodo* nuevoVecino = crearNodo(1);
    
    // Insertar al inicio de la lista del nodo 0
    nuevoVecino->siguiente = grafo[0];
    grafo[0] = nuevoVecino;
}
```

-----

## 3\. Recorridos de Grafos (Tema 3)

Existen dos algoritmos fundamentales para recorrer o buscar elementos en un grafo. La diferencia radica en el orden en que se visitan los vecinos.

### A. BFS (Breadth First Search) - Búsqueda en Anchura

Este algoritmo explora el grafo por **niveles** o capas. Imagina una onda de agua expandiéndose: primero visitas a todos tus vecinos directos (distancia 1), luego a los vecinos de tus vecinos (distancia 2), y así sucesivamente.

  * **Estructura Auxiliar:** Utiliza una **COLA (Queue)**.
  * **Lógica:** FIFO (First In, First Out). El primero que descubro es el primero que visito.

**Pasos Lógicos:**

1.  Entrar al nodo inicial.
2.  Meter todos sus vecinos a la cola.
3.  Sacar el primer elemento de la cola y repetir el proceso.

### B. DFS (Depth First Search) - Búsqueda en Profundidad

Este algoritmo explora el grafo yendo tan lejos como sea posible por una sola rama antes de retroceder. Es similar a resolver un laberinto: avanzas hasta chocar con pared, y luego retrocedes (*backtracking*) para probar otro camino.

  * **Estructura Auxiliar:** Utiliza una **PILA (Stack)** o **Recursividad**.
  * **Lógica:** LIFO (Last In, First Out).

**Código C++ (Implementación Recursiva):**

```cpp
// Arreglo global para evitar ciclos infinitos
bool visitado[5]; 

void DFS(int nodoActual, Nodo* grafo[]) {
    // 1. Marcar como visitado e imprimir (Procesar)
    visitado[nodoActual] = true;
    cout << nodoActual << " ";

    // 2. Recorrer la lista de vecinos de este nodo
    Nodo* temp = grafo[nodoActual];
    while(temp != NULL) {
        int vecino = temp->destino;
        
        // 3. Si el vecino NO ha sido visitado, profundizar (Recursión)
        if (!visitado[vecino]) {
            DFS(vecino, grafo);
        }
        temp = temp->siguiente;
    }
}
```

-----

## ⚠️ Errores Comunes al Implementar

1.  **Ciclos Infinitos:** En los grafos (a diferencia de los árboles) es posible regresar al nodo de inicio (A-\>B-\>A). Si no se utiliza un arreglo de `visitados[]`, el algoritmo `DFS` o `BFS` entrará en un bucle infinito y el programa se congelará.
2.  **Punteros no Inicializados:** Al declarar el arreglo `Nodo* grafo[N]`, este contiene basura de memoria. Es obligatorio hacer un bucle `for` inicial para poner todas las posiciones en `NULL`.
3.  **Perder la Referencia:** Al recorrer la lista de adyacencia, nunca se debe mover el puntero principal del arreglo (`grafo[i]`). Siempre se debe usar un puntero auxiliar (`Nodo* temp = grafo[i]`) para iterar.

-----

## 🛠️ Ejercicio Práctico Recomendado

Para consolidar el conocimiento, se sugiere realizar la siguiente práctica en el compilador:

1.  Copiar la estructura `Nodo` y el `main` de la **Lista de Adyacencia**.
2.  Crear un grafo de **4 nodos** (0, 1, 2, 3).
3.  Realizar las siguientes conexiones manualmente:
      * 0 → 1
      * 0 → 2
      * 1 → 2
      * 2 → 0 (Ciclo)
      * 2 → 3
4.  Ejecutar el algoritmo **DFS** iniciando desde el nodo 0 y verificar que se impriman todos los nodos sin caer en un bucle infinito.