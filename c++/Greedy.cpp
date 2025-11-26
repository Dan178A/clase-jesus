//Objetivo: Asignar colores (números) tal que ningún vecino tenga el mismo. 
//Estrategia: Probar colores 0, 1, 2... y quedarse con el primero libre.
#include <iostream>
#include <vector>
#include <list>

using namespace std;

class GrafoColor {
    int V; 
    list<int> *adj; // Lista de adyacencia

public:
    GrafoColor(int V) {
        this->V = V;
        adj = new list<int>[V];
    }

    void agregarArista(int v, int w) {
        adj[v].push_back(w);
        adj[w].push_back(v); // No dirigido
    }
    void colorear() {
        vector<int> resultado(V); // Guarda el color de cada nodo

        // 1. Inicializar: Primer nodo color 0, el resto sin color (-1)
        resultado[0] = 0;
        for (int u = 1; u < V; u++) resultado[u] = -1;

        // Arreglo booleano para marcar colores ocupados por vecinos
        vector<bool> colorDisponible(V, true);

        // 2. Ir nodo por nodo asignando colores
        for (int u = 1; u < V; u++) {
            
            // Paso A: Ver qué colores usan mis vecinos
            for (int vecino : adj[u]) {
                if (resultado[vecino] != -1) {
                    // Si el vecino tiene color X, marco X como NO disponible
                    colorDisponible[resultado[vecino]] = false;
                }
            }

            // Paso B: Buscar el primer color True (Disponible)
            int color;
            for (color = 0; color < V; color++) {
                if (colorDisponible[color] == true) break;
            }

            resultado[u] = color; // Asignar
            cout << "Nodo " << u << " ---> Color Asignado: " << color << endl;

            // Paso C: Resetear arreglo para la siguiente vuelta
            for (int i : adj[u]) {
                if (resultado[i] != -1) colorDisponible[resultado[i]] = true;
            }
            // (Nota técnica: Resetearlo completo es más seguro pero lento, 
            //  aquí reseteamos solo los usados para optimizar).
             for (int i = 0; i < V; i++) colorDisponible[i] = true;
        }
    }
};

int main() {
    cout << "=== COLOREADO DE GRAFOS (GREEDY) ===\n";
    cout << "Regla: Vecinos no pueden tener el mismo numero.\n\n";

    GrafoColor g(5);
    // Creando un grafo con conexiones complejas
    g.agregarArista(0, 1);
    g.agregarArista(0, 2);
    g.agregarArista(1, 2); // 0, 1 y 2 forman un triangulo (necesitan 3 colores distintos)
    g.agregarArista(1, 3);
    g.agregarArista(2, 3);
    g.agregarArista(3, 4);

    cout << "Nodo 0 ---> Color Asignado: 0 (Inicio)\n"; // El primero siempre es 0
    g.colorear();

    return 0;
}