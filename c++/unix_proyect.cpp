#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <ctime>
#include <stack>
#include <vector>
#include <algorithm>

using namespace std;

// ================================
// ESTRUCTURAS BASE
// ================================

struct Nodo {
    string nombre;
    Nodo* padre;
    time_t fechaCreacion;
    
    Nodo(string n, Nodo* p = nullptr) : nombre(n), padre(p) {
        fechaCreacion = time(0);
    }
    virtual ~Nodo() {}
    virtual bool esCarpeta() const = 0;
    virtual string getContenido() const { return ""; }
    virtual void setContenido(const string&) {}
};

struct ArchivoTexto : public Nodo {
    string contenido;
    ArchivoTexto(string n, string c = "", Nodo* p = nullptr) : Nodo(n, p), contenido(c) {}
    bool esCarpeta() const override { return false; }
    string getContenido() const override { return contenido; }
    void setContenido(const string& c) override { contenido = c; }
};

// ================================
// ÁRBOL AVL PARA CONTENIDOS
// ================================

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

    NodoAVL* nodoMinimo(NodoAVL* nodo) {
        NodoAVL* actual = nodo;
        while (actual && actual->izq) actual = actual->izq;
        return actual;
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

    NodoAVL* eliminar(NodoAVL* nodo, string nombre) {
        if (!nodo) return nodo;
        if (nombre < nodo->dato->nombre)
            nodo->izq = eliminar(nodo->izq, nombre);
        else if (nombre > nodo->dato->nombre)
            nodo->der = eliminar(nodo->der, nombre);
        else {
            if (!nodo->izq || !nodo->der) {
                NodoAVL* temp = nodo->izq ? nodo->izq : nodo->der;
                if (!temp) {
                    temp = nodo;
                    nodo = nullptr;
                } else {
                    *nodo = *temp;
                }
                // Nota: Aquí solo eliminamos el NodoAVL, no el Nodo (dato) para permitir el comando 'mv'
                delete temp;
            } else {
                NodoAVL* temp = nodoMinimo(nodo->der);
                nodo->dato = temp->dato;
                nodo->der = eliminar(nodo->der, temp->dato->nombre);
            }
        }
        if (!nodo) return nodo;
        nodo->altura = 1 + max(getAltura(nodo->izq), getAltura(nodo->der));
        int balance = getBalance(nodo);
        if (balance > 1 && getBalance(nodo->izq) >= 0) return rotarDerecha(nodo);
        if (balance > 1 && getBalance(nodo->izq) < 0) {
            nodo->izq = rotarIzquierda(nodo->izq);
            return rotarDerecha(nodo);
        }
        if (balance < -1 && getBalance(nodo->der) <= 0) return rotarIzquierda(nodo);
        if (balance < -1 && getBalance(nodo->der) > 0) {
            nodo->der = rotarDerecha(nodo->der);
            return rotarIzquierda(nodo);
        }
        return nodo;
    }

    Nodo* buscar(NodoAVL* nodo, string nombre) {
        if (!nodo) return nullptr;
        if (nodo->dato->nombre == nombre) return nodo->dato;
        return (nombre < nodo->dato->nombre) ? buscar(nodo->izq, nombre) : buscar(nodo->der, nombre);
    }

    void listar(NodoAVL* nodo) {
        if (nodo) {
            listar(nodo->izq);
            cout << nodo->dato->nombre << (nodo->dato->esCarpeta() ? "/" : "") << "  ";
            listar(nodo->der);
        }
    }

    void liberar(NodoAVL* nodo) {
        if (nodo) {
            liberar(nodo->izq);
            liberar(nodo->der);
            delete nodo->dato;
            delete nodo;
        }
    }
};

// ================================
// CLASE CARPETA
// ================================

struct Carpeta : public Nodo {
    NodoAVL* contenidos;
    ArbolAVL gestionAVL;

    Carpeta(string n, Nodo* p = nullptr) : Nodo(n, p), contenidos(nullptr) {}
    ~Carpeta() { gestionAVL.liberar(contenidos); }
    
    bool esCarpeta() const override { return true; }
    void agregar(Nodo* n) { contenidos = gestionAVL.insertar(contenidos, n); n->padre = this; }
    void removerSinBorrar(string nombre) { contenidos = gestionAVL.eliminar(contenidos, nombre); }
    Nodo* buscar(string n) { return gestionAVL.buscar(contenidos, n); }
};

// ================================
// LÓGICA DE LA TERMINAL
// ================================

class Terminal {
    Carpeta* raiz;
    Carpeta* actual;
    string archivoSistema;

    void guardarRecursivo(Nodo* nodo, ofstream& file, int nivel) {
        if (!nodo) return;
        for (int i = 0; i < nivel; i++) file << "  ";
        
        if (nodo->esCarpeta()) {
            file << "D|" << nodo->nombre << endl;
            Carpeta* carp = static_cast<Carpeta*>(nodo);
            guardarDesdeAVL(carp->contenidos, file, nivel + 1);
        } else {
            file << "F|" << nodo->nombre << "|" << nodo->getContenido() << endl;
        }
    }

    void guardarDesdeAVL(NodoAVL* navl, ofstream& file, int nivel) {
        if (navl) {
            guardarDesdeAVL(navl->izq, file, nivel);
            guardarRecursivo(navl->dato, file, nivel);
            guardarDesdeAVL(navl->der, file, nivel);
        }
    }

public:
    Terminal(string archivo) : archivoSistema(archivo) {
        raiz = new Carpeta("root");
        actual = raiz;
        cargarDesdeArchivo();
    }

    ~Terminal() { guardarSistema(); }

    string getRutaFull(Nodo* n) {
        if (!n || !n->padre) return "/";
        string path = getRutaFull(n->padre);
        return path + (path == "/" ? "" : "/") + n->nombre;
    }

    Nodo* resolverRuta(string ruta) {
        if (ruta == "/" || ruta == "root") return raiz;
        if (ruta == ".") return actual;
        if (ruta == "..") return actual->padre ? actual->padre : raiz;

        stringstream ss(ruta);
        string segmento;
        Nodo* temp = (ruta[0] == '/') ? raiz : actual;

        while (getline(ss, segmento, '/')) {
            if (segmento.empty() || segmento == ".") continue;
            if (segmento == "..") {
                if (temp->padre) temp = temp->padre;
                continue;
            }
            if (temp->esCarpeta()) {
                Nodo* sig = static_cast<Carpeta*>(temp)->buscar(segmento);
                if (sig) temp = sig; else return nullptr;
            } else return nullptr;
        }
        return temp;
    }

    void cargarDesdeArchivo() {
        ifstream file(archivoSistema);
        if (!file.is_open()) return;
        
        string linea;
        stack<Carpeta*> pila;
        pila.push(raiz);

        while (getline(file, linea)) {
            if (linea.empty()) continue;
            int nivel = 0;
            while (nivel * 2 < linea.size() && linea[nivel * 2] == ' ' && linea[nivel * 2 + 1] == ' ') nivel++;
            string data = linea.substr(nivel * 2);
            
            stringstream ss(data);
            string tipo, nombre, contenido;
            getline(ss, tipo, '|');
            getline(ss, nombre, '|');
            getline(ss, contenido);

            if (nombre == "root") continue;
            while (pila.size() > nivel + 1) pila.pop();

            if (tipo == "D") {
                Carpeta* nueva = new Carpeta(nombre, pila.top());
                pila.top()->agregar(nueva);
                pila.push(nueva);
            } else {
                pila.top()->agregar(new ArchivoTexto(nombre, contenido, pila.top()));
            }
        }
        file.close();
    }

    void guardarSistema() {
        ofstream file(archivoSistema);
        if (file.is_open()) {
            guardarRecursivo(raiz, file, 0);
            file.close();
        }
    }

    void ejecutar() {
        string entrada, cmd, arg1, arg2;
        while (true) {
            cout << getRutaFull(actual) << "$ ";
            getline(cin, entrada);
            if (entrada.empty()) continue;
            stringstream ss(entrada);
            ss >> cmd;

            if (cmd == "exit") break;
            else if (cmd == "ls") { actual->gestionAVL.listar(actual->contenidos); cout << endl; }
            else if (cmd == "mkdir") { ss >> arg1; actual->agregar(new Carpeta(arg1, actual)); }
            else if (cmd == "touch") { ss >> arg1; actual->agregar(new ArchivoTexto(arg1, "", actual)); }
            else if (cmd == "cd") {
                ss >> arg1;
                Nodo* d = resolverRuta(arg1);
                if (d && d->esCarpeta()) actual = static_cast<Carpeta*>(d);
                else cout << "Ruta no valida." << endl;
            }
            else if (cmd == "mv") {
                ss >> arg1 >> arg2;
                Nodo* nOr = resolverRuta(arg1);
                Nodo* nDes = resolverRuta(arg2);
                if (nOr && nDes && nDes->esCarpeta()) {
                    static_cast<Carpeta*>(nOr->padre)->removerSinBorrar(nOr->nombre);
                    static_cast<Carpeta*>(nDes)->agregar(nOr);
                }
            }
            else if (cmd == "edit") {
                ss >> arg1;
                Nodo* n = resolverRuta(arg1);
                if (n && !n->esCarpeta()) {
                    cout << "Contenido actual: " << n->getContenido() << "\nNuevo (EOF para terminar):" << endl;
                    string full, l;
                    while(getline(cin, l) && l != "EOF") full += l + "\\n";
                    n->setContenido(full);
                }
            }
            else if (cmd == "rename") {
                ss >> arg1 >> arg2;
                Nodo* n = resolverRuta(arg1);
                if (n) n->nombre = arg2;
            }
        }
    }
};

int main() {
    Terminal term("sistema.txt");
    term.ejecutar();
    return 0;
}