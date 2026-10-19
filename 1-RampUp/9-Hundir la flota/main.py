import clases
import funciones
import time
from rich.console import Console

consola = Console()

# Mostrar instrucciones por pantalla
funciones.mostrar_instrucciones()
input("Presiona ENTER para comenzar...")

# Nombres de cada participante
nombre_humano = input("Introduce tu nombre: ")
# humano = clases.Jugador("Gran Señor de los Martes")
humano = clases.Jugador(nombre_humano)
ordenador = clases.KarmaIA("Karma IA")
print(f"\nTe recuerdo que tu adversaria es {ordenador.nombre}. ¡Buena suerte!")

# Colocación de flota de cada jugador/a
print(f"\n{nombre_humano}, coloca tu flota.\n")
humano.tablero_propio.mostrar_tablero_coordenadas()
print()

humano_flota_colocacion = humano.colocar_flota()

if humano_flota_colocacion is None:
    print("\nHas abandonado antes de empezar. ¡Hasta la próxima!\n")
    exit()

ordenador.colocar_flota()
print(f"{ordenador.nombre} ya ha colocado su flota.\n¡¡¡QUE COMIENCE LA BATALLA!!!\n")
time.sleep(2)

# Sistema de turnos y PARTIDAS
partida = 0
jugadores_ids = [humano, ordenador]
abandono = False

while humano.queda_aun_flota() and ordenador.queda_aun_flota():
    # Determinando turno
    turno_actual = partida % 2 # da siempre resultados de 0 (par) y 1 (impar)
    jugador_actual = jugadores_ids[turno_actual]
    rival = jugadores_ids[(turno_actual + 1) % 2]
    print(f"\n_____ Turno de {jugador_actual.nombre} _____\n")

    if jugador_actual == humano:
        # Para visualizar el tablero de ataque en cada turno
        print(f"\nTablero de ataque de {jugador_actual.nombre}:\n")
        jugador_actual.tablero_ataque.mostrar_tablero_coordenadas()
        print()
        # print("tablero de KARMA")
        # rival.tablero_propio.mostrar_tablero_coordenadas()

    # Pedir coordenadas de ataque
    resultado_ataque = jugador_actual.realizar_disparo()

    if resultado_ataque is None:
        print(f"\n🏳️ {jugador_actual.nombre}, has abandonado la partida. ¡Hasta la próxima!\n")
        exit()
    
    fila, columna = resultado_ataque

    # Procesar el ataque
    resultado = rival.recibir_disparo(fila, columna)
    jugador_actual.anotar_en_tablero_ataque(fila, columna, resultado)

    # Mostrar resultado
    if resultado == "impacto":
        print(f"\n💥 {jugador_actual.nombre} ha acertado en {fila}{columna}.\n")
        if jugador_actual == ordenador:
            jugador_actual.tablero_ataque.mostrar_tablero_coordenadas()
    else:
        print(f"\n💧 {jugador_actual.nombre} ha fallado en {fila}{columna}.\n")
        partida += 1
        if jugador_actual == ordenador:
            jugador_actual.tablero_ataque.mostrar_tablero_coordenadas()

    # Pausa para que la persona lea antes de que el ordenador dispare
    time.sleep(5)

if humano.queda_aun_flota():
    print(f"\n¡🏆 {humano.nombre}, has ganado la batalla!\n")
elif ordenador.queda_aun_flota():
    print(f"\n💀 ¡{humano.nombre}, has perdido contra {ordenador.nombre}! Próximamente lo hará la humanidad... \n")



