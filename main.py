
from funciones import *
from excepciones import *

if __name__ == "__main__":
    
    vaciar_pantalla()
    print("=================================")
    print("      HUNDIR LA FLOTA     ")
    print("=================================")

    opcion = ""
    partida_cargada = False
    
    while opcion != "1" and opcion != "2":
        print("1. Nueva Partida.")
        print("2. Cargar Partida.")
        opcion = input("Elige una opción: ")

    tablero_jugador1 = []
    tablero_jugado2 = []
    turno_inicial = "JUGADOR 1"

    if opcion == "2":
        try:
            tablero_jugador1, tablero_jugado2, turno_inicial, filas, columnas = cargar_partida()
            print(f"Partida recuperada, turno de: {turno_inicial}")
            partida_cargada = True
            input("Pulsa ENTER para continuar...")
            
        except:
            print("No se econtró ninguna partida.")
            print("Se creará una partida.")
            input("Pulsa ENTER para continuar...")
            opcion = "1"
    if opcion == "1":
        filas = int(input("Número de filas: "))
        columnas = int(input("Número de colummas: "))
        num_barcos = 0
        while num_barcos < 2 or num_barcos > 5:
            try:
                entrada = input("¿Cuántos barcos (2-5)? ")
                num_barcos = int(entrada)
            except:
                print("Introduce un número válido.")

        tablero_jugador1 = crear_tablero(filas, columnas)
        tablero_jugado2 = crear_tablero(filas, columnas)
        colocacion_auto = input ("¿Quieres que se colocquen los barcos automáticamente(SI/NO)?")
        if colocacion_auto.upper() == "SI":
            colocacion_auto == True
        else:
            colocacion_auto == False

        if not colocacion_auto :
            turno_colocacion("JUGADOR 1", tablero_jugador1, num_barcos, filas, columnas)
            turno_colocacion("JUGADOR 2", tablero_jugado2, num_barcos, filas, columnas)
        else:
            turno_colocacion_auto("JUGADOR 1", tablero_jugador1, num_barcos, filas, columnas)
            turno_colocacion_auto("JUGADOR 2", tablero_jugado2, num_barcos, filas, columnas)
    partida_en_curso = True
    saltar_turno_jugador1 = False
    if partida_cargada and turno_inicial == "JUGADOR 2":
        saltar_turno_jugador1 = True

    while partida_en_curso:
        if not saltar_turno_jugador1:
            accion = turno_disparo("JUGADOR 1", tablero_jugador1, tablero_jugado2, filas, columnas)
            
            if accion == "SALIR":
                guardar_partida(tablero_jugador1, tablero_jugado2, "JUGADOR 1")
                partida_en_curso = False
                print("Guardar y salir.")
            else:
                if comprobar_victoria(tablero_jugado2):
                    ganador("JUGADOR 1")
                    partida_en_curso = False
        else:
            saltar_turno_jugador1 = False 

        if partida_en_curso:
            accion = turno_disparo("JUGADOR 2", tablero_jugado2, tablero_jugador1, filas, columnas)
            if accion == "SALIR":
                guardar_partida(tablero_jugador1, tablero_jugado2, "JUGADOR 2")
                partida_en_curso = False
                print("Guardar y salir.")
            else:
                if comprobar_victoria(tablero_jugador1):
                    ganador("JUGADOR 2")
                    partida_en_curso = False
    print() 
    print("Fin de la partida.")