#include <iostream>
#include <string>
#include <ctime>
using namespace std;

struct Nodo {
    string nombre;
    int tipo;
    time_t fechaCreacion;
    time_t fechaModificacion;
    Nodo* padre;
    
    Nodo(string n, int t) {
        nombre = n;
        tipo = t;
        fechaCreacion = time(0);
        fechaModificacion = time(0);
        padre = nullptr;
    }
    
    virtual ~Nodo() {}
    
    virtual bool esCarpeta() {
        return tipo == 0;
    }
    
    virtual bool esArchivo() {
        return tipo == 1;
    }
    
    virtual string obtenerRuta() {
        if (padre == nullptr) {
            return "/" + nombre;
        }
        
        string ruta = "";
        Nodo* actual = this;
        
        while (actual != nullptr) {
            if (actual->padre != nullptr) {
                ruta = "/" + actual->nombre + ruta;
            } else {
                ruta = "/" + actual->nombre;
            }
            actual = actual->padre;
        }
        
        return ruta;
    }
};

struct NodoArbol {
    string nombre;
    Nodo* dato;
    NodoArbol* izq;
    NodoArbol* der;
    int altura;
    
    NodoArbol(string n, Nodo* d) {
        nombre = n;
        dato = d;
        izq = nullptr;
        der = nullptr;
        altura = 1;
    }
};

struct ArchivoTexto : Nodo {
    string contenido;
    
    ArchivoTexto(string n, string c = "", Nodo* p = nullptr) : Nodo(n, 1) {
        contenido = c;
        padre = p;
    }
    
    bool esArchivo() {
        return true;
    }
};

struct Carpeta : Nodo {
    NodoArbol* raizContenidos;
    int cantidad;
    
    int alturaArbol(NodoArbol* n) {
        if (n == nullptr) return 0;
        return n->altura;
    }
    
    int balanceArbol(NodoArbol* n) {
        if (n == nullptr) return 0;
        return alturaArbol(n->izq) - alturaArbol(n->der);
    }
    
    NodoArbol* rotarDerecha(NodoArbol* y) {
        NodoArbol* x = y->izq;
        NodoArbol* T2 = x->der;
        
        x->der = y;
        y->izq = T2;
        
        y->altura = max(alturaArbol(y->izq), alturaArbol(y->der)) + 1;
        x->altura = max(alturaArbol(x->izq), alturaArbol(x->der)) + 1;
        
        return x;
    }
    
    NodoArbol* rotarIzquierda(NodoArbol* x) {
        NodoArbol* y = x->der;
        NodoArbol* T2 = y->izq;
        
        y->izq = x;
        x->der = T2;
        
        x->altura = max(alturaArbol(x->izq), alturaArbol(x->der)) + 1;
        y->altura = max(alturaArbol(y->izq), alturaArbol(y->der)) + 1;
        
        return y;
    }
    
    NodoArbol* insertarEnArbol(NodoArbol* nodo, string nombre, Nodo* dato) {
        if (nodo == nullptr) {
            cantidad++;
            return new NodoArbol(nombre, dato);
        }
        
        if (nombre < nodo->nombre) {
            nodo->izq = insertarEnArbol(nodo->izq, nombre, dato);
        } else if (nombre > nodo->nombre) {
            nodo->der = insertarEnArbol(nodo->der, nombre, dato);
        } else {
            return nodo;
        }
        
        nodo->altura = 1 + max(alturaArbol(nodo->izq), alturaArbol(nodo->der));
        
        int balance = balanceArbol(nodo);
        
        if (balance > 1 && nombre < nodo->izq->nombre) {
            return rotarDerecha(nodo);
        }
        
        if (balance < -1 && nombre > nodo->der->nombre) {
            return rotarIzquierda(nodo);
        }
        
        if (balance > 1 && nombre > nodo->izq->nombre) {
            nodo->izq = rotarIzquierda(nodo->izq);
            return rotarDerecha(nodo);
        }
        
        if (balance < -1 && nombre < nodo->der->nombre) {
            nodo->der = rotarDerecha(nodo->der);
            return rotarIzquierda(nodo);
        }
        
        return nodo;
    }
    
    NodoArbol* buscarEnArbol(NodoArbol* nodo, string nombre) {
        if (nodo == nullptr || nodo->nombre == nombre) {
            return nodo;
        }
        
        if (nombre < nodo->nombre) {
            return buscarEnArbol(nodo->izq, nombre);
        }
        
        return buscarEnArbol(nodo->der, nombre);
    }
    
    void recorrerArbol(NodoArbol* nodo) {
        if (nodo != nullptr) {
            recorrerArbol(nodo->izq);
            cout << nodo->nombre;
            if (nodo->dato->esCarpeta()) cout << "/";
            cout << "  ";
            recorrerArbol(nodo->der);
        }
    }
    
    void liberarArbol(NodoArbol* nodo) {
        if (nodo != nullptr) {
            liberarArbol(nodo->izq);
            liberarArbol(nodo->der);
            delete nodo->dato;
            delete nodo;
        }
    }
    
    NodoArbol* nodoMinimo(NodoArbol* nodo) {
        NodoArbol* actual = nodo;
        while (actual->izq != nullptr) {
            actual = actual->izq;
        }
        return actual;
    }
    
    NodoArbol* eliminarDelArbol(NodoArbol* raiz, string nombre) {
        if (raiz == nullptr) return raiz;
        
        if (nombre < raiz->nombre) {
            raiz->izq = eliminarDelArbol(raiz->izq, nombre);
        } else if (nombre > raiz->nombre) {
            raiz->der = eliminarDelArbol(raiz->der, nombre);
        } else {
            if (raiz->izq == nullptr || raiz->der == nullptr) {
                NodoArbol* temp = raiz->izq ? raiz->izq : raiz->der;
                
                if (temp == nullptr) {
                    temp = raiz;
                    raiz = nullptr;
                } else {
                    *raiz = *temp;
                }
                
                delete temp->dato;
                delete temp;
                cantidad--;
            } else {
                NodoArbol* temp = nodoMinimo(raiz->der);
                raiz->nombre = temp->nombre;
                raiz->dato = temp->dato;
                raiz->der = eliminarDelArbol(raiz->der, temp->nombre);
            }
        }
        
        if (raiz == nullptr) return raiz;
        
        raiz->altura = 1 + max(alturaArbol(raiz->izq), alturaArbol(raiz->der));
        
        int balance = balanceArbol(raiz);
        
        if (balance > 1 && balanceArbol(raiz->izq) >= 0) {
            return rotarDerecha(raiz);
        }
        
        if (balance > 1 && balanceArbol(raiz->izq) < 0) {
            raiz->izq = rotarIzquierda(raiz->izq);
            return rotarDerecha(raiz);
        }
        
        if (balance < -1 && balanceArbol(raiz->der) <= 0) {
            return rotarIzquierda(raiz);
        }
        
        if (balance < -1 && balanceArbol(raiz->der) > 0) {
            raiz->der = rotarDerecha(raiz->der);
            return rotarIzquierda(raiz);
        }
        
        return raiz;
    }
    
    Carpeta(string n, Nodo* p = nullptr) : Nodo(n, 0) {
        raizContenidos = nullptr;
        cantidad = 0;
        padre = p;
    }
    
    ~Carpeta() {
        liberarArbol(raizContenidos);
    }
    
    bool agregar(Nodo* nuevo) {
        if (nuevo == nullptr) return false;
        
        if (buscarEnArbol(raizContenidos, nuevo->nombre) != nullptr) {
            return false;
        }
        
        nuevo->padre = this;
        
        raizContenidos = insertarEnArbol(raizContenidos, nuevo->nombre, nuevo);
        
        fechaModificacion = time(0);
        
        return true;
    }
    
    bool eliminar(string nombre) {
        NodoArbol* encontrado = buscarEnArbol(raizContenidos, nombre);
        
        if (encontrado == nullptr) {
            return false;
        }
        
        raizContenidos = eliminarDelArbol(raizContenidos, nombre);
        
        fechaModificacion = time(0);
        
        return true;
    }
    
    Nodo* buscar(string nombre) {
        NodoArbol* encontrado = buscarEnArbol(raizContenidos, nombre);
        
        if (encontrado != nullptr) {
            return encontrado->dato;
        }
        
        return nullptr;
    }
    
    bool existe(string nombre) {
        return buscarEnArbol(raizContenidos, nombre) != nullptr;
    }
    
    void listar() {
        if (raizContenidos == nullptr) {
            cout << "Vacio" << endl;
            return;
        }
        
        recorrerArbol(raizContenidos);
        cout << endl;
    }
    
    int obtenerCantidad() {
        return cantidad;
    }
    
    bool esCarpeta() {
        return true;
    }
};

void navegarHaciaRaiz(Nodo* nodo) {
    Nodo* actual = nodo;
    while (actual != nullptr) {
        cout << actual->nombre;
        if (actual->esCarpeta()) cout << "/";
        cout << " <- ";
        actual = actual->padre;
    }
    cout << "RAIZ" << endl;
}

Nodo* buscarPorRuta(Carpeta* raiz, string ruta) {
    if (ruta == "/" || ruta == "") {
        return raiz;
    }
    
    return raiz->buscar(ruta);
}

void mostrarEstructura(Nodo* nodo, int nivel = 0) {
    if (nodo == nullptr) return;
    
    for (int i = 0; i < nivel; i++) {
        cout << "  ";
    }
    
    cout << nodo->nombre;
    if (nodo->esCarpeta()) cout << "/";
    cout << endl;
}