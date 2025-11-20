#include <iostream>
using namespace std;

struct NodoAVL {
    int dato;
    int altura;
    NodoAVL *izq, *der;
    // Constructor
    NodoAVL(int v) : dato(v), altura(1), izq(nullptr), der(nullptr) {}
};

int altura(NodoAVL* n) {
    // Retorna la altura del nodo o 0 si es nulo
    return n ? n->altura : 0;
}

int balance(NodoAVL* n) {
    // Retorna el balance del nodo (altura izquierda - altura derecha)
    return n ? altura(n->izq) - altura(n->der) : 0;
}

// NodoAVL* rotDer(NodoAVL* y) {
//     // Rotación simple a la derecha
//     NodoAVL* x = y->izq;
//     NodoAVL* T2 = x->der;

//     // Actualizar alturas
//     x->der = y;
//     y->izq = T2;
//     // Actualizar alturas
//     y->altura = max(altura(y->izq), altura(y->der)) + 1;
//     x->altura = max(altura(x->izq), altura(x->der)) + 1;

//     return x;
// }
NodoAVL* rotDer(NodoAVL* y) { // 'y' ES EL PADRE DESBALANCEADO
    
    // 1. 'x' se convierte en el hijo izquierdo del padre
    NodoAVL* x = y->izq; 
    NodoAVL* T2 = x->der;

    // 2. ¡LA MAGIA OCURRE AQUÍ!
    // El hijo ('x') ahora apunta al padre ('y') como su hijo derecho.
    // El padre ha sido "bajado" y el hijo "subido".
    x->der = y; 
    
    // 3. El antiguo hijo derecho de 'x' (T2) se convierte en el nuevo
    // hijo izquierdo de 'y' (el padre original).
    y->izq = T2;

    // ... se actualizan alturas ...
    y->altura = max(altura(y->izq), altura(y->der)) + 1;
    x->altura = max(altura(x->izq), altura(x->der)) + 1;
    // 4. Se retorna 'x', que ahora es el nuevo padre (la nueva raíz del subárbol)
    return x; 
}

NodoAVL* rotIzq(NodoAVL* x) {
    // Rotación simple a la izquierda
    NodoAVL* y = x->der;
    NodoAVL* T2 = y->izq;

    // Actualizar alturas
    y->izq = x;
    x->der = T2;
    // Actualizar alturas
    x->altura = max(altura(x->izq), altura(x->der)) + 1;
    y->altura = max(altura(y->izq), altura(y->der)) + 1;

    return y;
}

NodoAVL* insertarAVL(NodoAVL* nodo, int clave) {
    if (!nodo) return new NodoAVL(clave);

    // Insertar en subárbol izquierdo o derecho
    if (clave < nodo->dato)
        nodo->izq = insertarAVL(nodo->izq, clave);
    else if (clave > nodo->dato)
        nodo->der = insertarAVL(nodo->der, clave);
    else return nodo;

    nodo->altura = 1 + max(altura(nodo->izq), altura(nodo->der));
    int b = balance(nodo);

    if (b > 1 && clave < nodo->izq->dato) return rotDer(nodo);
    if (b < -1 && clave > nodo->der->dato) return rotIzq(nodo);
    if (b > 1 && clave > nodo->izq->dato) {
        nodo->izq = rotIzq(nodo->izq);
        return rotDer(nodo);
    }
    if (b < -1 && clave < nodo->der->dato) {
        nodo->der = rotDer(nodo->der);
        return rotIzq(nodo);
    }
    return nodo;
}

void inOrden(NodoAVL* r) {
    if (!r) return;
    inOrden(r->izq);
    cout << r->dato << " ";
    inOrden(r->der);
}

NodoAVL* mayorDeMenores(NodoAVL* nodo) {
    // El más grande del subárbol izquierdo
    // (ir a la izquierda una vez, y luego todo a la derecha)
    NodoAVL* actual = nodo->izq;
    while (actual != nullptr && actual->der != nullptr) {
        actual = actual->der;
    }
    return actual;
}

NodoAVL* menorDeMayores(NodoAVL* nodo) {
    // El más pequeño del subárbol derecho
    // (ir a la derecha una vez, y luego todo a la izquierda)
    NodoAVL* actual = nodo->der;
    while (actual != nullptr && actual->izq != nullptr) {
        actual = actual->izq;
    }
    return actual;
}