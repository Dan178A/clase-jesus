#include <iostream>
#include <vector>
#include <list>
#include <queue> // Necesario para BFS

using namespace std;

class GrafoBFS {
    int numNodos;
    vector<list<int>> adj;

public:
    GrafoBFS(int V) {
        numNodos = V;
        adj.resize(V);
    }

    void agregarArista(int origen, int destino) {
        adj[origen].push_back(destino);
    }

    void BFS(int inicio) {
        // Vector para marcar visitados
        vector<bool> visitado(numNodos, false);
        // La COLA (FIFO) es el corazón del BFS
        queue<int> cola;

        // Paso 1: Marcar inicio y meterlo a la cola
        visitado[inicio] = true;
        cola.push(inicio);

        int nivelActual = 0;
        
        cout << "\nNIVEL 0 (INICIO):" << endl;

        while(!cola.empty()) {
            // Sacamos el frente de la cola
            int actual = cola.front();
            cola.pop();
            
            cout << " [Visitando Nodo " << actual << "] --> Sus vecinos son: ";

            // Revisamos a todos los vecinos
            bool tieneVecinosNuevos = false;
            for (int vecino : adj[actual]) {
                if (!visitado[vecino]) {
                    visitado[vecino] = true;
                    cola.push(vecino);
                    cout << vecino << " "; // Los mostramos
                    tieneVecinosNuevos = true;
                }
            }
            
            if(!tieneVecinosNuevos) cout << "(Ninguno nuevo)";
            cout << endl;
            
            // Nota: Esta visualización es lineal, el BFS real procesa la cola dinámicamente.
        }
    }
};

int main() {
    cout << "=== SIMULACION VISUAL BFS (ANCHURA) ===" << endl;
    cout << "Imagina una onda de agua expandiendose.\n" << endl;

    GrafoBFS g(6);
    
    // Mismo grafo para comparar
    g.agregarArista(0, 1);
    g.agregarArista(0, 2);
    g.agregarArista(1, 3);
    g.agregarArista(1, 4);
    g.agregarArista(2, 5);

    /* Nivel 0: [0]
       Nivel 1: [1, 2]
       Nivel 2: [3, 4, 5]
    */

    cout << "Cola de exploracion paso a paso:" << endl;
    g.BFS(0);

    return 0;
}