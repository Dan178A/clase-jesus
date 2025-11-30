-----

# 📘 Clase Maestra: Optimización en Grafos

**Temas:** Recubrimiento Mínimo (MST) y Coloración
**Objetivo:** Aprender a conectar puntos gastando lo mínimo y a organizar elementos sin conflictos.

-----

## 🏗️ Tema 4: Algoritmos de Recubrimiento Mínimo (MST)

### 1\. ¿Cuál es el problema? (La Analogía del Electricista)

imagina que eres un electricista. Tienes 5 casas (Nodos) y necesitas conectarlas todas a la red eléctrica. Tienes varias rutas posibles (Aristas), y cada ruta tiene un costo de cable diferente (Peso).

**Tu Misión:** Conectar TODAS las casas usando la menor cantidad de cable (dinero) posible.

  * **Regla de Oro:** No puedes dejar casas aisladas y **NO debes crear ciclos** (no necesitamos dar vueltas en círculo, solo conectar).
  * El resultado se llama **Árbol de Recubrimiento Mínimo (MST)**.

-----

### 2\. Solución A: Algoritmo de Kruskal (El Ahorrador)

**Estrategia:** "Busco las ofertas más baratas primero".

1.  Haces una lista de **todas** las aristas (conexiones) del mapa.
2.  Las ordenas de **MENOR a MAYOR** costo.
3.  Empiezas a elegir las más baratas.
4.  **OJO:** Si elegir una arista cierra un ciclo (conecta dos nodos que ya estaban conectados indirectamente), **la descartas**.

**Ejemplo Visual:**

  * Arista A-B (Costo 1): ¡La tomo\!
  * Arista C-D (Costo 2): ¡La tomo\!
  * Arista A-C (Costo 3): ¡La tomo\!
  * Arista B-D (Costo 4): **¡ALTO\!** Si uno B con D, se crea un ciclo (A-B-D-C-A). La descarto.

**Código C++ (Concepto con Estructuras):**
*Para Kruskal usamos una herramienta llamada "Union-Find" para detectar ciclos rápidamente.*

```cpp
struct Arista {
    int origen, destino, peso;
}; A--------B
   |        |
   |        |
   D--------C
      8
   A---->B// esto esta bien
   A<----B // esto crea ciclo


// Comparador para ordenar de menor a mayor
bool compararAristas(Arista a, Arista b) {
    return a.peso < b.peso;
}

void Kruskal(vector<Arista>& aristas, int numNodos) {
    // 1. ORDENAR por peso (Lo más barato primero)
    sort(aristas.begin(), aristas.end(), compararAristas);

    int costoTotal = 0;
    
    cout << "--- CONEXIONES ELEGIDAS (KRUSKAL) ---\n";
    
    // 2. Iterar sobre las aristas ordenadas
    for (Arista a : aristas) {
        // En código real, aquí usamos "find()" para ver si ya están conectados
        if (!formanCiclo(a.origen, a.destino)) { 
            cout << "Conectando " << a.origen << " - " << a.destino << " ($" << a.peso << ")\n";
            costoTotal += a.peso;
            unirConjuntos(a.origen, a.destino);
        }
    }
    cout << "Gasto Total Mínimo: $" << costoTotal << endl;
}
```

-----

### 3\. Solución B: Algoritmo de Prim (La Mancha de Aceite)

**Estrategia:** "Me expando desde donde estoy".

1.  Eliges un nodo inicial al azar (ej. Casa A).
2.  Miras **solo las conexiones que salen de tus casas ya conectadas**.
3.  Eliges la más barata que lleve a una casa **NUEVA** (no visitada).
4.  Repites hasta conectar todo.

**Diferencia Clave:**

  * **Kruskal:** Salta por todo el mapa buscando lo barato (Global).
  * **Prim:** Crece ordenadamente desde un punto (Local).

-----

## 🎨 Tema 5: Coloración de Grafos

### 1\. ¿Cuál es el problema? (El Mapa Político)

Tienes un mapa de países. Quieres pintarlos de modo que **ningún país vecino tenga el mismo color**.

  * **Reto:** Usar la menor cantidad de colores posible.
  * **Número Cromático:** Es ese número mínimo de colores necesarios.

![Image of graph coloring algorithm example](image.png)

### 2\. Algoritmo Greedy (El Avaricioso)

Es la forma más rápida y sencilla, aunque no siempre da el mínimo perfecto, funciona muy bien.

**Lógica:**

1.  Tomas el primer nodo.
2.  Le asignas el primer color disponible (Color 1).
3.  Pasas al siguiente nodo. Miras a sus vecinos ya pintados.
4.  Le asignas el color más bajo que **NO** estén usando sus vecinos.

**Ejemplo Visual:**

  * Nodo A: Le pongo **ROJO**.
  * Nodo B (Vecino de A): No puedo usar Rojo. Le pongo **AZUL**.
  * Nodo C (Vecino de A y B): No puedo Rojo ni Azul. Le pongo **VERDE**.
  * Nodo D (Vecino solo de A): No puedo Rojo. ¿Puedo Azul? Sí. Le pongo **AZUL**.

**Código C++ (Visualizador):**

```cpp
void ColorearGreedy(int numNodos, vector<int> adj[]) {
    int resultado[numNodos];
    
    // 1. Inicializar: Nadie tiene color (-1)
    resultado[0] = 0; // Al primer nodo le damos color 0
    for (int u = 1; u < numNodos; u++)
        resultado[u] = -1;

    // Arreglo para marcar colores ocupados por vecinos
    bool colorDisponible[numNodos]; 
    for (int i = 0; i < numNodos; i++) colorDisponible[i] = true;

    // 2. Colorear el resto
    for (int u = 1; u < numNodos; u++) {
        
        // A. Mirar vecinos y marcar sus colores como NO disponibles
        for (int vecino : adj[u]) {
            if (resultado[vecino] != -1) {
                colorDisponible[resultado[vecino]] = false;
            }
        }

        // B. Buscar el primer color libre
        int color;
        for (color = 0; color < numNodos; color++) {
            if (colorDisponible[color] == true) break;
        }

        resultado[u] = color; // Asignar color

        // C. Resetear disponibles para la siguiente vuelta
        for (int i = 0; i < numNodos; i++) colorDisponible[i] = true; 
    }

    // Imprimir
    for (int u = 0; u < numNodos; u++)
        cout << "Nodo " << u << " ---> Color " << resultado[u] << endl;
}
```

### 3\. Algoritmo de Brelaz (DSatur) - Nivel Experto // ejemplo pendiente

El algoritmo Greedy a veces falla si el orden de los nodos es malo. **Brelaz** es más inteligente porque elige **QUÉ nodo pintar primero**.

**Estrategia (Grado de Saturación):**

1.  En lugar de ir en orden (0, 1, 2...), eliges el nodo con **más vecinos ya coloreados con colores distintos**.
2.  ¿Por qué? Porque ese nodo es el más "difícil" o restringido. Mejor resolverlo pronto.
3.  Si hay empate, eliges el que tenga más vecinos en total (Grado).

-----

## 🛠️ Ejercicio Práctico

Dibuja 4 nodos formando un cuadrado (A, B, C, D) y una diagonal cruzada (A con C).

1.  **MST:**
      * Ponle pesos: A-B(1), B-C(2), C-D(3), D-A(4), A-C(10).
      * Ejecuta **Kruskal** mentalmente: ¿Qué aristas eliges? (Recuerda: ¡no ciclos\!).
2.  **Coloración:**
      * Intenta pintar ese grafo.
      * A (Color 1).
      * B es vecino de A -\> (Color 2).
      * C es vecino de A y B -\> (Color ?).

-----
# 🎨 Clase Extra: Algoritmo de Brelaz (DSatur)

**Tema:** Coloración Inteligente
**Objetivo:** Pintar el grafo usando menos colores que el método Greedy.

-----

## 1\. ¿Por qué necesitamos a Brelaz?

el algoritmo **Greedy** pinta los nodos en el orden que le demos (0, 1, 2...).

  * **El Problema:** Si tenemos mala suerte con el orden, Greedy puede usar 5 colores cuando solo se necesitaban 3.
  * **La Solución:** **Brelaz (DSatur)**. Este algoritmo no sigue un orden fijo. En cada paso, elige pintar el nodo que esté **"más estresado"** (el que tenga más restricciones).

### 📋 Las 2 Reglas de Brelaz

Para decidir a quién pintar, miramos dos cosas:

1.  **Regla de Oro (Saturación):** Elige el nodo que tenga **más vecinos con colores DIFERENTES**.
      * *Por qué:* Si un nodo tiene vecinos Rojo, Verde y Azul, está muy "saturado" (restringido). Hay que pintarlo YA antes de que se nos acaben las opciones.
2.  **Regla de Desempate (Grado):** Si dos nodos tienen la misma saturación, elige el que tenga **más vecinos en total** (el más popular).

-----

## 🧠 Ejemplo Visual Paso a Paso

Imagina un grafo con 5 nodos (A, B, C, D, E).

1.  **Paso 1:** Nadie tiene color. Saturación de todos = 0.
      * *Desempate:* Elegimos el nodo con más conexiones (Digamos que es **A**).
      * 🎨 Pintamos **A de Color 0**.
2.  **Paso 2:** Ahora miramos a los demás.
      * Los vecinos de A ahora tienen Saturación = 1 (tienen un vecino pintado).
      * Los que no son vecinos de A siguen en Saturación = 0.
      * *Decisión:* Elegimos un vecino de A (Digamos **B**).
      * 🎨 Pintamos **B de Color 1**.
3.  **Paso 3 (La Magia):**
      * Miramos al nodo **C**. Supongamos que C es vecino de A (Color 0) y de B (Color 1).
      * ¡La Saturación de C es 2\! (Está rodeado de dos colores distintos).
      * Miramos al nodo **D**. Solo es vecino de A. Su saturación es 1.
      * *Decisión:* Brelaz grita: "¡Pinten a **C** primero\! Es el más crítico".

-----

## 💻 El Código en C++ (Laboratorio)

```cpp
#include <iostream>
#include <vector>
#include <set> // Usamos set para contar colores únicos automáticamente

using namespace std;

struct NodoInfo {
    int id;
    int grado;          // Cuántos vecinos tiene
    int saturacion;     // Cuántos colores distintos tiene alrededor
    int color;          // Su color final (-1 si no tiene)
};

class GrafoBrelaz {
    int V;
    vector<vector<int>> adj; // Lista de adyacencia
    vector<NodoInfo> infoNodos;

public:
    GrafoBrelaz(int V) {
        this->V = V;
        adj.resize(V);
        infoNodos.resize(V);
        for(int i=0; i<V; i++) {
            infoNodos[i] = {i, 0, 0, -1}; // Inicializar: Sin color (-1)
        }
    }

    void agregarArista(int v, int w) {
        adj[v].push_back(w);
        adj[w].push_back(v);
        infoNodos[v].grado++; // Aumentamos la popularidad
        infoNodos[w].grado++;
    }

    // Función auxiliar para calcular la saturación real de un nodo
    int calcularSaturacion(int nodo) {
        set<int> coloresVecinos; // El 'set' elimina duplicados automáticamente
        for (int vecino : adj[nodo]) {
            if (infoNodos[vecino].color != -1) {
                coloresVecinos.insert(infoNodos[vecino].color);
            }
        }
        return coloresVecinos.size(); // Devuelve cuántos colores DISTINTOS hay
    }

    void colorearDSatur() {
        cout << "\n--- INICIANDO ALGORITMO DE BRELAZ (DSATUR) ---\n";
        
        for (int i = 0; i < V; i++) {
            // PASO 1: Elegir el mejor candidato
            int mejorNodo = -1;
            int maxSat = -1;
            int maxGrado = -1;

            for (int j = 0; j < V; j++) {
                if (infoNodos[j].color == -1) { // Solo mirar los no pintados
                    
                    // Actualizamos su saturación actual
                    int satActual = calcularSaturacion(j);
                    
                    // Lógica de Brelaz:
                    // 1. Mayor Saturación gana
                    // 2. Empate? Mayor Grado gana
                    if (satActual > maxSat || (satActual == maxSat && infoNodos[j].grado > maxGrado)) {
                        mejorNodo = j;
                        maxSat = satActual;
                        maxGrado = infoNodos[j].grado;
                    }
                }
            }

            if (mejorNodo == -1) break; // Ya pintamos todos

            // PASO 2: Asignarle el primer color disponible (Igual que Greedy)
            vector<bool> disponible(V, true);
            for (int vecino : adj[mejorNodo]) {
                if (infoNodos[vecino].color != -1) {
                    disponible[infoNodos[vecino].color] = false;
                }
            }

            int colorEscogido;
            for (colorEscogido = 0; colorEscogido < V; colorEscogido++) {
                if (disponible[colorEscogido]) break;
            }

            // Pintar
            infoNodos[mejorNodo].color = colorEscogido;
            cout << "Turno " << i+1 << ": El nodo mas critico es " << mejorNodo 
                 << " (Sat: " << maxSat << "). Le damos Color " << colorEscogido << endl;
        }
    }
};

int main() {
    // Ejemplo: Un grafo "Rueda" (Un centro conectado a todos los de afuera)
    // Este es difícil para Greedy pero fácil para Brelaz.
    GrafoBrelaz g(6); // Centro (0) y 5 externos (1-5)

    // El 0 conecta con todos (Es el más popular)
    g.agregarArista(0, 1); g.agregarArista(0, 2); g.agregarArista(0, 3);
    g.agregarArista(0, 4); g.agregarArista(0, 5);

    // Los de afuera se conectan en círculo
    g.agregarArista(1, 2); g.agregarArista(2, 3); g.agregarArista(3, 4);
    g.agregarArista(4, 5); g.agregarArista(5, 1);

    g.colorearDSatur();

    return 0;
}
```

-----

## 📝 Tarea Rápida

1.  **Ejecuta el código:** Observa la consola.
2.  **Pregunta:** ¿A quién pintó primero el algoritmo?
      * *Respuesta esperada:* Debería pintar al **Nodo 0** primero.
      * *Por qué:* Aunque al principio todos tienen saturación 0, el Nodo 0 gana el desempate porque tiene **grado 5** (es amigo de todos), mientras que los otros tienen grado 3.
3.  **Conclusión:** Brelaz atacó el problema más grande (el centro) primero, simplificando el resto del mapa.

-----

