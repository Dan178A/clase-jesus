// C. Grafo con lista de adyacencia + BFS y DFS
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

class Grafo {
    int V;
    vector<vector<int>> adj;

public:
    Grafo(int v) : V(v) {
        adj.resize(v);
    }

    void agregarArista(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u); // si es no dirigido
    }

    void BFS(int inicio) {
        vector<bool> visitado(V, false);
        queue<int> q;

        visitado[inicio] = true;
        q.push(inicio);

        while (!q.empty()) {
            int actual = q.front();
            q.pop();
            cout << actual << " ";

            for (int vecino : adj[actual]) {
                if (!visitado[vecino]) {
                    visitado[vecino] = true;
                    q.push(vecino);
                }
            }
        }
    }

    void DFS(int inicio, vector<bool>& visitado) {
        visitado[inicio] = true;
        cout << inicio << " ";

        for (int v : adj[inicio])
            if (!visitado[v])
                DFS(v, visitado);
    }
};

int main() {
    Grafo g(5);
    g.agregarArista(0, 1);
    g.agregarArista(0, 2);
    g.agregarArista(1, 3);
    g.agregarArista(2, 4);

    cout << "BFS desde 0: ";
    g.BFS(0);

    vector<bool> vis(5, false);
    cout << "\nDFS desde 0: ";
    g.DFS(0, vis);
}
