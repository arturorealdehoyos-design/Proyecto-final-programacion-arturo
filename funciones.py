from excepciones import *
import random
AGUA = "··"
BARCO = "##"
TOCADO = "**"
HUNDIDO = "!!"
AGUA_DISPARO = "++"

def crear_tablero (filas: int, columnas: int)->list[list]:
    """Vamos a crear el tablero personalizado por el usuario. Por ejemplo:
    Columnas=10; Filas=10 --> ['····················', '····················', '····················', '····················', '····················', '····················', '····················', '····················', '····················', '····················']"""
    tablero = []
    i = 0
    while i < filas:
        fila = [AGUA] * columnas
        tablero.append(fila)
        i +=1
    return tablero

def vaciar_pantalla ():
    """Va a simular el borrado de pantalla ya que no hemos visto ninguna función que nos ayude a hacerlo."""
    print("\n" * 50)

def genrador_cabecero_tablero (columnas:int)->str:
    """Esta función recoge el núemro de columnas que hay y va a poner en el margen del tablero que letras son. 
    Por ejemplo: columanas: 10--> cabecera = "  1  2  3  4  5  6  7  8  9  10  """
    cabecera = " "
    for i in range(columnas):
        numero = i + 1
        if numero < 10:
            cabecera += "  " + str(numero)
        else:
            cabecera += " " + str(numero)
            
    return cabecera

def imprimir_tableros (tablero_usuario: list, tablero_oponente: list):
    """Imprime los dos tableros en tamaño real. No devuelve nada.
      Ejemplo: columnas = 5 y filas = 5:
                USUARIO                 OPONENTE
              1  2  3  4  5           1  2  3  4  5
            A ·· ·· ·· ·· ··        A ·· ·· ·· ·· ··
            B ·· ·· ·· ·· ··        B ·· ·· ·· ·· ··
            C ·· ·· ·· ·· ··        C ·· ·· ·· ·· ··
            D ·· ·· ·· ·· ··        D ·· ·· ·· ·· ··
            E ·· ·· ·· ·· ··        E ·· ·· ·· ·· ··"""
    
    filas = len(tablero_usuario)
    columnas = len(tablero_usuario[0])
    cabecera = genrador_cabecero_tablero(columnas)
    print("            USUARIO                           OPONENTE            ")
    print(cabecera, "       ", cabecera)
    for i in range(filas):
        fila_usuario = "" 
        for casilla in tablero_usuario[i]:
            fila_usuario += casilla + " " 
        fila_oponente = ""
        for casilla in tablero_oponente[i]:
            fila_oponente += casilla + " "
        letra = chr(65 + i) 
        print(f" {letra} {fila_usuario}       {letra} {fila_oponente}")

def transformar_coordenada(coordenada: str, filas_totales: int, columnas_totales: int) -> tuple[int, int]:
    """
    La función recibe 'A1' y devuelve la tupla (0, 0) si existe.
    Para saber si es correcto el la información que recibe la función:
      1. intentamos convertir a número entero la coordenada en la posición 0 (letra); lanza una excepción en caso de error.
      2. veemos si la columna es menor a 0 o mayor que el número total de columnas    """
    coord = coordenada.strip()
    coord = coordenada.upper()
    
    if len(coord) < 2:
        raise ErrorCordenada("Formato no válido (Letra+Número).")

    letra = coord[0]      
    numero_str = coord[1:] 
    fila = ord(letra) - 65
    if fila < 0 or fila >= filas_totales:
        raise ErrorCordenada(f"La fila '{letra}' no existe en el tablero.")

    try:
        numero = int(numero_str)
        columna = numero - 1 
    except ValueError:
        raise ErrorCordenada("La columna tiene que ser un número.")
    if columna < 0 or columna >= columnas_totales:
        raise ErrorCordenada(f"La columna '{numero_str}' no entra en el tablero.")

    return fila, columna

def validar_barco(tablero: list[list[str]], fila: int, columna: int, tamano: int, orientacion: str) -> bool:
    """Comprueba si el barco cabe en el tablero. Devuelve un True si está bien o un False si no cabe o se choca contra otro"""
    filas_totales = len(tablero)
    columnas_totales = len(tablero[0])
    for i in range(tamano):
        if orientacion == 'H':
            fila_actual = fila
            columna_actual = columna + i
        else:
            fila_actual = fila + i
            columna_actual = columna
        if fila_actual >= filas_totales or columna_actual >= columnas_totales:
            raise ErrorBarconocabe("El barco se sale del tablero.")
        if tablero[fila_actual][columna_actual] != AGUA:
            raise ErrorBarconocabe("El barco choca con otro.")
    return True


def colocar_barco(tablero: list[list[str]], fila:int, columna:int, tamano:int, orientacion:str)-> list[list[str]]:
    """La función va a recibir la fila, la columna y el tamaño del barco y su orientación, comprueba si cabe con la función anterior y si cabe le va a pintar y devuelve el tablero con el barco ya pintado."""
    validar_barco(tablero, fila, columna, tamano, orientacion)
    i = 0
    while i < tamano:
        if orientacion == 'H':
            tablero[fila][columna + i] = BARCO
        else:
            tablero[fila + i][columna] = BARCO
        i += 1
    return tablero

def buscar_barco(tablero: list[list[str]], fila: int, columna: int) -> list:
    """Esta función busca en qué coordenadas está el barco"""
    coordenadas = []
    max_filas = len(tablero)
    max_columnas = len(tablero[0])
    horizontal = False
    if columna > 0 and tablero[fila][columna-1] in [BARCO, TOCADO, HUNDIDO]:
        horizontal = True
    elif columna < max_columnas - 1 and tablero[fila][columna+1] in [BARCO, TOCADO, HUNDIDO]:
        horizontal = True
    if horizontal:
        i = columna
        while i >= 0 and tablero[fila][i] in [BARCO, TOCADO, HUNDIDO]:
            coordenadas.append((fila, i))
            i -= 1
        i = columna + 1 
        while i < max_columnas and tablero[fila][i] in [BARCO, TOCADO, HUNDIDO]:
            coordenadas.append((fila, i))
            i += 1
    else:
        i = fila
        while i >= 0 and tablero[i][columna] in [BARCO, TOCADO, HUNDIDO]:
            coordenadas.append((i, columna))
            i -= 1
        i = fila + 1
        while i < max_filas and tablero[i][columna] in [BARCO, TOCADO, HUNDIDO]:
            coordenadas.append((i, columna))
            i += 1  
    return coordenadas

def disparar(tablero: list[list[str]], fila: int, col: int) -> str:
    """
    La función mira si hay barco ene sa coordenada, dependiendo de si es agua o barco, pues se muestra un mensaje u otro.
    Si la coordeandad es barco, mira a ver si es tocado o hundido.
    Se devuelve dependiendo de lo anterior: "Agua", "Tocado", "Hundido" o "Repetido".
    """

    casilla = tablero[fila][col]
    if casilla == AGUA:
        tablero[fila][col] = AGUA_DISPARO
        return "Agua"
    elif casilla in [AGUA_DISPARO, TOCADO, HUNDIDO]:
        return "Repetido"
    elif casilla == BARCO:
        tablero[fila][col] = TOCADO
        partes_barco = buscar_barco(tablero, fila, col)
        esta_hundido = True
        for f, c in partes_barco:
            tablero_fila = tablero[f]
            if tablero_fila[c] == BARCO:
                esta_hundido = False 
        if esta_hundido:
            for f, c in partes_barco:
                tablero_fila[c] = HUNDIDO
            return "Hundido"
        else:
            return "Tocado"   
    return "Error"

def ocultar_barco(tablero: list[list[str]])-> list[list[str]]:
    """
    Esta función crea un tablero ocultando los barcos. Devuelve un tablero oculto. Ejemplo: 

 ·· ## ·· ·· ·· ·· ## ## ## ··        ·· ·· ·· ·· ·· ·· ·· ·· ·· ··
 ·· ## ## ·· ·· ·· ·· ·· ·· ··        ·· ·· ·· ·· ·· ·· ·· ·· ·· ··
 ·· ·· ## ·· ·· ·· ·· ·· ·· ··        ·· ·· ·· ·· ·· ·· ·· ·· ·· ··
 ·· ·· ## ·· ·· ·· ·· ·· ·· ··        ·· ·· ·· ·· ·· ·· ·· ·· ·· ··
 ·· ·· ·· ·· ·· ·· ·· ·· ·· ··   ->   ·· ·· ·· ·· ·· ·· ·· ·· ·· ··
 ·· ·· ·· ·· ·· ·· ·· ·· ·· ··        ·· ·· ·· ·· ·· ·· ·· ·· ·· ··
 ·· ·· ·· ·· ·· ·· ·· ·· ·· ··        ·· ·· ·· ·· ·· ·· ·· ·· ·· ··
 ·· ·· ·· ·· ·· ·· ·· ·· ·· ··        ·· ·· ·· ·· ·· ·· ·· ·· ·· ··
 ·· ·· ·· ·· ·· ·· ·· ·· ·· ··        ·· ·· ·· ·· ·· ·· ·· ·· ·· ··
    """

    tablero_oculto = []
    for fila in tablero:
        nueva_fila = list(fila) 
        for i in range(len(nueva_fila)):
            if nueva_fila[i] == BARCO:
                nueva_fila[i] = AGUA
        tablero_oculto.append(nueva_fila)
    return tablero_oculto

def comprobar_victoria(tablero: list[list[str]])-> bool:
    """Mita a ver si hay algún barco no hundido. Si no es así, manda un True. (Se acaba la partida)"""
    for fila in tablero:
        if BARCO in fila:
            return False 
    return True

def turno_colocacion(nombre_jugador:str, tablero_jugador:list[list[str]], num_barcos:int, filas: int, columnas: int):
    """Colocamos los barcos en el tablero y salta error si nos salimos del tablero o si no cabe el barco"""
    vaciar_pantalla()
    print("TURNO : ", nombre_jugador)
    print(f"Tienes que colocar {num_barcos} barcos.")
    input("Pulsa ENTER para empezar.")
    tamaños = []
    for i in range(num_barcos):
        tamaños.append(5 - i)
    for tam in tamaños:
        barco_puesto = False
        while not barco_puesto:
            vaciar_pantalla()
            print(f"{nombre_jugador}: Colocando barco de tamaño {tam}")
            imprimir_tableros(tablero_jugador, crear_tablero(filas, columnas))

            try:
                coord = input("Dime coordenada: ")
                ori = input("Orientación (H = Horizontal, V = Vertical): ").upper()
                f, c = transformar_coordenada(coord, filas, columnas)
                colocar_barco(tablero_jugador, f, c, tam, ori)
                barco_puesto = True
                
            except ErrorCordenada as error:
                print(f"Error: {error}")
                input("Pulsa ENTER para intentar de nuevo.") 
            except ErrorBarconocabe as error:
                print(f"Imposible: {error}")
                input("Pulsa ENTER para intentar de nuevo.") 
            except Exception as error:
                print(f"Error inesperado: {error}")
                input("Pulsa ENTER para intentar de nuevo.") 

def turno_colocacion_auto(nombre_jugador:str, tablero_jugador:list[list[str]], num_barcos:int, filas: int, columnas: int):
    """Colocamos los barcos en el tablero con la biblioteca random"""
    vaciar_pantalla()
    print("TURNO: ", nombre_jugador)
    print(f"Se colocaran automáticamente los barcos.")
    input("Pulsa ENTER para empezar.")
    tamaños = []
    for i in range(num_barcos):
        tamaños.append(5 - i)
    for tam in tamaños:
        barco_puesto = False
        while not barco_puesto:
            vaciar_pantalla()
            print(f"{nombre_jugador}: Colocando barco de tamaño {tam}")
            imprimir_tableros(tablero_jugador, crear_tablero(filas, columnas))
            numero = random.randint(1, columnas)
            numero_str = str(numero)
            letra_ord = random.randint(65, 65 + filas)
            letra = chr(letra_ord)
            try:
                coord = letra + numero_str
                ori_num = random.randint(1, 2)
                if ori_num == 1:
                    ori = "H"
                else:
                    ori = "V"
                f, c = transformar_coordenada(coord, filas, columnas)
                colocar_barco(tablero_jugador, f, c, tam, ori)
                barco_puesto = True
            except:
                pass

def turno_disparo(nombre_atacante: str, tablero_atacante: list[list[str]], tablero_defensor: list[list[str]], filas: int, columnas: int) -> None:
    """
    La función realiza el disparo del jugador.
    Muestra el tablero del que ataca y el tablero con los barcos ocultos del enemigo.
    """
    vaciar_pantalla()
    print(f"-   TURNO DE ATAQUE: {nombre_atacante}.")
    tablero_enemigo_visible = ocultar_barco(tablero_defensor)
    imprimir_tableros(tablero_atacante, tablero_enemigo_visible)
    disparo_hecho = False
    while not disparo_hecho:
        coord = input(f"\n{nombre_atacante}: introduzca coordenada de disparo(guardar partida: GUARDAR): ")
        if coord.upper() == "GUARDAR":
            return "SALIR"
        try:
            f, c = transformar_coordenada(coord, filas, columnas)
            resultado = disparar(tablero_defensor, f, c)
            if resultado == "Repetido":
                print("Ya has disparado ahí, introduzca otra coordenada.")
            else:
                vaciar_pantalla()
                tablero_enemigo_visible = ocultar_barco(tablero_defensor)
                imprimir_tableros(tablero_atacante, tablero_enemigo_visible)
                print(f"\nResultado: ¡¡ {resultado.upper()} !!")
                disparo_hecho = True
                input("Pulsa ENTER para cambiar de turno.")
        except ErrorCordenada as error:
            print(f"Error: {error}")

def ganador(nombre_ganador: str) -> None:
    """
    La función muestra el ganado, es decir, printea el ganador.
    """
    vaciar_pantalla()
    print("*" * 45)
    print(f"¡FELICIDADES {nombre_ganador}! HAS GANADO.")
    print("*" * 45)


def guardar_partida(tablero_j1: list, tablero_j2: list, turno: str):
    """
    Esta función guarda la partida en un partida.txt con la información de a quién le toca, las columas y filas que tienen los tableros y las filas del jugador 1 y 2.
"""
    with open("partida.txt", "w", encoding="UTF-8") as folder:
        folder.write(turno + "\n")

        filas_actuales = len(tablero_j1)
        columnas_actuales = len(tablero_j1[0])
        folder.write(str(filas_actuales) + "," + str(columnas_actuales) + "\n")
        i = 0
        while i < filas_actuales:
            fila = tablero_j1[i]
            texto_fila = ""
            j = 0
            while j < columnas_actuales:
                texto_fila += fila[j]
                if j < columnas_actuales - 1:
                    texto_fila += ","
                j += 1 
            
            folder.write(texto_fila + "\n")
            i += 1 
            
        i = 0
        while i < filas_actuales:
            fila = tablero_j2[i]
            texto_fila = ""
            
            j = 0
            while j < columnas_actuales:
                texto_fila += fila[j]
                if j < columnas_actuales - 1:
                    texto_fila += ","
                j += 1
            
            folder.write(texto_fila + "\n")
            i += 1
            
    print("\nPartida guardada correctamente en 'partida.txt'.")
        

def cargar_partida():
    """
    Esta función lee el archivo partida_anterior.txt sabiendo que la primera linea son los turnos y las siguiente ya las filas de los tableros.
    Devuelve tablero_j1, tablero_j2, turno
    """
    with open("partida.txt", "r", encoding="UTF-8") as folder:
        lineas = folder.readlines()
    
    turno = lineas[0].strip()
    
    dimension = lineas[1].strip().split(",")
    filas_guardadas = int(dimension[0])
    columnas_guardadas = int(dimension[1])
    tablero_j1 = []
    tablero_j2 = []
    
    linea_actual = 2
    
    i = 0
    while i < filas_guardadas:
        linea = lineas[linea_actual].strip()
        fila = linea.split(",")
        tablero_j1.append(fila)
        linea_actual += 1 
        i += 1 
        

    i = 0
    while i < filas_guardadas:
        linea = lineas[linea_actual].strip()
        fila = linea.split(",")
        tablero_j2.append(fila)
        
        linea_actual += 1
        i += 1
        
    return tablero_j1, tablero_j2, turno, filas_guardadas, columnas_guardadas
        
