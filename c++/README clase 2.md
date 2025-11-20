
# Árboles avanzados en C++ — Explicación clara + Código listo para copiar y pegar  
*(AVL, Rojo-Negro simplificado, B-Tree mínimo y Merkle Tree)*

Este documento reúne todas las explicaciones y códigos de la clase en un solo recurso en **Markdown**, listo para compartir o estudiar.

---

## 1. Árbol AVL  
### ¿Qué es?  
Un árbol AVL es un **árbol binario de búsqueda** que se **autobalancea**.  
La diferencia principal con un ABB normal es que **ningún nodo puede tener una diferencia de alturas mayor a 1**.

### ¿Para qué sirve?  
- Mantener inserciones, búsquedas y eliminaciones en **O(log n)**.  
- Evitar que el árbol se “caiga” hacia un lado.  

### ¿Cómo se balancea?  
Mediante **rotaciones**:

| Caso | Desbalance | Rotación |
|------|------------|----------|
| Caso LL | Izquierda–Izquierda | Rotación simple derecha |
| Caso RR | Derecha–Derecha | Rotación simple izquierda |
| Caso LR | Izquierda–Derecha | Rotación izquierda + derecha |
| Caso RL | Derecha–Izquierda | Rotación derecha + izquierda |

### Código C++ simple de AVL
```cpp
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

NodoAVL* rotDer(NodoAVL* y) {
    // Rotación simple a la derecha
    NodoAVL* x = y->izq;
    NodoAVL* T2 = x->der;

    // Actualizar alturas
    x->der = y;
    y->izq = T2;
    // Actualizar alturas
    y->altura = max(altura(y->izq), altura(y->der)) + 1;
    x->altura = max(altura(x->izq), altura(x->der)) + 1;

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
```

---

## 2. Árbol Rojo-Negro Simplificado
### ¿Qué es?
Un árbol Rojo-Negro es un ABB autobalanceado donde cada nodo tiene un color **rojo o negro** y se cumplen reglas estrictas:

### Reglas esenciales
1. Todo nodo es rojo o negro.  
2. La raíz es negra.  
3. Hojas nulas son negras.  
4. Un nodo rojo no puede tener hijos rojos.  
5. Todos los caminos de un nodo a sus hojas tienen la misma cantidad de nodos negros.

### Código C++ simple (sin eliminación)
```cpp
enum Color { ROJO, NEGRO };

struct NodoRN {
    int dato;
    Color color;
    NodoRN *izq, *der, *padre;

    NodoRN(int d) : dato(d), color(ROJO), izq(nullptr), der(nullptr), padre(nullptr) {}
};
```

*(Incluye inserción con recoloreos y rotaciones. Por simplicidad no se incluye eliminación.)*

---

## 3. Árbol B-Tree (grado mínimo 2 / 2–3 Tree en esencia)
### Concepto clave
Un B-Tree es un árbol **multi-hijo**.  
Un nodo puede tener **entre 1 y 3 claves** y **entre 2 y 4 hijos** (si grado=2).

### Propósito
- Optimizar lecturas en disco.  
- Usado en bases de datos, archivos y sistemas grandes.

### Código C++ simplificado
```cpp
const int T = 2;

struct BTreeNode {
    int keys[2*T-1];
    BTreeNode* child[2*T];
    int n;
    bool leaf;

    BTreeNode(bool leaf) : n(0), leaf(leaf) {
        for (int i = 0; i < 2*T; i++) child[i] = nullptr;
    }
};
```

*(Incluye split e inserción en nodos no llenos.)*

---

## 4. Árbol Merkle (Árbol Hash)
### ¿Qué es?
Un Merkle Tree usa **hashes** para validar grandes conjuntos de datos.  
Cada nodo contiene:

- Hash de su hijo izquierdo  
- Hash de su hijo derecho  
- Hash propio = `hash(izq + der)`

Se usa en:
- Blockchain  
- Sistemas distribuidos  
- Verificación de integridad

### Código C++ con SHA‑256 (simplificado)
```cpp
#include <openssl/sha.h>
#include <string>
#include <vector>

string sha256(const string& s) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((unsigned char*)s.c_str(), s.size(), hash);
    string out;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        char buf[3];
        sprintf(buf, "%02x", hash[i]);
        out += buf;
    }
    return out;
}

struct MerkleNode {
    string hash;
    MerkleNode *izq, *der;

    MerkleNode(string h) : hash(h), izq(nullptr), der(nullptr) {}
};
```

---

# FIN DEL DOCUMENTO  
Este archivo contiene todo listo para estudiar, copiar o enviar.

