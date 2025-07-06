def pedir_nombre() -> str: 
    '''
    La funcion solicita al usuario que ingrese su nombre,
    y lo retorna
    '''
    nombre = input("ingrese su nombre: ")
    return nombre


def elegir_seguir_jugando() -> str:
    '''
    La funcion pregunta al usuario que desea seguir jugando,
    tomando solo como valido "si" y "no"(sin distinguir mayusculas) y lo retorna
    '''
    
    eleccion = input ("queres seguir jugando?  (si - no): " ).lower()
    while eleccion != "si" and eleccion != "no":
        eleccion = input("ERROR, seleccione nuevamente (si - no): ")  
    return eleccion 


def buscar_preguntas_hechas(valor:int, lista:list)-> bool:
    '''
    La funcion verifica si un valor ya fue utilizado,
    recorriendo una lista con valores ya utulizados,
    si fue encontrado retorna False, sino True
    '''
    retorno = True
    for elemento in lista:
        if valor == elemento:
         retorno = False
    

    return retorno         


def mostrar_preguntas(pregunta:list, valor:int):
  '''
  La funcion muestra en pantalla una pregunta y sus opciones
  recibe por argumento, una lista de preguntas y el indice de la pregunta a mostrar
  '''

  print("pregunta: ",pregunta[valor]["pregunta"], "\n", "Respuesta a: ",
          pregunta[valor]  ["respuesta_a"], "\n", "Respuesta b: ",
          pregunta[valor]["respuesta_b"], "\n", "Respuesta c: ",
          pregunta[valor]["respuesta_c"])
  
    
def guardar_respuesta()-> str:
    '''
    Solicita al usuario una respuesta(a,b,c)
    y retorna su respuesta
    '''
    respuesta = str(input("¿Cual es tu respuesta? (a-b-c)")).lower()
    while respuesta != "a" and respuesta != "b" and respuesta != "c":
        respuesta = str(input("ERROR,¿Cual es tu respuesta? (a-b-c)")).lower()
    return respuesta
 
 
def evaluar_respuesta(respuesta:str, pregunta:list, valor:int)-> bool:
    '''
    La funcion compara la respuesta del usuario con la respuesta corrrecta dada,
    retorna True si es verdadera, sino False
    '''
    if respuesta == pregunta[valor]["respuesta_correcta"]:
     resultado = True
    else:
        resultado = False  
        
    return resultado


def imprimir_correccion(resultado:bool):
    '''
    La funcion imprime segun si la respuesta fue correcta o no,
    retorna True si es verdadera, sino False
    '''
    if resultado:
       print("Respuesta correcta")
    else:
       print("Respuesta incorrecta") 




def definir_movimiento(pos: int, tablero: list, respuesta_correcta: bool) -> int:
    '''
    Define la nueva posición del jugador según la respuesta.
    Si es correcta, avanza; si es incorrecta, retrocede.
    
    '''

  
    if respuesta_correcta:
        nueva_pos = pos + 1
    else:
        nueva_pos = pos - 1

 
    if nueva_pos >= 0 and nueva_pos < len(tablero):
        if respuesta_correcta:
            nueva_pos = nueva_pos + tablero[nueva_pos]
        else:
            nueva_pos = nueva_pos - tablero[nueva_pos]

   
    if nueva_pos < 0:
        nueva_pos = 0
    elif nueva_pos >= len(tablero):
        nueva_pos = 30  

    return nueva_pos







def definir_ganar_perder(pos: int, tablero: list) -> str:
    '''
    La funcion evalua si el jugador ganó, perdió o sigue en juego,
    retorna "no" si gana o pierde, y "si" si continua
    '''
    if pos == 30:
        print("¡Has ganado!")
        retorno = "no"
    elif pos == 0:
        print("Has perdido!")
        retorno = "no"
    else:
        retorno = "si"
    return retorno 


def imprimir_mensaje(posicion):
    '''
    La funcion mustra la posicion final del jugador y un mensaje de fin del juego
    '''
    print("Posicion final del jugador: ", posicion ," \n FIN DEL JUEGO ") 


def imprimir_fin_preguntas(posicion):
    print("No hay mas preguntas \n Posicion final del jugador: ", posicion, " \n FIN DEL JUEGO")    

     

def guardar_puntaje_jugador(nombre:str, posicion_actual:int):
       with open("archivo.csv", "a") as archivo:
        archivo.write(f"{nombre}, {posicion_actual}\n")





        