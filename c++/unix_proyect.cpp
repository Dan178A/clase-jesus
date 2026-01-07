#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <ctime>

using namespace std;

// --- CLASES BASE Y ESTRUCTURAS ---

struct Nodo {
    string nombre;
    Nodo* padre;
    time_t fechaCreacion;
    
    Nodo(string n, Nodo* p = nullptr) : nombre(n), padre(p) {
        fechaCreacion = time(0);
    }
    virtual ~Nodo() {}
    virtual bool esCarpeta() const = 0;
};

struct ArchivoTexto : public Nodo {
    string contenido;
    ArchivoTexto(string n, string c = "", Nodo* p = nullptr) : Nodo(n, p), contenido(c) {}
    bool esCarpeta() const override { return false; }
};

// --- ESTRUCTURA DINÁMICA: ÁRBOL AVL ---

struct NodoAVL {
    Nodo* dato;
    NodoAVL *izq, *der;
    int altura;

    NodoAVL(Nodo* d) : dato(d), izq(nullptr), der(nullptr), altura(1) {}
};

class ArbolAVL {
    int getAltura(NodoAVL* n) { return n ? n->altura : 0; }
    int getBalance(NodoAVL* n) { return n ? getAltura(n->izq) - getAltura(n->der) : 0; }

    NodoAVL* rotarDerecha(NodoAVL* y) {
        NodoAVL* x = y->izq;
        NodoAVL* T2 = x->der;
        x->der = y;
        y->izq = T2;
        y->altura = max(getAltura(y->izq), getAltura(y->der)) + 1;
        x->altura = max(getAltura(x->izq), getAltura(x->der)) + 1;
        return x;
    }

    NodoAVL* rotarIzquierda(NodoAVL* x) {
        NodoAVL* y = x->der;
        NodoAVL* T2 = y->izq;
        y->izq = x;
        x->der = T2;
        x->altura = max(getAltura(x->izq), getAltura(x->der)) + 1;
        y->altura = max(getAltura(y->izq), getAltura(y->der)) + 1;
        return y;
    }

public:
    NodoAVL* insertar(NodoAVL* nodo, Nodo* dato) {
        if (!nodo) return new NodoAVL(dato);
        if (dato->nombre < nodo->dato->nombre)
            nodo->izq = insertar(nodo->izq, dato);
        else if (dato->nombre > nodo->dato->nombre)
            nodo->der = insertar(nodo->der, dato);
        else return nodo;

        nodo->altura = 1 + max(getAltura(nodo->izq), getAltura(nodo->der));
        int balance = getBalance(nodo);

        if (balance > 1 && dato->nombre < nodo->izq->dato->nombre) return rotarDerecha(nodo);
        if (balance < -1 && dato->nombre > nodo->der->dato->nombre) return rotarIzquierda(nodo);
        if (balance > 1 && dato->nombre > nodo->izq->dato->nombre) {
            nodo->izq = rotarIzquierda(nodo->izq);
            return rotarDerecha(nodo);
        }
        if (balance < -1 && dato->nombre < nodo->der->dato->nombre) {
            nodo->der = rotarDerecha(nodo->der);
            return rotarIzquierda(nodo);
        }
        return nodo;
    }

    Nodo* buscar(NodoAVL* nodo, string nombre) {
        if (!nodo) return nullptr;
        if (nodo->dato->nombre == nombre) return nodo->dato;
        if (nombre < nodo->dato->nombre) return buscar(nodo->izq, nombre);
        return buscar(nodo->der, nombre);
    }

    void listar(NodoAVL* nodo) {
        if (nodo) {
            listar(nodo->izq);
            cout << nodo->dato->nombre << (nodo->dato->esCarpeta() ? "/" : "") << "  ";
            listar(nodo->der);
        }
    }
    
    // Función para guardar en archivo (Recorrido Preorder)
    void guardar(NodoAVL* nodo, ofstream& file, int nivel) {
        if (nodo) {
            for(int i=0; i<nivel; i++) file << "  ";
            file << (nodo->dato->esCarpeta() ? "D|" : "F|") << nodo->dato->nombre;
            if (!nodo->dato->esCarpeta()) file << "|" << static_cast<ArchivoTexto*>(nodo->dato)->contenido;
            file << endl;
            if (nodo->dato->esCarpeta()) {
                // Lógica para bajar en la jerarquía (se implementa en la clase Carpeta)
            }
            guardar(nodo->izq, file, nivel);
            guardar(nodo->der, file, nivel);
        }
    }
};

// --- CLASE CARPETA ---

struct Carpeta : public Nodo {
    NodoAVL* contenidos;
    ArbolAVL gestionAVL;

    Carpeta(string n, Nodo* p = nullptr) : Nodo(n, p), contenidos(nullptr) {}
    bool esCarpeta() const override { return true; }

    void agregar(Nodo* n) { contenidos = gestionAVL.insertar(contenidos, n); }
    Nodo* buscar(string n) { return gestionAVL.buscar(contenidos, n); }
};

// --- TERMINAL Y LÓGICA DE RUTAS ---

class Terminal {
    Carpeta* raiz;
    Carpeta* actual;

public:
    Terminal() {
        raiz = new Carpeta("root");
        actual = raiz;
    }

    string getRutaActual(Nodo* n) {
        if (!n->padre) return "/";
        return getRutaActual(n->padre) + (n->padre->padre ? "/" : "") + n->nombre;
    }

    Nodo* resolverRuta(string ruta) {
        if (ruta == "/") return raiz;
        if (ruta == "..") return actual->padre ? actual->padre : actual;
        
        stringstream ss(ruta);
        string segmento;
        Nodo* temp = (ruta[0] == '/') ? raiz : actual; // Absoluta vs Relativa 

        while (getline(ss, segmento, '/')) {
            if (segmento.empty()) continue;
            if (temp->esCarpeta()) {
                Nodo* sig = static_cast<Carpeta*>(temp)->buscar(segmento);
                if (sig) temp = sig;
                else return nullptr;
            }
        }
        return temp;
    }

    void ejecutar() {
        string entrada, comando, arg1, arg2;
        while (true) {
            cout << getRutaActual(actual) << "$ ";
            getline(cin, entrada);
            stringstream ss(entrada);
            ss >> comando;

            if (comando == "exit") break;
            else if (comando == "ls") { actual->gestionAVL.listar(actual->contenidos); cout << endl; }
            else if (comando == "mkdir") {
                ss >> arg1;
                actual->agregar(new Carpeta(arg1, actual));
            }
            else if (comando == "touch") {
                ss >> arg1;
                actual->agregar(new ArchivoTexto(arg1, "", actual));
            }
            else if (comando == "cd") {
                ss >> arg1;
                Nodo* destino = resolverRuta(arg1);
                if (destino && destino->esCarpeta()) actual = static_cast<Carpeta*>(destino);
                else cout << "Ruta no valida." << endl;
            }
        }
    }
};

int main() {
    Terminal term;
    term.ejecutar();
    return 0;
}