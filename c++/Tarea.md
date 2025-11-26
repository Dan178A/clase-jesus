
# 📘 CUADERNO DE ENTRENAMIENTO: Estructuras Jerárquicas y Grafos

-----

## 📅 PARTE 1: Árboles y Montículos (Calentamiento)

### 🧠 Recordatorio Rápido

  * **Árbol Binario:** Jerarquía simple. Izquierda y Derecha.
  * **Montículo (Heap):** Árbol estricto. En un **Max-Heap**, el padre siempre es MAYOR que los hijos. Se llena de izquierda a derecha sin huecos. Se implementa con un **Vector**.

### ✏️ Actividad 1.1: El Arquitecto de Montículos (Papel y Lápiz)

**Instrucción:** Tienes la siguiente lista de números: `[10, 50, 30, 20, 60, 40]`.

1.  Dibuja un **Max-Heap** insertando los números uno por uno en ese orden. (Recuerda: Si un hijo es mayor que su padre, ¡intercámbialos/sube al hijo\!).
2.  Dibuja cómo queda el **Vector (Arreglo)** final que representa ese árbol.

> *Espacio para dibujar...*

### 💻 Actividad 1.2: El Traductor (Código)

**Instrucción:** Escribe una función pequeña en C++ que, dado un índice `i` de un arreglo, imprima quiénes son sus hijos.

```cpp
// Completa la función
void imprimirHijos(int i, vector<int>& heap) {
    int hijoIzq = ___________; // ¿Cuál es la fórmula?
    int hijoDer = ___________; // ¿Cuál es la fórmula?

    // Agrega un if para verificar que el hijo existe (que no se salga del tamaño del vector)
    if (__________) cout << "Hijo Izquierdo: " << heap[hijoIzq] << endl;
    if (__________) cout << "Hijo Derecho: " << heap[hijoDer] << endl;
}
```

-----

## 🕵️ PARTE 2: Árbol de Merkle (Lógica)

### 🧠 Recordatorio Rápido

Se usa para seguridad. Los padres contienen el **Hash** (huella) de la suma de sus hijos. Si una hoja cambia, la raíz cambia.

### ✏️ Actividad 2.1: El Detective (Visual)

**Escenario:** Tienes un Árbol de Merkle de 4 hojas (Datos A, B, C, D).

1.  Dibuja el árbol completo (Hojas -\> Padres -\> Raíz).
2.  Imagina que modificamos el **Dato C**.
3.  **Encierra en un círculo rojo** todos los nodos que cambiarían su Hash automáticamente.

> *Espacio para dibujar...*

-----

## 🌐 PARTE 3: Grafos - Fundamentos y Representación

### 🧠 Recordatorio Rápido

Redes de nodos conectados.

  * **Matriz de Adyacencia:** Tabla (Gastona de memoria).
  * **Lista de Adyacencia:** Arreglo de Listas (Eficiente, tu favorita).

### ✏️ Actividad 3.1: Del Dibujo al Código (Papel)

Mira este Grafo Dirigido:

  * A -\> B
  * A -\> C
  * B -\> D
  * C -\> B
  * D -\> A (Ciclo)

<!-- end list -->

1.  Dibuja el Grafo.
2.  Escribe su **Lista de Adyacencia** (Como si fuera una agenda telefónica).
      * `[A] -> ___ -> ___`
      * `[B] -> ___`
      * `[C] -> ___`
      * `[D] -> ___`

### 💻 Actividad 3.2: Constructor de Grafos (Código)

**Instrucción:** Completa el código para crear las conexiones del ejercicio anterior.

```cpp
struct Nodo {
    int destino;
    Nodo* siguiente;
};

// Arreglo de punteros (Asumimos: A=0, B=1, C=2, D=3)
Nodo* grafo[4]; 

// Tu tarea: Escribe las líneas para conectar A(0) con B(1) y C(2).
// Usa una función imaginaria agregarArista(origen, destino) o hazlo manual.

// ... Escribe tu código aquí ...
```

-----

## 🚶 PARTE 4: Recorridos (BFS y DFS)

### 🧠 Recordatorio Rápido

  * **BFS (Anchura):** Onda expansiva. Usa **Cola**. (Visita vecinos directos primero).
  * **DFS (Profundidad):** Laberinto. Usa **Recursión/Pila**. (Va al fondo y regresa).

### ✏️ Actividad 4.1: Simulador Humano

Usa el grafo que dibujaste en la Actividad 3.1.

1.  **Simulación BFS (Inicio A):**

      * Cola: `[A]` -\> Saco A, meto vecinos...
      * Escribe el orden en que se imprimen los nodos: `A, __, __, __`

2.  **Simulación DFS (Inicio A):**

      * Voy a A -\> Voy a su primer vecino B -\> Voy al vecino de B...
      * Escribe el orden de visita: `A, __, __, __`

-----

## 🏎️ PARTE 5: Algoritmos de Ruta (Dijkstra y Warshall)

### 🧠 Recordatorio Rápido

  * **Dijkstra:** Ruta más corta desde UN punto. Usa **Relajación** (¿Encontré un atajo?).
  * **Roy-Warshall:** Rutas entre TODOS los puntos. Usa **Matriz** y 3 bucles.

### ✏️ Actividad 5.1: Encontrando el Atajo

Tenemos 3 ciudades:

  * X -\> Y (Costo 10)
  * Y -\> Z (Costo 5)
  * X -\> Z (Costo 20)

<!-- end list -->

1.  Inicialmente, ¿cuál es la distancia que conocemos de X a Z? `___`
2.  Si aplicamos Dijkstra y visitamos Y... vemos que X-\>Y-\>Z suma `___`.
3.  ¿Es menor 15 que 20? (Sí/No). Entonces actualizamos. Esto se llama **Relajación**.

### 💻 Actividad 5.2: El Reto Final (Código Warshall)

**Instrucción:** Este código tiene un error grave en el orden de los bucles. ¡Arréglalo para que funcione Roy-Warshall\!

```cpp
// CÓDIGO CON ERROR
void RoyWarshall(int grafo[N][N]) {
    // Los bucles están desordenados. ¿Cuál debe ir afuera para ser el "Pivote/Puente"?
    for (int i = 0; i < N; i++) {      // Origen
        for (int j = 0; j < N; j++) {  // Destino
             for (int k = 0; k < N; k++) { // Puente <--- ¡ESTO ESTÁ MAL AQUÍ!
                
                if (grafo[i][k] + grafo[k][j] < grafo[i][j]) {
                    grafo[i][j] = grafo[i][k] + grafo[k][j];
                }
             }
        }
    }
}
```
