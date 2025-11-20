


**Árbol AVL · Árbol Rojo-Negro · Árbol 2–3 / B-Tree · Árbol de Merkle (Hash Tree)**

#  🟦 **1. Árbol AVL (Adelson-Velsky and Landis)**

## 📘 ¿Qué es?

Un **árbol binario de búsqueda** que **se auto-balancea** después de cada inserción/eliminación.

Cada nodo cumple:

```
factor_balance = altura(izquierda) – altura(derecha)
```

Debe estar siempre entre **–1, 0 o 1**.

---

## 🔄 **Rotaciones AVL**

Cuando el árbol se desbalancea, aplicamos una de estas rotaciones:

## **1. Rotación Simple a la Derecha (LL)**

```
        A
       /
      B
     /
    C
```

→ se transforma en:

```
      B
     / \
    C   A
```

---

## **2. Rotación Simple a la Izquierda (RR)**

```
    A
     \
      B
       \
        C
```

→

```
      B
     / \
    A   C
```

---

## **3. Rotación Doble Izquierda-Derecha (LR)**

```
      A
     /
    B
     \
      C
```

→ primero rotamos **B-C**, luego **A-B**.

---

## **4. Rotación Doble Derecha-Izquierda (RL)**

```
    A
     \
      B
     /
    C
```

---

## 🧠 **C++ Básico de AVL (Insertar + Rotaciones)**

```cpp
#include <iostream>
using namespace std;

struct Nodo {
    int valor;
    int altura;
    Nodo *izq, *der;

    Nodo(int v) {
        valor = v;
        altura = 1;
        izq = der = nullptr;
    }
};

int altura(Nodo* n) {
    return (n == nullptr) ? 0 : n->altura;
}

int balance(Nodo* n) {
    return (n == nullptr) ? 0 : altura(n->izq) - altura(n->der);
}

Nodo* rotDer(Nodo* y) {
    Nodo* x = y->izq;
    Nodo* T2 = x->der;

    x->der = y;
    y->izq = T2;

    y->altura = max(altura(y->izq), altura(y->der)) + 1;
    x->altura = max(altura(x->izq), altura(x->der)) + 1;

    return x;
}

Nodo* rotIzq(Nodo* x) {
    Nodo* y = x->der;
    Nodo* T2 = y->izq;

    y->izq = x;
    x->der = T2;

    x->altura = max(altura(x->izq), altura(x->der)) + 1;
    y->altura = max(altura(y->izq), altura(y->der)) + 1;

    return y;
}

Nodo* insertar(Nodo* nodo, int valor) {
    if (nodo == nullptr) 
        return new Nodo(valor);

    if (valor < nodo->valor)
        nodo->izq = insertar(nodo->izq, valor);
    else
        nodo->der = insertar(nodo->der, valor);

    nodo->altura = 1 + max(altura(nodo->izq), altura(nodo->der));

    int fb = balance(nodo);

    // Casos LL
    if (fb > 1 && valor < nodo->izq->valor)
        return rotDer(nodo);

    // Casos RR
    if (fb < -1 && valor > nodo->der->valor)
        return rotIzq(nodo);

    // Casos LR
    if (fb > 1 && valor > nodo->izq->valor) {
        nodo->izq = rotIzq(nodo->izq);
        return rotDer(nodo);
    }

    // Casos RL
    if (fb < -1 && valor < nodo->der->valor) {
        nodo->der = rotDer(nodo->der);
        return rotIzq(nodo);
    }

    return nodo;
}
```

---

# 🔴⚫ **2. Árbol Rojo-Negro (Red-Black Tree)**

## 📘 Propósito:

Mantener el árbol **casi balanceado** con reglas más simples que AVL.
Los buscadores web, bases de datos y la STL de C++ los usan.

---

## ❗ Reglas del Rojo-Negro

1. Todo nodo es **rojo o negro**.
2. La raíz **siempre es negra**.
3. Las hojas NIL son negras.
4. Un nodo rojo nunca puede tener hijos rojos (**no hay dos rojos seguidos**).
5. Todo camino desde un nodo hasta sus hojas NIL tiene **el mismo número de nodos negros**.

---

## 🌳 Ejemplo visual

```
        (10B)
       /     \
    (5R)     (20R)
```

---

## ⭐ Inserción simplificada

El código completo es largo, pero esta versión didáctica muestra los principios:

```cpp
enum Color { ROJO, NEGRO };

struct NodoRN {
    int valor;
    Color color;
    NodoRN *izq, *der, *padre;

    NodoRN(int v) {
        valor = v;
        color = ROJO;
        izq = der = padre = nullptr;
    }
};
```

---

# 🟥🟧 **3. Árbol 2–3 y B-Tree**

## 📘 Árbol 2–3

Todo nodo tiene:

* **1 o 2 claves**
* **2 o 3 hijos**

Reglas:

* Las hojas tienen la misma profundidad (siempre simétrico).
* Inserciones que desbordan generan **divisiones (split)**.

---

## 🌳 Ejemplo simple de 2–3

```
      [10 | 20]
     /    |    \
   <10  10-20  >20
```

---

## 📘 B-TREE (Generalización para discos, bases de datos)

Nivel *t* (grado mínimo):

* Cada nodo tiene entre `t-1` y `2t-1` claves.
* Excelente para almacenar **muchísima información** en estructuras externas.

---

## ⭐ Ejemplo B-Tree de grado t=2

```
          [10 | 20]
        /     |      \
      [5]   [12]   [30 | 40 | 50]
```

---

## ⭐ Código básico (estructuras)

```cpp
struct BTreeNode {
    int *keys;
    int t;
    BTreeNode **C;
    int n;
    bool leaf;

    BTreeNode(int _t, bool _leaf) {
        t = _t;
        leaf = _leaf;
        keys = new int[2*t - 1];
        C = new BTreeNode*[2*t];
        n = 0;
    }
};
```

---

# 🔐🌲 **4. Árbol de Merkle (Merkle Tree / Hash Tree)**

## 📘 ¿Qué es?

Un árbol binario donde **cada hoja es un hash de datos**,
y cada nodo interno es el hash de la **concatenación de sus hijos**.

Usado en:

* Criptomonedas (Bitcoin, Ethereum)
* Git
* Sistemas de verificación

---

## 🔍 Ejemplo visual

```
                H(ABCD)
              /         \
        H(AB)            H(CD)
        /   \            /   \
     H(A)  H(B)       H(C)  H(D)
```

Si un bit cambia → TODO EL ÁRBOL cambia.

---

## ⭐ C++ usando SHA1 simple (sin librerías externas)

(versión ilustrativa)

```cpp
string hashSimple(string s) {
    int h = 0;
    for(char c : s) h = (h * 131 + c) % 1000000;
    return to_string(h);
}

struct NodoMerkle {
    string hash;
    NodoMerkle *izq, *der;

    NodoMerkle(string h) {
        hash = h;
        izq = der = nullptr;
    }
};

NodoMerkle* construir(vector<string> datos) {
    vector<NodoMerkle*> nodos;

    for (auto& d : datos)
        nodos.push_back(new NodoMerkle(hashSimple(d)));

    while (nodos.size() > 1) {
        vector<NodoMerkle*> padres;

        for (int i = 0; i < nodos.size(); i += 2) {
            if (i + 1 == nodos.size()) {
                padres.push_back(nodos[i]);
                continue;
            }
            string h = hashSimple(nodos[i]->hash + nodos[i+1]->hash);
            NodoMerkle* padre = new NodoMerkle(h);
            padre->izq = nodos[i];
            padre->der = nodos[i+1];
            padres.push_back(padre);
        }
        nodos = padres;
        break
    }
    return nodos[0];
}
```