//Algoritmo de Kruskal: Encuentra el Recubrimiento Mínimo en un grafo ponderado usando una estrategia voraz (greedy).
#include <iostream>
#include <vector>
#include <algorithm> // Para ordenar (sort)

using namespace std;

// 1. Estructura de la Arista
struct Arista {
    int origen, destino, peso;
};

// 2. Comparador para ordenar de MENOR a MAYOR peso
bool comparar(Arista a, Arista b) {
    return a.peso < b.peso;
}

// 3. Estructura para detectar ciclos (Union-Find simple)
struct UnionFind {
    int padre[100];
    
    void iniciar(int n) {
        for(int i = 0; i < n; i++) padre[i] = i; // Cada uno es su propio jefe al inicio
    }
    
    int encontrarJefe(int i) {
        if (padre[i] == i) return i;
        return encontrarJefe(padre[i]);
    }
    
    void unir(int i, int j) {
        int jefeI = encontrarJefe(i);
        int jefeJ = encontrarJefe(j);
        if (jefeI != jefeJ) padre[jefeI] = jefeJ; // Ahora son del mismo equipo
    }
};

int main() {
    cout << "=== ALGORITMO DE KRUSKAL (Recubrimiento Minimo) ===\n";
    
    // Definimos las conexiones posibles y sus precios
    // Grafo: 4 Nodos (0, 1, 2, 3)
    vector<Arista> aristas = {
        {0, 1, 10}, // A-B cuesta 10
        {0, 2, 6},  // A-C cuesta 6
        {0, 3, 5},  // A-D cuesta 5
        {1, 3, 15}, // B-D cuesta 15
        {2, 3, 4}   // C-D cuesta 4
    };

    // PASO 1: Ordenar por precio (Lo mas barato primero)
    sort(aristas.begin(), aristas.end(), comparar);

    UnionFind uf;
    uf.iniciar(4); // 4 nodos

    int costoTotal = 0;
    cout << "Analizando aristas ordenadas...\n";

    // PASO 2: Iterar y elegir
    for (Arista a : aristas) {
        int jefeOrigen = uf.encontrarJefe(a.origen);
        int jefeDestino = uf.encontrarJefe(a.destino);

        if (jefeOrigen != jefeDestino) {
            // No tienen el mismo jefe, asi que NO forman ciclo. ¡La elegimos!
            cout << " [SI] Conectando nodo " << a.origen << " con " << a.destino 
                 << " (Costo: " << a.peso << ")\n";
            
            uf.unir(a.origen, a.destino);
            costoTotal += a.peso;
        } else {
            // Ya tienen el mismo jefe, estan conectados indirectamente.
            cout << " [NO] Descartando " << a.origen << "-" << a.destino 
                 << " (Costo: " << a.peso << ") -> ¡Formaria un CICLO!\n";
        }
    }

    cout << "\n--- RESULTADO FINAL ---\n";
    cout << "Costo Minimo Total para conectar todo: " << costoTotal << endl;

    return 0;
}