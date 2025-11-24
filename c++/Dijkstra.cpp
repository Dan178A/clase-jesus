#include <iostream>
#include <vector>
#include <queue>
#include <climits> // Para usar INT_MAX
#include <utility> // Para std::pair
#include <string>  // Para std::to_string
using namespace std;

const int INFINITO = INT_MAX;

// Estructura para representar una carretera
struct Arista {
    int destino;
    int peso; // Kilómetros o Minutos
};

// Clase para comparar en la cola de prioridad (Para que salga el menor primero)
struct Comparador {
    bool operator()(pair<int, int> const& a, pair<int, int> const& b) {
        return a.first > b.first;
    }
};

void Dijkstra(int nodoInicio, int numNodos, vector<vector<Arista>>& grafo) {
    // 1. Tabla de distancias (Iniciamos todo en "Desconocido/Infinito")
    vector<int> distancia(numNodos, INFINITO);
    distancia[nodoInicio] = 0;

    // 2. Cola de Prioridad: Guarda pares <DistanciaAcumulada, Nodo>
    // Ordena automáticamente para darnos siempre el nodo más cercano disponible
    priority_queue<pair<int, int>, vector<pair<int, int>>, Comparador> cola;
    
    cola.push({0, nodoInicio});

    cout << "\n=== INICIANDO DIJKSTRA DESDE NODO " << nodoInicio << " ===\n";

    while (!cola.empty()) {
        // Sacamos al ganador actual (el más cercano)
        int distActual = cola.top().first;
        int u = cola.top().second;
        cola.pop();

        // Si encontramos una distancia vieja en la cola que es peor que la actual, la ignoramos
        if (distActual > distancia[u]) continue;

        cout << " -> Visitando Nodo " << u << " (Distancia acumulada: " << distActual << ")\n";

        // 3. RELAJACIÓN: Miramos a los vecinos
        for (auto& arista : grafo[u]) {
            int v = arista.destino;
            int pesoCamino = arista.peso;

            // La Pregunta Clave: ¿Es más rápido ir por AQUÍ que por donde conocía antes?
            if (distancia[u] + pesoCamino < distancia[v]) {
                
                cout << "    * ¡ATAJO ENCONTRADO! Para ir al nodo " << v;
                cout << " antes costaba " << (distancia[v] == INFINITO ? "INF" : to_string(distancia[v]));
                cout << ", ahora cuesta " << distancia[u] + pesoCamino << endl;

                distancia[v] = distancia[u] + pesoCamino; // Actualizamos la tabla
                cola.push({distancia[v], v});             // Lo metemos para seguir explorando
            }
        }
    }

    // IMPRESIÓN FINAL
    cout << "\n=== RESULTADOS FINALES DESDE NODO " << nodoInicio << " ===\n";
    for (int i = 0; i < numNodos; i++) {
        cout << "Destino Nodo " << i << ": " << (distancia[i] == INFINITO ? "Inalcanzable" : to_string(distancia[i]) + " km") << endl;
    }
}

int main() {
    int numNodos = 5;
    // Grafo representado como vector de vectores (Listas de adyacencia)
    vector<vector<Arista>> grafo(numNodos);

    // Mapa de carreteras:
    // 0 conecta con 1 (10km) y 4 (5km)
    grafo[0].push_back({1, 10});
    grafo[0].push_back({4, 5});
    
    // 1 conecta con 2 (1km)
    grafo[1].push_back({2, 1});
    
    // 4 conecta con 1 (3km) y 2 (9km)
    grafo[4].push_back({1, 3});
    grafo[4].push_back({2, 9});
    
    // 2 conecta con 3 (4km)
    grafo[2].push_back({3, 4});

    // 3 conecta con 0 (7km)
    grafo[3].push_back({0, 7});

    Dijkstra(0, numNodos, grafo);

    return 0;
}