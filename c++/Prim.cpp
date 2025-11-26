//Algoritmo de Prim (La Mancha de Aceite): Igual que Kruskal, pero creciendo desde un nodo inicial. 
//Estructura: Lista de Adyacencia + Cola de Prioridad.
#include <iostream>
#include <vector>
#include <queue> // Necesario para priority_queue

using namespace std;

// Usamos pair para guardar <Peso, Destino>
typedef pair<int, int> Par;

int main() {
    cout << "\n=== ALGORITMO DE PRIM (Creciendo desde el nodo 0) ===\n";

    int numNodos = 4;
    // Lista de Adyacencia: grafo[origen] contiene pares {peso, destino}
    vector<vector<Par>> grafo(numNodos);

    // Mismo grafo que Kruskal
    // 0 conecta con...
    grafo[0].push_back({10, 1});
    grafo[0].push_back({6, 2});
    grafo[0].push_back({5, 3});
    
    // 1 conecta con...
    grafo[1].push_back({10, 0});
    grafo[1].push_back({15, 3});
    
    // 2 conecta con...
    grafo[2].push_back({6, 0});
    grafo[2].push_back({4, 3}); // C-D
    
    // 3 conecta con...
    grafo[3].push_back({5, 0});
    grafo[3].push_back({15, 1});
    grafo[3].push_back({4, 2}); // D-C

    // COLA DE PRIORIDAD (Min-Heap: El menor arriba)
    priority_queue<Par, vector<Par>, greater<Par>> cola;

    int costoTotal = 0;
    vector<bool> visitado(numNodos, false);

    // Empezamos en nodo 0, costo 0
    cola.push({0, 0}); 

    while(!cola.empty()) {
        // Sacamos el mas barato disponible
        int costo = cola.top().first;
        int nodoActual = cola.top().second;
        cola.pop();

        // Si ya lo conectamos antes, ignorar
        if(visitado[nodoActual]) continue;

        // ¡Lo conectamos!
        visitado[nodoActual] = true;
        costoTotal += costo;
        
        if (costo > 0) // Para no imprimir el nodo inicial 0 con costo 0
             cout << " -> Conectando nodo " << nodoActual << " (Costo agregado: " << costo << ")\n";

        // Añadir vecinos a la cola
        for(auto vecino : grafo[nodoActual]) {
            int pesoArista = vecino.first;
            int nodoVecino = vecino.second;
            
            if(!visitado[nodoVecino]) {
                cola.push({pesoArista, nodoVecino});
            }
        }
    }

    cout << "Costo Minimo Total: " << costoTotal << endl;
    return 0;
}