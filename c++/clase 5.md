-----

# 📘 Clase Avanzada: Algoritmos de Caminos Mínimos (GPS)

**Tema:** Dijkstra y Roy-Warshall
**Objetivo:** Entender cómo Google Maps encuentra la ruta más rápida.

-----

## 1\. Introducción: El Problema del GPS

 imagina que tienes un mapa de ciudades conectadas por carreteras. Pero ahora, las líneas no son solo conexiones; tienen un **PESO** (Kilómetros, minutos de tráfico, costo de peaje).

Hasta ahora, BFS nos decía cuál camino tenía *menos paradas*. Pero el camino con menos paradas no siempre es el más rápido (puede haber un tramo larguísimo).

  * **El Reto:** Queremos ir del Punto A al Punto B "gastando" lo menos posible.

-----

## 🏎️ Parte 1: Algoritmo de Dijkstra (El "Waze")

### 🧠 El Concepto

Dijkstra sirve para encontrar la ruta más corta desde **UN origen específico** hacia **TODOS los demás destinos**.

**La Lógica del "Codicioso" (Greedy):**

1.  Estoy en mi ciudad actual.
2.  Miro a todos mis vecinos directos.
3.  Elijo el camino más "barato" acumulado hasta ahora.
4.  **Relajación (Relaxation):** Si encuentro un atajo a través de un vecino que mejora el tiempo que ya conocía para llegar a un destino, **actualizo mi tabla de tiempos**.

[Image of Dijkstra algorithm visualization graph]

### 📝 La Tabla de Distancias (Visualización Mental)

Imagina que queremos ir de la ciudad `A` a todas las demás. Iniciamos una tabla así:

| Ciudad | Distancia desde A | ¿Ya la visité definitvamente? |
| :--- | :--- | :--- |
| **A (Inicio)** | **0** | No |
| **B** | **Infinito** (∞) | No |
| **C** | **Infinito** (∞) | No |

*Cada vez que exploramos, borramos el "Infinito" y ponemos el número real. Si luego encontramos un número menor, borramos el viejo y ponemos el nuevo.*

### 💻 El Código (C++)

Para esto usamos una **Cola de Prioridad** (una lista que siempre pone al menor arriba automáticamente).

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <climits> // Para usar INT_MAX (Infinito)

using namespace std;

const int INF = INT_MAX; // Representamos infinito

struct Arista {
    int destino;
    int peso;
};

// Algoritmo de Dijkstra
void Dijkstra(int inicio, int numNodos, vector<vector<Arista>>& grafo) {
    // 1. Tabla de distancias: Todos inician en Infinito menos el origen
    vector<int> distancia(numNodos, INF);
    distancia[inicio] = 0;

    // 2. La Cola de Prioridad (Guarda pares: <PesoAcumulado, Nodo>)
    // Nota técnica: priority_queue ordena de mayor a menor por defecto, 
    // así que usamos "greater" para que ordene de menor a mayor.
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> cola;
    
    // Metemos el origen a la cola
    cola.push({0, inicio});

    while (!cola.empty()) {
        // Sacamos el nodo con la MENOR distancia acumulada
        int distActual = cola.top().first;
        int u = cola.top().second;
        cola.pop();

        // Si la distancia que sacamos es mayor a la que ya conocemos, la ignoramos
        if (distActual > distancia[u]) continue;

        // 3. RELAJACIÓN: Miramos a los vecinos
        for (auto& arista : grafo[u]) {
            int v = arista.destino;
            int pesoCamino = arista.peso;

            // ¿Es más rápido ir por 'u' hacia 'v' que lo que ya sabíamos?
            if (distancia[u] + pesoCamino < distancia[v]) {
                distancia[v] = distancia[u] + pesoCamino; // Actualizamos
                cola.push({distancia[v], v}); // Metemos a la cola para seguir explorando
            }
        }
    }

    // Imprimir resultados
    cout << "Distancias desde el nodo " << inicio << ":\n";
    for (int i = 0; i < numNodos; i++) {
        cout << "A nodo " << i << " -> " << (distancia[i] == INF ? "Inalcanzable" : to_string(distancia[i])) << endl;
    }
}
```

-----

## 🌐 Parte 2: Algoritmo Roy-Warshall (Floyd-Warshall)

### 🧠 El Concepto

Este algoritmo es más "bruto" pero muy poderoso. No busca la ruta desde UN origen, busca la ruta más corta entre **TODOS contra TODOS** al mismo tiempo.

Se basa en una pregunta simple:

> *"¿Puedo llegar más rápido de la ciudad A a la ciudad B si paso por una ciudad intermedia K?"*

### 📝 La Matriz Mágica

Aquí usamos una **Matriz de Adyacencia** (Tabla `NxN`).

1.  Llenamos la tabla con los pesos directos. (Si no hay conexión directa, ponemos Infinito).
2.  Probamos usar cada ciudad como "puente" intermedio.

**Fórmula clave:**
`Distancia[i][j] = min(Distancia[i][j], Distancia[i][k] + Distancia[k][j])`

  * `i` = Origen
  * `j` = Destino
  * `k` = Ciudad Puente (Intermedia)

### 💻 El Código (C++)

Este es más fácil de escribir (3 bucles), pero cuidado: **¡El orden de los bucles importa\!** El bucle `k` (el puente) debe ir **afuera**.

```cpp
#include <iostream>
#include <vector>
#define INF 99999 // Un número muy grande

using namespace std;

void RoyWarshall(int grafo[4][4], int numNodos) {
    int dist[4][4];

    // 1. Copiamos el grafo original a nuestra matriz de distancias
    for (int i = 0; i < numNodos; i++)
        for (int j = 0; j < numNodos; j++)
            dist[i][j] = grafo[i][j];

    // 2. TRES BUCLES ANIDADOS
    // k = nodo intermedio (puente)
    // i = origen
    // j = destino
    
    for (int k = 0; k < numNodos; k++) {          // Probamos cada nodo como puente
        for (int i = 0; i < numNodos; i++) {      // Para cada origen
            for (int j = 0; j < numNodos; j++) {  // Para cada destino
                
                // Si pasar por K es más corto que ir directo de i a j...
                if (dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j]; // ¡Actualizamos el atajo!
                }
                
            }
        }
    }

    // Imprimir la matriz final de caminos mínimos
    cout << "Matriz de distancias minimas entre todo par de nodos:\n";
    for (int i = 0; i < numNodos; i++) {
        for (int j = 0; j < numNodos; j++) {
            if (dist[i][j] == INF) cout << "INF\t";
            else cout << dist[i][j] << "\t";
        }
        cout << endl;
    }
}
```

-----

## 🥊 Resumen: ¿Cuál usar en el Parcial?

| Característica | Dijkstra | Roy-Warshall |
| :--- | :--- | :--- |
| **Objetivo** | De **UN** punto a todos los demás. | De **TODOS** a todos. |
| **Velocidad** | Muy rápido ($N^2$ o $N \log N$). | Lento ($N^3$). No usar con muchos nodos. |
| **Estructura** | Usa Listas de Adyacencia + Cola. | Usa Matriz de Adyacencia + 3 Bucles. |
| **Complejidad Código** | Más largo de escribir. | Muy corto (3 `for`), fácil de memorizar. |
| **Cuándo usar** | "Dada la ciudad A, halla el camino más corto a B". | "Halla la matriz de caminos mínimos". |

-----

### 🛠️ Tarea Visual para 
1.  **Dibujo:** Dibuja 3 ciudades (A, B, C) formando un triángulo.
      * A -\> B (Peso 10)
      * B -\> C (Peso 10)
      * A -\> C (Peso 50)
2.  **Pregunta Warshall:** Visualmente, ¿cuál es el camino directo de A a C? (Respuesta: 50).
3.  **Pregunta Warshall:** Si usamos B como puente (`k=B`), ¿cuánto suma A-\>B + B-\>C? (Respuesta: 20).
4.  **Conclusión:** Como 20 \< 50, la matriz se actualiza. ¡Eso es Warshall\!