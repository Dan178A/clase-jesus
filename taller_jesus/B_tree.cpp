#include <iostream>
#include <vector>
using namespace std;

// Árbol B de Orden 3 (Máximo 2 claves, 3 hijos)
const int T = 2; // Grado mínimo (t). Max claves = 2*t - 1 = 3

class NodoB {
public:
    vector<int> claves; // Los números guardados
    vector<NodoB*> hijos; // Punteros a hijos
    bool esHoja; // ¿Es una hoja?

    NodoB(bool hoja) { esHoja = hoja; }

    // Función para partir una caja llena (SPLIT)
    void partirHijo(int i, NodoB* hijoLleno) {
        // Crear nueva caja para la mitad derecha
        NodoB* nuevoHermanito = new NodoB(hijoLleno->esHoja);

        // Mover la mitad de las claves al hermano
        // (En implementación real es un bucle, aquí simplificamos visualmente)
        // El hijoLleno tiene [10, 20, 30]. El 20 sube. El 30 se va al nuevo.
        
        // Insertar el del medio en MI lista de claves (Yo soy el Padre)
        claves.insert(claves.begin() + i, hijoLleno->claves[1]); // Sube el 20
        
        // Conectar el nuevo hermanito a mis hijos
        hijos.insert(hijos.begin() + i + 1, nuevoHermanito);
        
        // Limpiar y organizar las cajas de abajo...
        // (Lógica omitida para claridad del ejercicio: mover claves restantes)
        cout << "   * ¡CRACK! Se partio un nodo. El valor " << hijoLleno->claves[1] << " subio de nivel.\n";
    }

    // Insertar en un nodo que NO está lleno
    void insertarNoLleno(int k) {
        int i = claves.size() - 1;

        if (esHoja) {
            // Si soy hoja, simplemente busco el hueco y lo meto
            claves.push_back(0); // Espacio temporal
            while (i >= 0 && claves[i] > k) {
                claves[i+1] = claves[i]; // Mover a la derecha
                i--;
            }
            claves[i+1] = k; // Insertar
            cout << " -> Insertado " << k << " en una hoja.\n";
        } else {
            // Si no soy hoja, busco a qué hijo bajar
            while (i >= 0 && claves[i] > k) i--;
            i++; 

            // Si el hijo está lleno, lo parto antes de bajar
            if (hijos[i]->claves.size() == 3) { // 3 es overflow en este ejemplo
                partirHijo(i, hijos[i]);
                if (claves[i] < k) i++;
            }
            hijos[i]->insertarNoLleno(k);
        }
    }
};

class ArbolB {
    NodoB* raiz;
public:
    ArbolB() { raiz = NULL; }

    void insertar(int k) {
        if (raiz == NULL) {
            raiz = new NodoB(true);
            raiz->claves.push_back(k);
            cout << "Raiz creada con " << k << endl;
        } else {
            // Si la raíz está llena, el árbol crece hacia arriba
            if (raiz->claves.size() == 3) { 
                NodoB* nuevaRaiz = new NodoB(false);
                nuevaRaiz->hijos.push_back(raiz);
                nuevaRaiz->partirHijo(0, raiz); // La antigua raíz se parte
                
                int i = 0;
                if (nuevaRaiz->claves[0] < k) i++;
                nuevaRaiz->hijos[i]->insertarNoLleno(k);
                
                raiz = nuevaRaiz; // Actualizar puntero raíz
            } else {
                raiz->insertarNoLleno(k);
            }
        }
    }
};

int main() {
    cout << "=== SIMULACION INSERCION B-TREE ===\n";
    ArbolB t;
    t.insertar(10);
    t.insertar(20);
    t.insertar(30); // Aquí simulará el proceso de llenado
    t.insertar(40);
    return 0;
}