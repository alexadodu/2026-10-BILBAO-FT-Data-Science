def mostrar_instrucciones():
    instrucciones = """
    ==========================================
     ⚓ ¡BIENVENIDO/A A HUNDIR LA FLOTA! ⚓
    ==========================================
    
    🎯 OBJETIVO:
    Hundir todos los barcos del rival 'Karma IA' antes de que ésta hunda los tuyos.

    🧮 EL TABLERO:
    • Cuadrícula de 10x10. 
    • Filas: de la A a la J.
    • Columnas: del 1 al 10.

    🚢 TU FLOTA:
    • 1 barco de 4 casillas
    • 2 barcos de 3 casillas
    • 3 barcos de 2 casillas
    • 4 barcos de 1 casilla (submarinos)
      ⚠️ Regla de oro: ¡Los barcos no pueden tocarse entre sí (ni en diagonal)!

    ⚙️ CÓMO JUGAR:
    1. FASE DE COLOCACIÓN: Introduce fila, columna y orientación (Norte, Sur, Este, Oeste). No se pueden colocar en diagonal.
    2. FASE DE DISPARO: Introduce fila y columna para atacar al rival.
       • Impacto (X): ¡Acierto! Vuelves a disparar.
       • Agua (O): Fallo. Pasa el turno a 'Karma IA.'

    ¡Buena suerte, Almirante! 🫡
    ==========================================
    """
    print(instrucciones)

def preguntar(pregunta):
    respuesta = input(pregunta).lower().replace('í', 'i').strip()

    if respuesta == "si":
        return True
    else:
        return False