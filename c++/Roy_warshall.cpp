#include <iostream>
#include <iomanip> // Para que la tabla se vea bonita (setw)

using namespace std;

// Definimos un número "Infinito" seguro (para evitar desbordamiento al sumar)
#define INF 999

const int N = 4; // Número de nodos fijo para el ejemplo

void imprimirMatriz(int matriz[N][N], string titulo) {
    cout << "\n--- " << titulo << " ---\n";
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (matriz[i][j] == INF) 
                cout << setw(5) << "INF";
            else 
                cout << setw(5) << matriz[i][j];
        }
        cout << endl;
    }
}

void RoyWarshall(int grafo[N][N]) {
    int dist[N][N];

    // 1. Copia inicial
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            dist[i][j] = grafo[i][j];

    // 2. EL ALGORITMO (3 Bucles)
    // k = Nodo Intermedio (El puente)
    for (int k = 0; k < N; k++) {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                
                // Si ir de 'i' a 'k' y luego de 'k' a 'j' es más corto...
                if (dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j]; // ¡Actualizamos!
                }
                
            }
        }
    }

    imprimirMatriz(dist, "MATRIZ FINAL (Caminos Minimos)");
}

int main() {
    // Definimos el grafo inicial (Matriz)
    // 0 conecta con 1 (5km) y 3 (10km)
    // 1 conecta con 2 (3km)
    // 2 conecta con 3 (1km)
    // 3 no conecta con nadie
    int grafo[N][N] = {
        {0,   5,   INF, 10},
        {INF, 0,   3,   INF},
        {INF, INF, 0,   1},
        {INF, INF, INF, 0}
    };

    imprimirMatriz(grafo, "MATRIZ INICIAL (Solo vecinos directos)");
    
    cout << "\nCalculando rutas optimas...\n";
    cout << "Buscando puentes para acortar caminos...\n";
    
    RoyWarshall(grafo);

    cout << "\nOBSERVACION: Mira como la distancia de (0 a 3) bajo de 10 a 9.";
    cout << "\nExplicacion: 0->1(5) + 1->2(3) + 2->3(1) = 9. ¡Es un mejor camino!";

    return 0;
}