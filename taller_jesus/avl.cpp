#include <iostream>
#include <algorithm> // Para max()
using namespace std;

struct Nodo {
    int valor;
    Nodo *izq, *der;
    int altura;
};

// Función para obtener altura (maneja nulos)
int altura(Nodo *n) {
    if (n == NULL) return 0;
    return n->altura;
}

// Crear nuevo nodo
Nodo* nuevoNodo(int valor) {
    Nodo* nodo = new Nodo();
    nodo->valor = valor;
    nodo->izq = nodo->der = NULL;
    nodo->altura = 1;
    return nodo;
}

// --- ROTACIONES (La Magia) ---

Nodo *rotarDerecha(Nodo *y) {
    Nodo *x = y->izq;
    Nodo *T2 = x->der;
    // Rotar
    x->der = y;
    y->izq = T2;
    // Actualizar alturas
    y->altura = max(altura(y->izq), altura(y->der)) + 1;
    x->altura = max(altura(x->izq), altura(x->der)) + 1;
    return x; // Nueva raíz
}

Nodo *rotarIzquierda(Nodo *x) {
    Nodo *y = x->der;
    Nodo *T2 = y->izq;
    // Rotar
    y->izq = x;
    x->der = T2;
    // Actualizar alturas
    x->altura = max(altura(x->izq), altura(x->der)) + 1;
    y->altura = max(altura(y->izq), altura(y->der)) + 1;
    return y; // Nueva raíz
}

// Obtener Factor de Equilibrio
int getBalance(Nodo *n) {
    if (n == NULL) return 0;
    return altura(n->izq) - altura(n->der);
}

// --- INSERTAR RECURSIVO ---
Nodo* insertar(Nodo* nodo, int valor) {
    // 1. Inserción normal de BST
    if (nodo == NULL) return nuevoNodo(valor);
    if (valor < nodo->valor)
        nodo->izq = insertar(nodo->izq, valor);
    else if (valor > nodo->valor)
        nodo->der = insertar(nodo->der, valor);
    else return nodo; // No duplicados

    // 2. Actualizar altura
    nodo->altura = 1 + max(altura(nodo->izq), altura(nodo->der));

    // 3. Ver si se desbalanceó
    int balance = getBalance(nodo);

    // Caso 1: Izquierda-Izquierda (Simple Der)
    if (balance > 1 && valor < nodo->izq->valor)
        return rotarDerecha(nodo);

    // Caso 2: Derecha-Derecha (Simple Izq)
    if (balance < -1 && valor > nodo->der->valor)
        return rotarIzquierda(nodo);

    // Caso 3: Izquierda-Derecha (Doble)
    if (balance > 1 && valor > nodo->izq->valor) {
        nodo->izq = rotarIzquierda(nodo->izq);
        return rotarDerecha(nodo);
    }

    // Caso 4: Derecha-Izquierda (Doble)
    if (balance < -1 && valor < nodo->der->valor) {
        nodo->der = rotarDerecha(nodo->der);
        return rotarIzquierda(nodo);
    }

    return nodo;
}

void preOrden(Nodo *root) {
    if(root != NULL) {
        cout << root->valor << " ";
        preOrden(root->izq);
        preOrden(root->der);
    }
}

int main() {
    Nodo *raiz = NULL;
    
    cout << "Insertando: 10, 20, 30, 40, 50, 25\n";
    raiz = insertar(raiz, 10);
    raiz = insertar(raiz, 20);
    raiz = insertar(raiz, 30); // Aquí rota solo
    raiz = insertar(raiz, 40);
    raiz = insertar(raiz, 50);
    raiz = insertar(raiz, 25);
    
    cout << "Recorrido Pre-Orden del AVL (Raiz -> Izq -> Der): \n";
    preOrden(raiz);
    
    return 0;
}