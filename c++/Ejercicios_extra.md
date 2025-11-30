# Ejercicios Extra de Grafos
-----

## 📂 ARCHIVO 1: Recorridos Básicos (BFS y DFS)

**Tema 3 (Parte 1)**
**Objetivo:** Ver la diferencia entre explorar por "Niveles" (Onda) vs "Profundidad" (Laberinto).

```cpp
#include <iostream>
#include <vector>
#include <list>
#include <queue> // Para BFS

using namespace std;

class GrafoRecorridos {
    int V;
    vector<list<int>> adj;
    vector<bool> visitado;

public:
    GrafoRecorridos(int V) {
        this->V = V;
        adj.resize(V);
    }

    void agregarArista(int v, int w) {
        adj[v].push_back(w); // Grafo dirigido
    }

    // --- ALGORITMO BFS (ANCHURA / NIVELES) ---
    void BFS(int inicio) {
        vector<bool> visitadoBFS(V, false);
        queue<int> cola;

        visitadoBFS[inicio] = true;
        cola.push(inicio);

        cout << "\n--- INICIO BFS (Modo Radar/Onda) ---\n";

        while(!cola.empty()) {
            int actual = cola.front();
            cola.pop();
            cout << " -> Visitando: " << actual << " | Vecinos por ver: ";

            for(int vecino : adj[actual]) {
                if(!visitadoBFS[vecino]) {
                    visitadoBFS[vecino] = true;
                    cola.push(vecino);
                    cout << "[" << vecino << "] ";
                }
            }
            cout << endl;
        }
        cout << "--- FIN BFS ---\n";
    }

    // --- ALGORITMO DFS (PROFUNDIDAD / LABERINTO) ---
    void DFS_Recursivo(int v, vector<bool>& visitados, int nivel) {
        visitados[v] = true;
        
        // Dibujamos espacios para simular profundidad
        string sangria = "";
        for(int i=0; i<nivel; i++) sangria += "   |";

        cout << sangria << "--> Entrando a: " << v << endl;

        for (int vecino : adj[v]) {
            if (!visitados[vecino]) {
                DFS_Recursivo(vecino, visitados, nivel + 1);
            }
        }
    }

    void DFS(int inicio) {
        vector<bool> visitados(V, false);
        cout << "\n--- INICIO DFS (Modo Laberinto) ---\n";
        DFS_Recursivo(inicio, visitados, 0);
        cout << "--- FIN DFS ---\n";
    }
};

int main() {
    GrafoRecorridos g(6);
    // Grafo de ejemplo
    g.agregarArista(0, 1); g.agregarArista(0, 2);
    g.agregarArista(1, 3); g.agregarArista(1, 4);
    g.agregarArista(2, 5);

    g.BFS(0); // Ejecutar Anchura
    g.DFS(0); // Ejecutar Profundidad

    return 0;
}
```

-----

## 📂 ARCHIVO 2: Rutas Óptimas (Dijkstra y Roy-Warshall)

**Tema 3 (Parte 2)**
**Objetivo:** Comparar "Ruta desde un punto" (Dijkstra) vs "Todas las rutas posibles" (Warshall).

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <climits>
#include <iomanip>

using namespace std;

const int INF = 999; // Usamos un número grande pero seguro para evitar overflow

// --- 1. ALGORITMO DE DIJKSTRA ---
struct Par {
    int distancia;
    int nodo;
    // Sobrecarga para que la cola ordene de MENOR a MAYOR
    bool operator>(const Par& otro) const {
        return distancia > otro.distancia;
    }
};

void Dijkstra(int inicio, int N, vector<vector<pair<int,int>>>& adj) {
    priority_queue<Par, vector<Par>, greater<Par>> cola;
    vector<int> dist(N, INF);

    dist[inicio] = 0;
    cola.push({0, inicio});

    cout << "\n--- DIJKSTRA (Desde nodo " << inicio << ") ---\n";

    while (!cola.empty()) {
        int d = cola.top().distancia;
        int u = cola.top().nodo;
        cola.pop();

        if (d > dist[u]) continue;

        for (auto vecino : adj[u]) {
            int v = vecino.first;
            int peso = vecino.second;

            // RELAJACION: ¿Encontre un camino mas corto?
            if (dist[u] + peso < dist[v]) {
                cout << "   * Atajo encontrado hacia " << v << ": Antes " << dist[v] << ", Ahora " << dist[u] + peso << endl;
                dist[v] = dist[u] + peso;
                cola.push({dist[v], v});
            }
        }
    }
}

// --- 2. ALGORITMO ROY-WARSHALL ---
void RoyWarshall(int grafo[4][4], int N) {
    int dist[4][4];
    // Copiar grafo
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            dist[i][j] = grafo[i][j];

    cout << "\n--- ROY-WARSHALL (Calculando matriz) ---\n";
    
    // K es el nodo intermedio (PUENTE)
    for (int k = 0; k < N; k++) {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }

    // Imprimir
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if(dist[i][j] == INF) cout << setw(4) << "INF";
            else cout << setw(4) << dist[i][j];
        }
        cout << endl;
    }
}

int main() {
    // Datos para Dijkstra
    int N_Dijkstra = 5;
    vector<vector<pair<int,int>>> adj(N_Dijkstra);
    adj[0].push_back({1, 10}); adj[0].push_back({4, 5});
    adj[1].push_back({2, 1}); adj[4].push_back({1, 3}); adj[4].push_back({2, 9});
    adj[2].push_back({3, 4}); 
    
    Dijkstra(0, N_Dijkstra, adj);

    // Datos para Warshall
    int grafo[4][4] = {
        {0, 5, INF, 10},
        {INF, 0, 3, INF},
        {INF, INF, 0, 1},
        {INF, INF, INF, 0}
    };
    RoyWarshall(grafo, 4);

    return 0;
}
```

-----

## 📂 ARCHIVO 3: Recubrimiento Mínimo (Kruskal y Prim)

**Tema 4**
**Objetivo:** Conectar todos los nodos gastando lo mínimo (Cables, tuberías).

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>

using namespace std;

// Estructura para Kruskal
struct Arista {
    int u, v, peso;
    bool operator<(const Arista& otra) const { // Para ordenar
        return peso < otra.peso;
    }
};

// --- KRUSKAL (Union-Find) ---
struct UnionFind {
    vector<int> padre;
    UnionFind(int n) {
        padre.resize(n);
        for(int i=0; i<n; i++) padre[i] = i;
    }
    int find(int x) {
        if(padre[x] == x) return x;
        return find(padre[x]);
    }
    void unite(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        if(rootX != rootY) padre[rootX] = rootY;
    }
};

void Kruskal(vector<Arista> aristas, int N) {
    sort(aristas.begin(), aristas.end()); // Paso 1: Ordenar
    UnionFind uf(N);
    int costo = 0;

    cout << "\n--- KRUSKAL (El Ahorrador) ---\n";
    for(auto a : aristas) {
        if(uf.find(a.u) != uf.find(a.v)) {
            cout << " [SI] Conecto " << a.u << "-" << a.v << " ($" << a.peso << ")\n";
            costo += a.peso;
            uf.unite(a.u, a.v);
        } else {
            cout << " [NO] Descarto " << a.u << "-" << a.v << " (Ciclo)\n";
        }
    }
    cout << "Costo Total Kruskal: " << costo << endl;
}

// --- PRIM (La Mancha de Aceite) ---
typedef pair<int, int> pii; // <Peso, Destino>

void Prim(int N, vector<vector<pii>>& adj) {
    priority_queue<pii, vector<pii>, greater<pii>> pq;
    vector<bool> visitado(N, false);
    int costo = 0;

    pq.push({0, 0}); // Empezar en nodo 0 con costo 0

    cout << "\n--- PRIM (Crecimiento Local) ---\n";
    while(!pq.empty()) {
        int p = pq.top().first;
        int u = pq.top().second;
        pq.pop();

        if(visitado[u]) continue; // Ya lo tenemos

        visitado[u] = true;
        costo += p;
        if(p > 0) cout << " -> Agrego nodo " << u << " (Costo arista: " << p << ")\n";

        for(auto vecino : adj[u]) {
            if(!visitado[vecino.second]) {
                pq.push(vecino);
            }
        }
    }
    cout << "Costo Total Prim: " << costo << endl;
}

int main() {
    int N = 4;
    // Grafo para Kruskal
    vector<Arista> aristas = { {0,1,10}, {0,2,6}, {0,3,5}, {1,3,15}, {2,3,4} };
    Kruskal(aristas, N);

    // Grafo para Prim (Lista de Adyacencia)
    vector<vector<pii>> adj(N);
    adj[0].push_back({10, 1}); adj[1].push_back({10, 0});
    adj[0].push_back({6, 2});  adj[2].push_back({6, 0});
    adj[0].push_back({5, 3});  adj[3].push_back({5, 0});
    adj[2].push_back({4, 3});  adj[3].push_back({4, 2});
    
    Prim(N, adj);
    return 0;
}
```

-----

## 📂 ARCHIVO 4: Coloración (Greedy y Brelaz)

**Tema 5**
**Objetivo:** Pintar el mapa sin que vecinos se repitan.

```cpp
#include <iostream>
#include <vector>
#include <set>
#include <algorithm>

using namespace std;

class GrafoColor {
    int V;
    vector<vector<int>> adj;

public:
    GrafoColor(int V) {
        this->V = V;
        adj.resize(V);
    }

    void agregarArista(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    // --- ALGORITMO GREEDY (El Rapido) ---
    void Greedy() {
        vector<int> resultado(V, -1);
        resultado[0] = 0; // Al primero le damos color 0

        cout << "\n--- COLORACION GREEDY ---\n";
        
        for (int u = 1; u < V; u++) {
            vector<bool> disponible(V, true);
            
            // Ver colores de vecinos
            for (int i : adj[u])
                if (resultado[i] != -1)
                    disponible[resultado[i]] = false;

            // Buscar el primer disponible
            int color;
            for (color = 0; color < V; color++)
                if (disponible[color]) break;

            resultado[u] = color;
            cout << "Nodo " << u << " -> Color " << color << endl;
        }
    }

    // --- ALGORITMO BRELAZ / DSATUR (El Inteligente) ---
    // Calcula la saturacion (cuantos colores distintos tiene alrededor)
    int getSaturacion(int u, const vector<int>& colores) {
        set<int> coloresVecinos;
        for(int v : adj[u]) {
            if(colores[v] != -1) coloresVecinos.insert(colores[v]);
        }
        return coloresVecinos.size();
    }

    void Brelaz() {
        vector<int> resultado(V, -1);
        vector<bool> coloreado(V, false);
        int nodosPintados = 0;

        cout << "\n--- COLORACION BRELAZ (DSATUR) ---\n";

        while(nodosPintados < V) {
            int mejorNodo = -1;
            int maxSat = -1;
            int maxGrado = -1;

            // 1. ELEGIR EL NODO MAS CRITICO
            for(int i=0; i<V; i++) {
                if(!coloreado[i]) {
                    int sat = getSaturacion(i, resultado);
                    int grado = adj[i].size();

                    // Prioridad: Mayor Saturacion > Mayor Grado
                    if(sat > maxSat || (sat == maxSat && grado > maxGrado)) {
                        maxSat = sat;
                        maxGrado = grado;
                        mejorNodo = i;
                    }
                }
            }

            // 2. PINTARLO (Igual que Greedy)
            vector<bool> disponible(V, true);
            for (int vecino : adj[mejorNodo])
                if (resultado[vecino] != -1)
                    disponible[resultado[vecino]] = false;

            int color;
            for (color = 0; color < V; color++)
                if (disponible[color]) break;

            resultado[mejorNodo] = color;
            coloreado[mejorNodo] = true;
            nodosPintados++;

            cout << "Turno " << nodosPintados << ": Pinto Nodo " << mejorNodo 
                 << " (Sat: " << maxSat << ") -> Color " << color << endl;
        }
    }
};

int main() {
    GrafoColor g(5);
    // Grafo dificil: 0 conectado a todos (Rueda)
    g.agregarArista(0, 1); g.agregarArista(0, 2);
    g.agregarArista(0, 3); g.agregarArista(0, 4);
    g.agregarArista(1, 2); g.agregarArista(2, 3);
    g.agregarArista(3, 4); g.agregarArista(4, 1);

    g.Greedy();
    g.Brelaz(); // Observa que Brelaz elegira al 0 primero por su alto grado

    return 0;
}
```