#include <iostream>
#include <vector>
#include <list>

using namespace std;

// Clase Grafo usando Lista de Adyacencia 
class Grafo {
    int numNodos;
    vector<list<int>> adj; // Arreglo de listas
    vector<bool> visitado; // Para no perderse en ciclos

public:
    Grafo(int V) {
        numNodos = V;
        adj.resize(V);
        visitado.resize(V, false);
    }

    // Función para añadir una arista (camino)
    void agregarArista(int origen, int destino) {
        adj[origen].push_back(destino); // Grafo dirigido
    }

    // El motor del DFS
    void DFS(int nodoActual, int nivel) {
        // Marcamos como visitado
        visitado[nodoActual] = true;

        // Visualización: Usamos espacios para simular "profundidad"
        string sangria = "";
        for(int i=0; i<nivel; i++) sangria += "    |"; // Dibuja la rama

        cout << sangria << "--> Entrando al nodo: " << nodoActual << endl;

        // Recorremos los vecinos
        for (int vecino : adj[nodoActual]) {
            if (!visitado[vecino]) {
                DFS(vecino, nivel + 1); // Llamada recursiva (baja un nivel)
            } else {
                cout << sangria << "    (El nodo " << vecino << " ya fue visitado, ignorar)" << endl;
            }
        }
        
        cout << sangria << "<-- Regresando del nodo: " << nodoActual << " (Backtracking)" << endl;
    }
};

int main() {
    cout << "=== SIMULACION VISUAL DFS (PROFUNDIDAD) ===" << endl;
    cout << "Imagina un laberinto. Vamos al fondo primero.\n" << endl;

    Grafo g(6); // Creamos 6 nodos (0 al 5)

    // Construimos el mapa
    g.agregarArista(0, 1);
    g.agregarArista(0, 2);
    g.agregarArista(1, 3);
    g.agregarArista(1, 4);
    g.agregarArista(2, 5);

    /* Estructura Visual del Grafo creado:
           0
         /   \
        1     2
       / \     \
      3   4     5
    */

    cout << "Iniciando recorrido desde el Nodo 0..." << endl;
    g.DFS(0, 0);

    return 0;
}