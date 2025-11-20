import numpy as np
import random
import os

# Constantes Globales
CELULA_VIVA_VAL = 1 # Representación numérica para numpy
CELULA_VACIA_VAL = 0 # Representación numérica para numpy
CELULA_VIVA_CHAR = 'X' # Carácter para mostrar
CELULA_VACIA_CHAR = '.' # Carácter para mostrar

ARCHIVO_ENTRADA_ACA = 'ACAENTRA'
ARCHIVO_SALIDA_ACA = 'ACASALI.TXT'
MAX_DIMENSION = 30
MIN_DIMENSION = 10

# Funciones de Ayuda

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_dimensiones(dim_str):
    """Valida y devuelve las dimensiones enteras de una cadena (n,m)"""
    try:
        n_str, m_str = dim_str.split(',')
        n = int(n_str)
        m = int(m_str)
        if MIN_DIMENSION <= n <= MAX_DIMENSION and MIN_DIMENSION <= m <= MAX_DIMENSION:
            return n, m
        else:
            print(f"Dimensiones inválidas. Deben estar entre {MIN_DIMENSION} y {MAX_DIMENSION}")
            return None, None
    except ValueError:
        print("Formato de dimensiones incorrecto. Use 'n,m' (ej. 10,10)")
        return None, None

def validar_coordenadas(coord_str, filas, columnas):
    """Valida y devuelve las coordenadas enteras de una cadena (i,j)"""
    try:
        i_str, j_str = coord_str.split(',')
        i = int(i_str)
        j = int(j_str)
        if 0 <= i < filas and 0 <= j < columnas:
            return i, j
        else:
            print(f"Coordenadas fuera de rango. Filas: 0-{filas-1}, Columnas: 0-{columnas-1}.")
            return None, None
    except ValueError:
        print("Formato de coordenadas incorrecto. Use 'i,j' (ej. 0,0)")
        return None, None

def inicializar_tablero_vacio_np(filas, columnas):
    """Crea un tablero numpy vacío de las dimensiones especificadas"""
    return np.full((filas, columnas), CELULA_VACIA_VAL, dtype=int)

# Funciones Centrales del ACA

def leer_configuracion_inicial(nombre_archivo):
    """
    Lee la configuración inicial del tablero desde un archivo de texto especificado.
    El formato del archivo es:
    Línea 1: n,m (filas, columnas)
    Líneas subsiguientes: i,j (fila, columna de una celda viva)
    """
    nombre_archivo="ACAENTRA.txt"
    print(f"\nIntentando leer la configuración inicial desde '{nombre_archivo}'...")
    try:
        with open(nombre_archivo, 'r') as f:
            lineas = f.readlines()

        if not lineas:
            print("El archivo está vacío.")
            return None, None, None

        # Leer dimensiones
        filas, columnas = validar_dimensiones(lineas[0].strip())
        if filas is None or columnas is None:
            return None, None, None

        tablero = inicializar_tablero_vacio_np(filas, columnas)

        # Leer coordenadas de celdas vivas
        for num_linea, linea in enumerate(lineas[1:], 2): # Empezar desde la línea 2 para errores
            i, j = validar_coordenadas(linea.strip(), filas, columnas)
            if i is not None and j is not None:
                tablero[i, j] = CELULA_VIVA_VAL # Acceso a elementos de numpy
            else:
                print(f"Advertencia: Ignorando línea {num_linea} por formato o coordenadas inválidas: '{linea.strip()}'")

        print(f"Configuración inicial cargada desde '{nombre_archivo}'. Dimensiones: {filas}x{columnas}")
        return tablero, filas, columnas

    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encontró")
        return None, None, None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None, None, None

def configuracion_inicial_manual():
    """
    Permite al usuario introducir manualmente las dimensiones iniciales del tablero y las coordenadas de las celdas vivas.
    """
    print("\n--- Configuración Manual del Caldo de Cultivo ---")
    filas, columnas = None, None
    while filas is None:
        dim_input = input(f"Ingrese las dimensiones del tablero (n,m, máx {MAX_DIMENSION}x{MAX_DIMENSION}): ")
        filas, columnas = validar_dimensiones(dim_input)

    tablero = inicializar_tablero_vacio_np(filas, columnas)

    print("Ingrese las coordenadas de las células vivas (i,j). Deje en blanco para terminar")
    while True:
        coord_input = input(f"Célula viva (i,j) para un tablero de {filas}x{columnas}: ")
        if not coord_input:
            break
        i, j = validar_coordenadas(coord_input, filas, columnas)
        if i is not None and j is not None:
            tablero[i, j] = CELULA_VIVA_VAL # Acceso a elementos de numpy
            print(f"Célula agregada en ({i},{j}).")

    print("Configuración manual completa.")
    return tablero, filas, columnas

def configuracion_inicial_aleatoria():
    """
    Genera una configuración inicial aleatoria de celdas vivas en el tablero.
    El usuario introduce las dimensiones y el número de celdas vivas (o una cantidad aleatoria).
    """
    print("\n--- Configuración Aleatoria del Caldo de Cultivo ---")
    filas, columnas = None, None
    while filas is None:
        dim_input = input(f"Ingrese las dimensiones del tablero (n,m, máx {MAX_DIMENSION}x{MAX_DIMENSION}): ")
        filas, columnas = validar_dimensiones(dim_input)

    tablero = inicializar_tablero_vacio_np(filas, columnas)
    total_celdas = filas * columnas

    num_celulas_vivas = -1
    while True:
        num_input = input(f"Ingrese el número de células vivas (mínimo {filas}, máximo {total_celdas}) o 'r' para aleatorio: ").lower()
        if num_input == 'r':
            num_celulas_vivas = random.randint(filas, total_celdas)
            print(f"Se generarán {num_celulas_vivas} células vivas aleatoriamente.")
            break
        try:
            num_celulas_vivas = int(num_input)
            if filas <= num_celulas_vivas <= total_celdas:
                break
            else:
                print(f"El número de células vivas debe estar entre {filas} y {total_celdas}.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número o 'r'")

    # Colocar celdas vivas aleatoriamente
    indices_planos = np.arange(total_celdas) # Array de 0 a total_celdas-1
    np.random.shuffle(indices_planos) # Mezclar los índices
    
    for i in range(num_celulas_vivas):
        idx = indices_planos[i]
        f = idx // columnas # Convertir índice plano a fila
        c = idx % columnas  # Convertir índice plano a columna
        tablero[f, c] = CELULA_VIVA_VAL # Asignar célula viva

    print(f"Configuración aleatoria completa. {num_celulas_vivas} células vivas en un tablero {filas}x{columnas}")
    return tablero, filas, columnas

def mostrar_tablero(tablero, generacion="Actual"):
    """
    Muestra el estado actual del tablero (numpy array)
    """
    if tablero is None:
        print("No hay tablero para mostrar")
        return

    print(f"\n--- Generación {generacion} ---")
    for f in range(tablero.shape[0]): # tablero.shape[0] es el número de filas
        for c in range(tablero.shape[1]): # tablero.shape[1] es el número de columnas
            char_to_print = CELULA_VIVA_CHAR if tablero[f, c] == CELULA_VIVA_VAL else CELULA_VACIA_CHAR
            print(char_to_print, end=' ')
        print() # Nueva línea después de cada fila
    print("-" * (tablero.shape[1] * 2 + 5))

def contar_vecinos(tablero, f, c, filas, columnas):
    """
    Cuenta el número de vecinos vivos para una celda dada (f, c).
    Regla 1: Los vecinos fuera del tablero se consideran vacíos.
    """
    conteo_vecinos = 0
    for df in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if df == 0 and dc == 0:
                continue

            nf, nc = f + df, c + dc

            if 0 <= nf < filas and 0 <= nc < columnas:
                if tablero[nf, nc] == CELULA_VIVA_VAL:
                    conteo_vecinos += 1
    return conteo_vecinos

def aplicar_reglas(tablero, filas, columnas):
    """
    Aplica las reglas del Juego de la Vida para evolucionar el tablero a la siguiente generación.
    """
    nuevo_tablero = inicializar_tablero_vacio_np(filas, columnas)

    for f in range(filas):
        for c in range(columnas):
            celda_actual_esta_viva = (tablero[f, c] == CELULA_VIVA_VAL)
            vecinos_vivos = contar_vecinos(tablero, f, c, filas, columnas)

            if celda_actual_esta_viva:
                # REGLA 1: Muere por soledad (0 o 1 vecino)
                if vecinos_vivos < 2:
                    nuevo_tablero[f, c] = CELULA_VACIA_VAL
                # REGLA 2: Muere por superpoblación (4 o más vecinos)
                elif vecinos_vivos >= 4:
                    nuevo_tablero[f, c] = CELULA_VACIA_VAL
                # REGLA 3: Sobrevive (2 o 3 vecinos)
                elif 2 <= vecinos_vivos <= 3:
                    nuevo_tablero[f, c] = CELULA_VIVA_VAL
            else: # La celda actual está vacía
                # REGLA 4: Nace (exactamente 3 vecinos)
                if vecinos_vivos == 3:
                    nuevo_tablero[f, c] = CELULA_VIVA_VAL

    return nuevo_tablero

def modificar_tablero(tablero, filas, columnas):
    """
    Permite al usuario modificar el tablero actual agregando o eliminando celdas.
    """
    print("\n--- Modificar Caldo de Cultivo ---")
    while True:
        accion = input("¿Desea (a)gregar, (e)liminar una célula o (t)erminar? ").lower()
        if accion == 't':
            break

        if accion not in ['a', 'e']:
            print("Opción inválida. Por favor, elija 'a', 'e' o 't'")
            continue

        coord_input = input(f"Ingrese las coordenadas (i,j) para la acción (tablero {filas}x{columnas}): ")
        f, c = validar_coordenadas(coord_input, filas, columnas)
        if f is None or c is None:
            continue

        if accion == 'a':
            if tablero[f, c] == CELULA_VACIA_VAL:
                tablero[f, c] = CELULA_VIVA_VAL
                print(f"Célula agregada en ({f},{c})")
            else:
                print(f"La celda ({f},{c}) ya está ocupada")
        elif accion == 'e':
            if tablero[f, c] == CELULA_VIVA_VAL:
                tablero[f, c] = CELULA_VACIA_VAL
                print(f"Célula eliminada en ({f},{c})")
            else:
                print(f"La celda ({f},{c}) ya está vacía")
        mostrar_tablero(tablero, "Modificado")
    return tablero

# Funciones de Milagro (Recorridos y Aplicación)

def recorrido_espiral(filas, columnas):
    """Genera coordenadas para un recorrido en espiral."""
    ruta = []
    f_inicio, f_fin = 0, filas - 1
    c_inicio, c_fin = 0, columnas - 1

    while f_inicio <= f_fin and c_inicio <= c_fin:
        # Recorrer a la derecha
        for c in range(c_inicio, c_fin + 1):
            ruta.append((f_inicio, c))
        f_inicio += 1

        # Recorrer hacia abajo
        for f in range(f_inicio, f_fin + 1):
            ruta.append((f, c_fin))
        c_fin -= 1

        # Recorrer a la izquierda
        if f_inicio <= f_fin:
            for c in range(c_fin, c_inicio - 1, -1):
                ruta.append((f_fin, c))
            f_fin -= 1

        # Recorrer hacia arriba
        if c_inicio <= c_fin:
            for f in range(f_fin, f_inicio - 1, -1):
                ruta.append((f, c_inicio))
            c_inicio += 1
    return ruta

def recorrido_diagonal_secundaria_inferior(filas, columnas):
    """Genera coordenadas para el recorrido de la diagonal secundaria inferior."""
    ruta = []
    for suma_fc in range(columnas - 1, filas + columnas - 1):
        for f in range(filas):
            c = suma_fc - f
            if 0 <= c < columnas:
                ruta.append((f, c))
    return ruta

def recorrido_zigzag_vertical(filas, columnas):
    """Genera coordenadas para un recorrido vertical en zigzag."""
    ruta = []
    for c in range(columnas):
        if c % 2 == 0: # Columna par: de arriba a abajo
            for f in range(filas):
                ruta.append((f, c))
        else: # Columna impar: de abajo a arriba
            for f in range(filas - 1, -1, -1):
                ruta.append((f, c))
    return ruta

def aplicar_milagro(tablero, filas, columnas):
    """
    Permite al usuario aplicar uno de los tres eventos de "milagro".
    """
    print("\n--- Aplicar Milagro ---")
    print("1. Milagro 1 (Recorrido en espiral, celdas coordenadas impares (fila,columna))")
    print("2. Milagro 2 (Diagonal secundaria inferior, celdas con coordenada columna par)")
    print("3. Milagro 3 (Zigzag vertical, celdas con coordenada fila impar)")
    print("4. Volver al menú principal")

    eleccion = input("Seleccione una opción de milagro: ")

    ruta_coordenadas = []
    celdas_relevantes_conteo = 0
    celdas_vacias_en_ruta = []
    posicion_nacimiento = None

    if eleccion == '1':
        ruta_coordenadas = recorrido_espiral(filas, columnas)
        
        celdas_relevantes = [(f, c) for f, c in ruta_coordenadas if f % 2 != 0 and c % 2 != 0]
        celdas_relevantes_conteo = len(celdas_relevantes)
        requeridas_vacias = celdas_relevantes_conteo // 2

        for f, c in celdas_relevantes:
            if tablero[f, c] == CELULA_VACIA_VAL:
                celdas_vacias_en_ruta.append((f, c))
        
        print(f"Milagro 1: Celdas relevantes con coordenadas (fila,col) impares: {celdas_relevantes_conteo}")
        print(f"Celdas vacías requeridas para el milagro: {requeridas_vacias}")
        print(f"Celdas vacías encontradas en el recorrido: {len(celdas_vacias_en_ruta)}")

        if len(celdas_vacias_en_ruta) >= requeridas_vacias:
            if celdas_vacias_en_ruta:
                for f, c in ruta_coordenadas:
                    if f % 2 != 0 and c % 2 != 0 and tablero[f, c] == CELULA_VACIA_VAL:
                        posicion_nacimiento = (f, c)
                        break
                if posicion_nacimiento:
                    tablero[posicion_nacimiento[0], posicion_nacimiento[1]] = CELULA_VIVA_VAL
                    print(f"¡Milagro 1 ocurrido! Una célula ángel nació en ({posicion_nacimiento[0]},{posicion_nacimiento[1]})")
                else:
                    print("Milagro 1 no ocurrió: No se encontró una posición vacía elegible para el nacimiento")
            else:
                print("Milagro 1 no ocurrió: No hay celdas vacías en el recorrido relevante")
        else:
            print("Milagro 1 no ocurrió: No se cumple la condición de celdas vacías requeridas")

    elif eleccion == '2':
        ruta_coordenadas = recorrido_diagonal_secundaria_inferior(filas, columnas)
        
        celdas_relevantes = [(f, c) for f, c in ruta_coordenadas if c % 2 == 0]
        celdas_relevantes_conteo = len(celdas_relevantes)
        requeridas_vacias = celdas_relevantes_conteo * 7 // 10

        for f, c in celdas_relevantes:
            if tablero[f, c] == CELULA_VACIA_VAL:
                celdas_vacias_en_ruta.append((f, c))
        
        print(f"Milagro 2: Celdas relevantes con coordenada columna par: {celdas_relevantes_conteo}")
        print(f"Celdas vacías requeridas para el milagro: {requeridas_vacias}")
        print(f"Celdas vacías encontradas en el recorrido: {len(celdas_vacias_en_ruta)}")

        if len(celdas_vacias_en_ruta) >= requeridas_vacias:
            if celdas_vacias_en_ruta:
                for f, c in reversed(ruta_coordenadas):
                     if c % 2 == 0 and tablero[f, c] == CELULA_VACIA_VAL:
                        posicion_nacimiento = (f, c)
                        break
                if posicion_nacimiento:
                    tablero[posicion_nacimiento[0], posicion_nacimiento[1]] = CELULA_VIVA_VAL
                    print(f"¡Milagro 2 ocurrido! Una célula nació en ({posicion_nacimiento[0]},{posicion_nacimiento[1]})")
                else:
                    print("Milagro 2 no ocurrió: No se encontró una posición vacía elegible para el nacimiento")
            else:
                print("Milagro 2 no ocurrió: No hay celdas vacías en el recorrido relevante")
        else:
            print("Milagro 2 no ocurrió: No se cumple la condición de celdas vacías requeridas")

    elif eleccion == '3':
        ruta_coordenadas = recorrido_zigzag_vertical(filas, columnas)
        
        celdas_relevantes = [(f, c) for f, c in ruta_coordenadas if f % 2 != 0]
        celdas_relevantes_conteo = len(celdas_relevantes)
        requeridas_vacias = celdas_relevantes_conteo * 6 // 10

        for f, c in celdas_relevantes:
            if tablero[f, c] == CELULA_VACIA_VAL:
                celdas_vacias_en_ruta.append((f, c))
        
        print(f"Milagro 3: Celdas relevantes con coordenada fila impar: {celdas_relevantes_conteo}")
        print(f"Celdas vacías requeridas para el milagro: {requeridas_vacias}")
        print(f"Celdas vacías encontradas en el recorrido: {len(celdas_vacias_en_ruta)}")

        if len(celdas_vacias_en_ruta) >= requeridas_vacias:
            if celdas_vacias_en_ruta:
                indice_inicio_segunda_mitad = len(ruta_coordenadas) // 2
                se_encontro_posicion_nacimiento = False
                for idx in range(indice_inicio_segunda_mitad, len(ruta_coordenadas)):
                    f, c = ruta_coordenadas[idx]
                    if f % 2 != 0 and tablero[f, c] == CELULA_VACIA_VAL:
                        posicion_nacimiento = (f, c)
                        se_encontro_posicion_nacimiento = True
                        break
                if se_encontro_posicion_nacimiento:
                    tablero[posicion_nacimiento[0], posicion_nacimiento[1]] = CELULA_VIVA_VAL
                    print(f"¡Milagro 3 ocurrido! Una célula nació en ({posicion_nacimiento[0]},{posicion_nacimiento[1]})")
                else:
                    print("Milagro 3 no ocurrió: No se encontró una posición vacía elegible en la segunda mitad del recorrido")
            else:
                print("Milagro 3 no ocurrió: No hay celdas vacías en el recorrido relevante")
        else:
            print("Milagro 3 no ocurrió: No se cumple la condición de celdas vacías requeridas")

    elif eleccion == '4':
        print("Volviendo al menú principal")
    else:
        print("Opción inválida de milagro")

    input("\nPresione Enter para continuar...")
    return tablero

def ejecutar_simulacion(tablero, filas, columnas):
    """
    Calcula y muestra la evolución del tablero durante X generaciones,
    o hasta que no queden celdas vivas.
    """
    if tablero is None:
        print("No hay un tablero inicial configurado para la simulación")
        input("Presione Enter para continuar...")
        return None

    while True:
        try:
            generaciones_str = input("Ingrese el número de generaciones a simular (0 para solo una generación): ")
            generaciones = int(generaciones_str)
            if generaciones < 0:
                print("El número de generaciones no puede ser negativo")
            else:
                break
        except ValueError:
            print("Entrada inválida. Ingrese un número entero")

    tablero_actual = tablero.copy() # Copia del array numpy
    celulas_vivas_iniciales = np.sum(tablero_actual == CELULA_VIVA_VAL) # Contar con numpy

    if celulas_vivas_iniciales == 0:
        print("\nEl tablero inicial no tiene células vivas. No hay evolución posible")
        mostrar_tablero(tablero_actual, 0)
        input("Presione Enter para continuar...")
        return tablero_actual

    for gen in range(1, generaciones + 1):
        limpiar_pantalla()
        mostrar_tablero(tablero_actual, gen - 1)
        print(f"Simulando generación {gen} de {generaciones}...")

        siguiente_tablero = aplicar_reglas(tablero_actual, filas, columnas)
        celulas_vivas_en_siguiente_gen = np.sum(siguiente_tablero == CELULA_VIVA_VAL)

        if celulas_vivas_en_siguiente_gen == 0:
            print(f"\n¡Todas las células murieron en la generación {gen}!")
            mostrar_tablero(siguiente_tablero, gen)
            input("Presione Enter para continuar...")
            return siguiente_tablero
        
        tablero_actual = siguiente_tablero

    limpiar_pantalla()
    mostrar_tablero(tablero_actual, generaciones)
    print(f"\nSimulación completada después de {generaciones} generaciones")
    input("Presione Enter para continuar...")
    return tablero_actual

def guardar_configuracion_final(tablero, nombre_archivo):
    """
    Guarda la configuración final de las celdas vivas en un archivo de texto especificado.
    """
    if tablero is None:
        print("No hay un tablero para guardar")
        return

    try:
        with open(nombre_archivo, 'w') as f:
            celulas_vivas_encontradas = False
            # np.where devuelve las coordenadas (filas, columnas) de los elementos que cumplen la condición
            filas_vivas, cols_vivas = np.where(tablero == CELULA_VIVA_VAL)
            
            if len(filas_vivas) == 0:
                print(f"No hay células vivas en el tablero final. El archivo '{nombre_archivo}' estará vacío")
            else:
                for r, c in zip(filas_vivas, cols_vivas):
                    f.write(f"{r},{c}\n")
                celulas_vivas_encontradas = True
                print(f"Configuración final guardada exitosamente en '{nombre_archivo}'")
    except Exception as e:
        print(f"Error al guardar la configuración final en '{nombre_archivo}': {e}")
    input("Presione Enter para continuar...")

# Flujo Principal del Programa

def menu_principal():
    """
    Presenta el menú principal al usuario y maneja el flujo general del programa.
    """
    tablero_actual = None
    filas, columnas = None, None
    
    while True:
        limpiar_pantalla()
        print("\n--- AUTÓMATA CELULAR ACA ---")
        print("1. Cargar configuración inicial desde archivo (ACAENTRA.TXT)")
        print("2. Configurar tablero manualmente")
        print("3. Generar configuración aleatoria")
        print("4. Mostrar tablero actual")
        print("5. Modificar tablero (agregar/eliminar células)")
        print("6. Calcular y mostrar siguiente generación (Puntual)")
        print("7. Permitir 'Milagros'")
        print("8. Calcular y mostrar tras X generaciones")
        print("9. Guardar configuración final (ACASALI.TXT)")
        print("0. Salir de ACA")

        eleccion = input("Ingrese su opción: ")

        if eleccion == '1':
            tablero_actual, filas, columnas = leer_configuracion_inicial(ARCHIVO_ENTRADA_ACA)
            if tablero_actual is not None:
                mostrar_tablero(tablero_actual, "Inicial")
            else:
                print("No se pudo cargar la configuración")
            input("Presione Enter para continuar...")

        elif eleccion == '2':
            tablero_actual, filas, columnas = configuracion_inicial_manual()
            if tablero_actual is not None:
                mostrar_tablero(tablero_actual, "Inicial")
            input("Presione Enter para continuar...")

        elif eleccion == '3':
            tablero_actual, filas, columnas = configuracion_inicial_aleatoria()
            if tablero_actual is not None:
                mostrar_tablero(tablero_actual, "Inicial")
            input("Presione Enter para continuar...")

        elif eleccion == '4':
            if tablero_actual is not None:
                mostrar_tablero(tablero_actual, "Actual")
            else:
                print("No hay un tablero configurado. Por favor, cargue o genere uno primero")
            input("Presione Enter para continuar...")
        
        elif eleccion == '5':
            if tablero_actual is not None and filas is not None and columnas is not None:
                tablero_actual = modificar_tablero(tablero_actual, filas, columnas)
            else:
                print("No hay un tablero configurado para modificar")
            input("Presione Enter para continuar...")

        elif eleccion == '6':
            if tablero_actual is not None and filas is not None and columnas is not None:
                celulas_vivas_conteo = np.sum(tablero_actual == CELULA_VIVA_VAL)
                if celulas_vivas_conteo == 0:
                    print("No hay células vivas en el tablero para evolucionar")
                    mostrar_tablero(tablero_actual, "Actual")
                else:
                    tablero_actual = aplicar_reglas(tablero_actual, filas, columnas)
                    mostrar_tablero(tablero_actual, "Siguiente")
            else:
                print("No hay un tablero configurado para calcular la siguiente generación")
            input("Presione Enter para continuar...")

        elif eleccion == '7':
            if tablero_actual is not None and filas is not None and columnas is not None:
                tablero_actual = aplicar_milagro(tablero_actual, filas, columnas)
                mostrar_tablero(tablero_actual, "Después del Milagro")
            else:
                print("No hay un tablero configurado para aplicar milagros")
            input("Presione Enter para continuar...")

        elif eleccion == '8':
            if tablero_actual is not None and filas is not None and columnas is not None:
                tablero_actual = ejecutar_simulacion(tablero_actual, filas, columnas)
            else:
                print("No hay un tablero configurado para simular")

        elif eleccion == '9':
            guardar_configuracion_final(tablero_actual, ARCHIVO_SALIDA_ACA)

        elif eleccion == '0':
            print("Saliendo de AUTÓMATA CELULAR ACA. ¡Hasta luego!")
            break

        else:
            print("Opción inválida. Por favor, intente de nuevo")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()