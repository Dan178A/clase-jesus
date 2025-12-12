Sí, el mensaje anterior está formateado en **Markdown** (con los títulos, negritas y bloques de código listos).

Para que te sea más fácil copiarlo y pegarlo en un archivo de texto (`.md`), Notion, Obsidian o incluso en el chat con Jesús sin perder el formato, aquí te dejo el **código fuente** completo. Solo dale a "Copiar":

````markdown
# 🚀 Misión: Proyecto Terminal Unix
**Estudiante:** Jesús Blanca
**Meta:** Crear una simulación de Linux desde cero.
**Fecha de Entrega:** Semana del 12 de Enero, 2026.

---

## 📅 PARTE 1: El Plan de Batalla (4 Fases)

Este proyecto es grande, así que no lo vamos a atacar todo de golpe. Lo dividiremos en misiones pequeñas.

### 🚩 Fase 1: Cimientos y Git (Días 1-3)
* **Vital:** Configurar **Git y GitHub** (Repositorio Privado). *Advertencia: Si no usas Git, no corrigen el proyecto*.
* **Estructura:** Definir el `struct Nodo` en C++.
* **Persistencia Inicial:** Crear el archivo `.txt` de prueba (ej: `sistema.txt`) y diseñar la función para leerlo al iniciar.

### 🚩 Fase 2: El Explorador (Días 4-7)
* **Objetivo:** Poder movernos por el sistema que cargamos.
* **Comando `ls`:** Ver qué hay en la carpeta actual.
* **Comando `cd`:** Entrar a carpetas y regresar (`cd ..`).
* **Visualización:** Que la consola muestre la ruta bonita: `/home/jesus $`.

### 🚩 Fase 3: El Constructor (Días 8-12)
* **Objetivo:** Modificar el árbol.
* **Comando `mkdir`:** Crear carpetas nuevas (Insertar nodo).
* **Comando `touch`:** Crear archivos vacíos.
* **Editor:** Poder escribir texto dentro de un archivo.

### 🚩 Fase 4: Mudanza y Guardado (Días 13-15)
* **Comando `mv`:** Mover archivos/carpetas de un lado a otro (Cambio de punteros).
* **Comando `exit`:** Al cerrar, **guardar todo** en el archivo `.txt` para que no se pierdan los datos.
* **Rutas:** Soportar rutas complejas como `cd /bin/user`.

---

## 🎓 PARTE 2: Clase 0 - Arquitectura del Sistema (Visual)

Jesús, aquí está el secreto. El PDF prohíbe usar librerías fáciles como vectores (`std::vector`). Tenemos que hacerlo a mano.

¿Cómo metemos **infinitos hijos** dentro de una carpeta si no sabemos cuántos habrá?
**Respuesta:** ¡Usando lo que más te gusta! **Listas Enlazadas**.

### 1. El Concepto Visual: Árbol General + Listas
No es un árbol binario (izq/der). Es un árbol donde cada carpeta tiene una **Lista de Hijos**.



**La Regla de Oro:**
1.  **Hijo (Vertical):** Tu primer hijo es tu "puerta de entrada" al contenido.
2.  **Hermano (Horizontal):** Tus hijos se toman de la mano uno al lado del otro.

### 2. El `struct Nodo` (Tu Bloque de Lego)
Vamos a construir esto en C++. Necesitamos saber quién es el padre (para subir), quién es el primer hijo (para bajar) y quién es el hermano (para listar).

```cpp
enum Tipo { CARPETA, ARCHIVO };

struct Nodo {
    string nombre;       // Ej: "home", "tarea.txt"
    Tipo tipo;           // ¿Es folder o archivo?
    string contenido;    // Solo si es archivo de texto
    
    // --- PUNTEROS DE NAVEGACIÓN ---
    
    Nodo* padre;         // Para poder hacer "cd .."
    
    Nodo* primerHijo;    // Puntero hacia ADENTRO (El primer elemento de la carpeta)
    
    Nodo* siguienteHermano; // Puntero hacia el LADO (El siguiente elemento en la lista)
};
````

### 3\. Visualizando los Comandos

#### 📂 Comando `ls` (Listar)

Imagina que estás parado en el nodo `HOME`.

1.  Miras a tu `primerHijo`. (Digamos que es "User").
2.  Imprimes "User".
3.  Te mueves a `User->siguienteHermano`. (Digamos que es "Docs").
4.  Imprimes "Docs".
5.  Repites hasta que el hermano sea `NULL`.
    *¡Es simplemente recorrer una lista enlazada\!*

#### 📂 Comando `mkdir` (Crear Carpeta)

Queremos crear "Musica" dentro de la carpeta actual.

1.  Creas el nodo `Nuevo` ("Musica").
2.  Vas al `primerHijo` de la carpeta actual.
3.  Recorres los hermanos hasta el final.
4.  Al último hermano le dices: `ultimo->siguienteHermano = Nuevo`.
    *¡Es insertar al final de una lista\!*

#### 📂 Comando `mv` (Mover)

Queremos mover "Foto.jpg" a la carpeta "Imágenes".

1.  **Desconectar:** Sacas a "Foto.jpg" de la lista donde está (ajustando los punteros del hermano anterior).
2.  **Conectar:** Llevas el nodo a la lista de hijos de "Imágenes" y lo pegas al final.
    *¡Es re-enlazar nodos\!*

-----

## ⚠️ Recordatorios Importantes del PDF

1.  **Visual Studio Code:** Debes compilar y programar allí.
2.  **Git es OBLIGATORIO:** "De no hacer uso de Git, no se revisará el proyecto". Tienes que hacer *commits* seguidos.
3.  **Recursividad:** Para guardar el árbol en el `.txt` al final (`exit`), necesitarás una función recursiva que recorra todo el árbol.

### 🛠️ Tu Primera Misión (Para hoy)

1.  Crea el repositorio en GitHub.
2.  Crea el `main.cpp`.
3.  Escribe el `struct Nodo` que te mostré arriba.
4.  Sube eso a GitHub ("Initial commit").

