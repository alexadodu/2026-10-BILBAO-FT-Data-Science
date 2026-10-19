import string
import time
import random
import variables
from rich.console import Console

consola = Console()

class Tablero:
    """
    Clase que representa el tablero de juego de Hundir la Flota.
    
    Gestiona una matriz de celdas que pueden tener diferentes estados:
    agua, barco, impacto o fallo. Proporciona métodos para colocar barcos,
    marcar impactos/fallos y mostrar el tablero con coordenadas.
    
    Atributos:
        tamanio (int): Tamaño del tablero (número de filas y columnas)
        estados (dict): Diccionario que mapea estados a símbolos visuales
        tablero (list): Matriz 2D que almacena el estado de cada celda
    """

    def __init__(self, tamanio_cuadricula = variables.TAMANO_TABLERO):
        """
        Inicializa un nuevo tablero vacío.
        
        Argumentos:
            tamanio_cuadricula (int): Tamaño del tablero. 
                Por defecto usa TAMANO_TABLERO de variables.py
        """

        self.tamanio = tamanio_cuadricula
        self.estados = {
            variables.AGUA: "[#4C7EB6]~[/]",
            variables.BARCO: "[bold #E69029]#[/]",
            variables.FALLO: "[bold #6DCCB4]o[/]",
            variables.IMPACTO: "[bold #FE0000]x[/]"            
            # variables.AGUA: "~",
            # variables.BARCO: "#",
            # variables.FALLO: "O",
            # variables.IMPACTO: "X"
        }

        # Crear matriz vacía llena de agua
        self.tablero = []
        for i in range(self.tamanio):
            linea = []
            for j in range(self.tamanio):
                linea.append(variables.AGUA)
            self.tablero.append(linea)        


    def mostrar_tablero_coordenadas(self):
        """
        Imprime el tablero por consola con coordenadas (letras y números).
        
        Muestra una cuadrícula con:
        - Números de columna en la parte superior (1, 2, 3...)
        - Letras de fila a la izquierda (A, B, C...)
        - Símbolos que representan el estado de cada celda
        """

        # 1. Imprimir fila de arriba del tablero con los números
        numeros = "  "
        for numero in range(self.tamanio):
            numeros += f" {numero+1}"
        print(numeros)
        # consola.print(numeros, style="bold")

        # 2. Recorrer cada fila del tablero
        for indice_fila, fila in enumerate(self.tablero):
            # 3. Obtener la letra de esa fila
            letra = string.ascii_uppercase[indice_fila]
            print(f"{letra} ")

            # 4. Recorrer cada celda de la fila
            for celda in fila:
                # 5. Traducir el estado al símbolo visual
                simbolo = self.estados[celda]
                linea += f" {simbolo}"
            # 6. Imprimir línea completa
            #print(linea)
            consola.print(linea)


    def _calculo_celdas_barco(self, fila, columna, tamanio_barco, orientacion):
        """
        Calcula todas las coordenadas que ocupará un barco según su tamaño y orientación.
        
        Argumentos:
            fila (int): Índice de fila de la posición inicial
            columna (int): Índice de columna de la posición inicial
            tamanio_barco (int): Número de celdas que ocupa el barco
            orientacion (str): Dirección hacia la que se extiende el barco
                (NORTE, SUR, ESTE, OESTE)
        
        Returns:
            list: Lista de tuplas (fila, columna) con todas las posiciones del barco
        
        Nota:
            Método privado auxiliar. No valida si las coordenadas están dentro del tablero.
        """

        celdas_barco = []
        for i in range(tamanio_barco):
            if orientacion == None:     # lo será para los barcos de 1 posición
                celdas_barco.append((fila, columna))
            elif orientacion == variables.NORTE:
                celdas_barco.append((fila - i, columna))
            elif orientacion == variables.SUR:
                celdas_barco.append((fila + i, columna))
            elif orientacion == variables.OESTE:
                celdas_barco.append((fila, columna - i))
            elif orientacion == variables.ESTE:
                celdas_barco.append((fila, columna + i))
        return celdas_barco


    def _celdas_dentro_tablero(self, celdas_barco):
        """
        Verifica si todas las celdas de una lista están dentro de los límites del tablero.
        
        Argumentos:
            celdas_barco (list): Lista de tuplas (fila, columna) a verificar
        
        Returns:
            bool: True si todas las celdas están dentro del tablero, False en caso contrario
        """

        for f, c in celdas_barco:
            if not (0 <= f < self.tamanio and 0 <= c < self.tamanio):
                return False
        return True


    def _celdas_en_agua(self, celdas_barco):
        """
        Verifica si todas las celdas de una lista están en estado AGUA.
        
        Argumentos:
            celdas_barco (list): Lista de tuplas (fila, columna) a verificar
        
        Returns:
            bool: True si todas las celdas están en agua, False si alguna tiene
                barco, impacto o fallo
        
        Nota:
            Método privado auxiliar. Asume que las coordenadas son válidas.
        """

        for f, c in celdas_barco:
            if self.tablero[f][c] != variables.AGUA:
                return False
        return True


    def _celdas_adyacentes_libres(self, celdas_barco):
        """
        Verifica que no haya barcos en las celdas adyacentes a un barco.
        
        Calcula todas las celdas adyacentes (8 direcciones) a las celdas del barco
        y comprueba que ninguna contenga otro barco. Las celdas fuera del tablero
        se consideran válidas (es el borde).
        
        Argumentos:
            celdas_barco (list): Lista de tuplas (fila, columna) que ocupa el barco
        
        Returns:
            bool: True si todas las celdas adyacentes están libres (agua o fuera del tablero),
                False si hay un barco en alguna celda adyacente
        """

        # Genera todas las celdas adyacentes al barco (8 direcciones)
        celdas_adyacentes = set()
        for f, c in celdas_barco:
            for f_ady in [-1, 0, 1]:
                for c_ady in [-1, 0, 1]:
                    # Excluir la celda central (la propia celda del barco)
                    if f_ady != 0 or c_ady != 0:
                        celdas_adyacentes.add((f + f_ady, c + c_ady))

        # Quitar las celdas que corresponden al propio barco (no son adyacentes)
        celdas_adyacentes -= set(celdas_barco)

        # Comprobar si las celdas adyacentes están en agua o fuera del tablero
        for f, c in celdas_adyacentes:
            # Solo verificar celdas dentro del tablero
            if 0 <= f < self.tamanio and 0 <= c < self.tamanio:
                if self.tablero[f][c] == variables.BARCO:
                    return False
        return True


    def colocar_barco(self, fila, columna, tamanio_barco, orientacion):
        """
        Coloca un barco en el tablero en la posición y orientación especificadas.
        
        Realiza todas las validaciones necesarias antes de colocar el barco:
        - Coordenadas válidas
        - Orientación válida (para barcos de más de 1 posición)
        - El barco no se sale del tablero
        - No hay otros barcos en las mismas celdas
        - No hay barcos en celdas adyacentes (respetando distancia de seguridad)
        
        Argumentos:
            fila (str): Letra de la fila (A-J para tablero de 10)
            columna (int): Número de la columna (1-10 para tablero de 10)
            tamanio_barco (int): Tamaño del barco (1, 2, 3 o 4 posiciones)
            orientacion (str): Dirección hacia la que se extiende
                (NORTE, SUR, ESTE, OESTE). Ignorado para barcos de 1 posición.
        
        Returns:
            tuple: (exito, mensaje) donde:
                - exito (bool): True si el barco se colocó correctamente, False si hubo error
                - mensaje (str): Descripción del resultado o error
        
        Nota:
            Si el barco es de 1 posición, la orientación no importa.
        """

        try:
            # Conversión de coordenadas de usuario a índices de matriz
            fila_conv = string.ascii_uppercase.index(fila.upper())
            columna_conv = columna - 1

            # Validación de orientación solo para barcos de más de 1 posición
            if tamanio_barco > 1:
                if orientacion not in [variables.NORTE, variables.SUR, variables.ESTE, variables.OESTE]:
                    return (False, "Orientación inválida")

            # Cálculo de las celdas que ocupará el barco
            celdas_barco = self._calculo_celdas_barco(fila_conv, columna_conv, tamanio_barco, orientacion)

            # Comprobación de que todas las celdas están dentro del tablero
            if not self._celdas_dentro_tablero(celdas_barco):
                return (False, "El barco se sale del tablero.")

            # Comprobación de que las celdas están en agua (no hay otro barco)
            if not self._celdas_en_agua(celdas_barco):
                return (False, f"Ya hay un barco en esa posición.")
               
            # Comprobación de que no hay barcos en celdas adyacentes
            if not self._celdas_adyacentes_libres(celdas_barco):
                return (False, "Hay un barco demasiado cerca.")             

            # Colocar el barco en todas las celdas calculadas
            for f, c in celdas_barco:
                self.tablero[f][c] = variables.BARCO
            return (True, "Barco colocado con éxito.")
        
        except (ValueError, TypeError):
            return (False, f"Coordenadas {fila}{columna} incorrectas.")


    def marcar_impacto(self, fila, columna):
        """
        Marca una celda del tablero como impacto (disparo acertado).
        
        Argumentos:
            fila (str): Letra de la fila (A-J para tablero de 10)
            columna (int): Número de la columna (1-10 para tablero de 10)
        
        Returns:
            bool: True si se marcó correctamente, False si las coordenadas son inválidas
        
        Nota:
            No verifica si realmente hay un barco en esa posición (se verfica antes de llamar al método).
            Solo cambia el estado de la celda a IMPACTO.
        """
        try:
            # Conversión de coordenadas
            fila = string.ascii_uppercase.index(fila.upper())
            columna = columna - 1
            
            # Validación de que está dentro del tablero
            if fila in range(self.tamanio) and columna in range(self.tamanio):
                self.tablero[fila][columna] = variables.IMPACTO
                return True
            else:
                return False
        except (ValueError, TypeError):
            return False


    def marcar_fallo(self, fila, columna):
        """
        Marca una celda del tablero como fallo (disparo al agua).
        
        Argumentos:
            fila (str): Letra de la fila (A-J para tablero de 10)
            columna (int): Número de la columna (1-10 para tablero de 10)
        
        Returns:
            bool: True si se marcó correctamente, False si las coordenadas son inválidas
        
        Nota:
            No verifica si realmente hay agua en esa posición (se verifica antes de llamar al método).
            Solo cambia el estado de la celda a FALLO.
        """
        try:
            # Conversión de coordenadas
            fila = string.ascii_uppercase.index(fila.upper())
            columna = columna - 1
            
            # Validación de que está dentro del tablero
            if fila in range(self.tamanio) and columna in range(self.tamanio):
                self.tablero[fila][columna] = variables.FALLO
                return True
            else:
                return False
        except (ValueError, TypeError):
            return False


class Jugador:

    def __init__(self, nombre):
        self.nombre = nombre
        self.tablero_propio = Tablero()
        self.tablero_ataque = Tablero()
        self.flota = {
            variables.BARCO_1_POSICION: variables.N_BARCOS_1_POSICION,
            variables.BARCO_2_POSICIONES: variables.N_BARCOS_2_POSICIONES,
            variables.BARCO_3_POSICIONES: variables.N_BARCOS_3_POSICIONES,
            variables.BARCO_4_POSICIONES: variables.N_BARCOS_4_POSICIONES,
        }

        self.vidas = 0
        for tamanio, cantidad in self.flota.items():
            self.vidas += tamanio * cantidad

    def colocar_flota(self):
        for tamanio, cantidad in self.flota.items():
            print(f"\nColoca tu(s) {cantidad} barco(s) de {tamanio} posición/es de eslora.\n")
            for barco in range(cantidad):
                while True:
                    try:
                        fila = input("Introduce la fila (A, B, C...) o SALIR para abandonar la partida: ").upper()

                        if fila == "SALIR":
                            return None
                        
                        columna = int(input("Introduce la columna (1, 2, 3...): "))
                        orientacion = None  # para los barcos de 1 posición

                        if tamanio > 1:
                            orientacion = input("Introduce orientación del barco (N/S/E/O): ").upper()
                            
                        exito, mensaje = self.tablero_propio.colocar_barco(fila, columna, tamanio, orientacion)

                        if exito:
                            print(f"\n{mensaje}\n")
                            self.tablero_propio.mostrar_tablero_coordenadas()
                            print()
                            break
                        else:
                            print(mensaje)
                    except ValueError:
                        print("La columna debe ser un número.")
        return True

    def realizar_disparo(self):
        while True:
            try:
                fila_input = input("Introduce la fila (A, B, C...) o SALIR para abandonar la partida: ").upper()

                if fila_input == "SALIR":
                    return None
                
                columna_input = int(input("Introduce la columna (1, 2, 3...): "))

                # Conversión a índices
                fila = string.ascii_uppercase.index(fila_input.upper())
                columna = columna_input - 1

                # Accedemos al tablero para ver el estado de esta
                estado_celda = self.tablero_ataque.tablero[fila][columna]         

                # Comprobación de si ya se ha disparado en esa misma celda
                if estado_celda == variables.IMPACTO or estado_celda == variables.FALLO:
                    print(f"Ya has disparado en {fila_input}{columna_input}. Intentálo de nuevo.")
                else:
                    break

            except ValueError:
                print("Las coordenadas son incorrectas. Deben ser una letra y un número.")

            except IndexError:
                print("Las coordenadas están fuera del tablero.")
        return (fila_input, columna_input)


    def recibir_disparo(self, fila, columna):
        if self.tablero_propio.tablero[string.ascii_uppercase.index(fila.upper())][columna - 1] == variables.BARCO:
            # el método tablero.marcar_impacto() ya convierte las coordenadas, pero para comprobar el estado 
            # de si hay un barco, he hecho la conversión directamente
            self.tablero_propio.marcar_impacto(fila, columna)
            self.vidas -= 1
            return "impacto"
        else:
            self.tablero_propio.marcar_fallo(fila, columna)
            return "fallo"


    def anotar_en_tablero_ataque(self, fila, columna, respuesta):
        if respuesta == "impacto":
            self.tablero_ataque.marcar_impacto(fila, columna)
        else:
            self.tablero_ataque.marcar_fallo(fila, columna)

    def queda_aun_flota(self):
        # Devuelve True si tengo vidas, False si no
        return self.vidas > 0
pass


class KarmaIA(Jugador):
    def colocar_flota(self):
        print(f"\n{self.nombre} está colocando su flota en secreto...\n")
        time.sleep(3) # pausa para extra de realidad

        for tamanio, cantidad in self.flota.items():
            for _ in range(cantidad):
                while True:
                    # Elije de forma aleatoria fila, columna y orientación en el caso de que el barco > 1 posicion
                    fila = random.choice(string.ascii_uppercase[:variables.TAMANO_TABLERO])
                    columna = random.randint(0, variables.TAMANO_TABLERO - 1)

                    if tamanio > 1:
                        orientacion = random.choice(["N", "S", "E", "O"])
                    else:
                        orientacion = None

                    # Intenta colocar el barco
                    exito, _ = self.tablero_propio.colocar_barco(fila, columna, tamanio, orientacion)

                    # Si ha colocado el barco, sale del bucle y va con el siguiente
                    if exito:
                        break

    def realizar_disparo(self):
        # 1. determina dónde se han realizado impactos
        impactos_realizados = []

        for fila in range(self.tablero_ataque.tamanio):
            for columna in range(self.tablero_ataque.tamanio):
                if self.tablero_ataque.tablero[fila][columna] == variables.IMPACTO:
                    impactos_realizados.append((fila, columna))   

        # 2. Calcula las celdas adyacentes a los impactos (exploración)
        celdas_objetivo = []
        for f, c in impactos_realizados:
            celdas_adyacentes = [(f-1, c), (f+1, c), (f, c-1), (f, c+1)]
            for f_ady, c_ady in celdas_adyacentes:
                if 0 <= f_ady < self.tablero_ataque.tamanio and 0 <= c_ady < self.tablero_ataque.tamanio:
                    celdas_objetivo.append((f_ady, c_ady))

        # 3. Comprueba si los impactos están en línea recta (el barco de mayor tamaño es de 4)
        if len(impactos_realizados) >= 2 and len(impactos_realizados) < 4:
            
            filas = []
            columnas = []
            for f_imp, c_imp in impactos_realizados:
                filas.append(f_imp)
                columnas.append(c_imp)

            # Comprueba si están en horizontal, es decir, misma fila
            objetivos = []
            if len(set(filas)) == 1:
                for f_obj, c_obj in celdas_objetivo:
                    if f_obj == filas[0]:
                        objetivos.append((f_obj, c_obj))

            # Comprueba si están en vertical, es decir, misma columna
            elif len(set(columnas)) == 1:
                for f_obj, c_obj in celdas_objetivo:
                    if c_obj == columnas[0]:
                        objetivos.append((f_obj, c_obj))

            if objetivos:
                celdas_objetivo = objetivos
            
        celdas_filtradas = []
        for f_tab, c_tab in celdas_objetivo:
            # comprueba que es agua
            if self.tablero_ataque.tablero[f_tab][c_tab] == variables.AGUA:
                celdas_filtradas.append((f_tab,c_tab))

        celdas_objetivo = celdas_filtradas

        # 4. Decidir ataque
        if celdas_objetivo:
            fila_obj, col_obj = random.choice(celdas_objetivo)
        else:
            while True:
                # Elije de forma aleatoria fila y columna
                fila_obj = random.randint(0, variables.TAMANO_TABLERO - 1)
                col_obj = random.randint(0, variables.TAMANO_TABLERO - 1)

                # Accede al tablero para ver el estado de esta
                estado_celda = self.tablero_ataque.tablero[fila_obj][col_obj]         

                # Comprobación de si ya se ha disparado en esa misma celdaS
                if estado_celda == variables.AGUA:
                    break

        fila_objetivo = string.ascii_uppercase[fila_obj]
        columna_objetivo = col_obj + 1

        return (fila_objetivo, columna_objetivo)


                
