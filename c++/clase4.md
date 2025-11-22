
-----

# 📘 Unidad V: Estructuras Dinámicas Jerárquicas - GRAFOS

Esta unidad cubre los fundamentos teóricos y prácticos de los Grafos, una de las estructuras de datos más versátiles en la programación. A diferencia de los árboles, que tienen una jerarquía estricta, los grafos representan relaciones libres entre objetos.

-----

## 📍 Tema 1: Grafos y sus Aplicaciones

### 1.1 ¿Qué es un Grafo?

Un grafo es una estructura de datos no lineal formada por dos componentes principales:

1.  **Vértices (Nodos):** Los puntos o elementos que contienen la información.
2.  **Aristas (Arcos):** Las líneas que conectan a los vértices entre sí, representando una relación.

Matemáticamente se define como $G = (V, E)$.

#### Diferencia clave con los Árboles:

  * **Árbol:** Existe un nodo raíz, hay jerarquía (padres e hijos), y **no** hay ciclos (caminos cerrados).
  * **Grafo:** No hay raíz única, no hay jerarquía estricta, y **sí** puede haber ciclos (puedes salir de un nodo y regresar a él por otro camino).

### 1.2 Tipos de Grafos

Para modelar problemas reales, usamos diferentes tipos:

  * **Grafo No Dirigido:** La relación es bidireccional (como una amistad en Facebook). Si A es amigo de B, B es amigo de A.
      * *Visual:* Líneas simples. `A — B`
  * **Grafo Dirigido (Dígrafo):** La relación tiene un sentido (como seguir a alguien en Twitter/X). A sigue a B, pero B no necesariamente sigue a A.
      * *Visual:* Flechas. `A → B`
  * **Grafo Ponderado:** Las conexiones tienen un "peso" o costo (distancia, tiempo, precio).
      * *Visual:* Números sobre las líneas. `A --(5km)-- B`

### 1.3 Aplicaciones en la Vida Real

  * **Redes Sociales:** Usuarios (Nodos) y Amistades (Aristas).
  * **Mapas (GPS):** Intersecciones (Nodos) y Calles (Aristas con peso de distancia).
  * **Internet:** Routers (Nodos) y Cables de fibra (Aristas).

-----

## 🏗️ Tema 2: Representación de Grafos

Para que una computadora entienda un grafo, debemos "traducir" el dibujo a estructuras de datos. Existen tres formas principales:

### 2.1 Matriz de Adyacencia

Utilizamos una tabla (arreglo bidimensional de `NxN`) donde las filas y columnas representan los nodos.

  * **1 (o True):** Existe una conexión.
  * **0 (o False):** No existe conexión.
  * *En grafos ponderados, en lugar de 1 se pone el peso.*

**Ejemplo Visual:**
Imagina 3 nodos: A(0), B(1), C(2).

  * A conecta con B.
  * C conecta con A.

| | A (0) | B (1) | C (2) |
|---|---|---|---|
| **A (0)** | 0 | **1** | 0 |
| **B (1)** | 0 | 0 | 0 |
| **C (2)** | **1** | 0 | 0 |

**Código C++ (Estático):**

```cpp
const int V = 5; // Número de vértices
int grafo[V][V]; // Matriz de 5x5 iniciada en 0

// Añadir arista de 0 a 1
grafo[0][1] = 1;
```

  * ✅ **Ventaja:** Es muy rápido saber si dos nodos están conectados `if(grafo[a][b])`.
  * ❌ **Desventaja:** Ocupa mucha memoria ($N^2$). Si tienes 10,000 nodos y pocas aristas, la matriz estará llena de ceros inútiles.

### 2.2 Matriz de Incidencia

Es una matriz donde las filas son **Vértices** y las columnas son **Aristas**.

  * Se marca con 1 si el vértice es parte de esa arista.
  * Es menos común en programación básica, pero útil en circuitos eléctricos.

### 2.3 Listas de Adyacencia (Recomendado para C++ dinámico)

Esta es la forma más eficiente en memoria. Utilizamos un **Arreglo de Listas Enlazadas**.
Cada posición del arreglo representa un nodo, y de él "cuelga" una lista con sus vecinos.

**Ejemplo Visual:**

  * **Nodo A:** `-> [B] -> NULL`
  * **Nodo B:** `-> NULL`
  * **Nodo C:** `-> [A] -> [B] -> NULL`

**Estructura en C++:**
Aquí combinamos arreglos con `structs` dinámicos.

```cpp
// 1. El nodo de la lista (El destino)
struct NodoVecino {
    int destino;           // A qué nodo conecta
    int peso;              // (Opcional) Peso de la arista
    NodoVecino* siguiente; // Puntero al siguiente vecino
};

// 2. La estructura del Grafo
struct Grafo {
    int numVertices;
    NodoVecino* listaAdy[100]; // Arreglo de punteros (cabezas de listas)
};
```

  * ✅ **Ventaja:** Ahorra espacio. Solo guardas las conexiones que existen.
  * ❌ **Desventaja:** Buscar si A conecta con B es un poco más lento (hay que recorrer la lista de A).

-----

## 🏃 Tema 3: Recorridos de Grafos

Al igual que en los árboles teníamos Pre-orden o In-orden, en los grafos tenemos dos formas fundamentales de "caminar" por ellos. Esto es vital para buscar rutas (GPS) o conexiones.

### 3.1 BFS - Búsqueda en Anchura (Breadth-First Search)

Explora el grafo por "niveles" o capas. Primero visita a todos los vecinos directos, luego a los vecinos de los vecinos.

  * **Analogía:** Una onda de agua expandiéndose o un incendio que crece parejo en todas direcciones.
  * **Estructura Auxiliar:** Usa una **COLA (Queue)** (FIFO - Primero en entrar, primero en salir).

**Algoritmo Lógico:**

1.  Entrar al nodo inicial y marcarlo "visitado".
2.  Meterlo en la Cola.
3.  Mientras la Cola no esté vacía:
      * Sacar un nodo.
      * Meter a la cola a todos sus vecinos **no visitados**.

### 3.2 DFS - Búsqueda en Profundidad (Depth-First Search)

Explora el grafo yendo tan lejos como sea posible por una rama antes de retroceder.

  * **Analogía:** Resolver un laberinto. Vas por un camino hasta que chocas con pared, y luego retrocedes (*backtracking*) para probar otro camino.
  * **Estructura Auxiliar:** Usa una **PILA (Stack)** o **Recursividad** (LIFO - Último en entrar, primero en salir).

**Algoritmo Lógico (Recursivo):**

1.  Entrar al nodo inicial y marcarlo "visitado".
2.  Buscar el primer vecino no visitado.
3.  Llamar a la función DFS de nuevo para ese vecino (ir al fondo).
4.  Si no hay vecinos, regresar (la recursión se devuelve sola).

-----

## 📝 Resumen Comparativo

| Característica | Matriz de Adyacencia | Lista de Adyacencia |
| :--- | :--- | :--- |
| **Memoria** | Mucha ($N^2$) | Poca (N + E) |
| **Velocidad de Consulta** | Instantánea O(1) | Lenta (depende de vecinos) |
| **Implementación** | Arreglos bidimensionales | Punteros y Structs |
| **Ideal para** | Grafos densos (muchas conexiones) | Grafos dispersos (pocas conexiones) |

| Algoritmo | Estructura de Datos | Estrategia | Uso Común |
| :--- | :--- | :--- | :--- |
| **BFS** | Cola (Queue) | Capas / Niveles | Ruta más corta (GPS) |
| **DFS** | Pila / Recursión | Profundidad / Backtracking | Laberintos, Rompecabezas |