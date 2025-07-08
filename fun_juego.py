import pygame
import random

def dibujar_boton(pantalla, rect, color, texto):
    '''
    Dibuja un botón rectangular con borde negro, relleno de un color dado y con texto centrado.

    Parámetros:
    pantalla: superficie de Pygame donde se va a dibujar el botón.
    rect: lista o tupla con las coordenadas y tamaño del botón en el formato [x, y, ancho, alto].
    color: tupla RGB con el color de fondo del botón (por ejemplo, (0, 200, 0) para verde).
    texto: cadena de caracteres que se mostrará centrada dentro del botón.
    '''
    pygame.draw.rect(pantalla, color, rect)
    pygame.draw.rect(pantalla, (0, 0, 0), rect, 2)
    fuente = pygame.font.SysFont(None, 28)
    texto_render = fuente.render(texto, True, (0, 0, 0))
    texto_rect = texto_render.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
    pantalla.blit(texto_render, texto_rect)

def dibujar_tablero(pantalla, posicion):
    ancho_casilla = 20
    alto_casilla = 20
    x_inicial = 10
    y_inicial = 10

    CANT_FILAS = 2
    CANT_COLUMNAS = 15

    fuente = pygame.font.SysFont(None, 18)
    numero = 1
    for fila in range(CANT_FILAS):
        for col in range(CANT_COLUMNAS):
            x = x_inicial + col * (ancho_casilla + 2)
            y = y_inicial + fila * (alto_casilla + 2)

            color = (200, 200, 200)
            pygame.draw.rect(pantalla, color, (x, y, ancho_casilla, alto_casilla))

            num_render = fuente.render(str(numero), True, (0, 0, 0))
            pantalla.blit(num_render, (x + 3, y + 3))

            if numero - 1 == posicion:
                pygame.draw.circle(pantalla, (255, 0, 0), (x + ancho_casilla // 2, y + alto_casilla // 2), 8)

            numero += 1



def mostrar_pregunta_pygame(pantalla, pregunta, fuente):
    '''
    Muestra en pantalla una pregunta con sus tres opciones de respuesta, formateando el texto para que no exceda cierto largo por línea.

    Parámetros:
    pantalla: superficie donde se mostrará la pregunta y opciones.
    pregunta: diccionario que contiene la pregunta y sus respuestas con claves.
    fuente: objeto de fuente de Pygame para renderizar el texto.

    Funcionamiento:
    Se divide el texto de la pregunta en líneas de hasta 50 caracteres
    Se muestran las líneas una debajo de otra 
    Luego se dibujan tres rectángulos grises para las opciones con el texto correspondiente dentro.
    Cada opción es devuelta como una tupla (letra, rectángulo) dentro de una lista.

    Retorna:
    - Una lista de tuplas asociado a una de las respuestas a, b o c.
    '''
    color_texto = (0, 0, 0)
    x = 20
    y = 80

    texto = pregunta["pregunta"]
    max_caracteres = 50
    lineas = []
    palabras = []
    palabra = ""
    


    for i in range (0,len(texto)):
        c = texto[i]
        if c != " ":
            palabra += c
        else:
            if palabra != "":
                palabras.append(palabra)
                palabra = ""
     
  
    if palabra != "":
        palabras.append(palabra)

    linea_actual = ""
    posible_linea = ""

    for palabra_actual in palabras:
        if linea_actual == "":  
            posible_linea = palabra_actual
        else:
            posible_linea = linea_actual + " " + palabra_actual

        if len(posible_linea) > max_caracteres:
            lineas.append(linea_actual)
            linea_actual = palabra_actual
        else:
            linea_actual = posible_linea

    if linea_actual != "":      
        lineas.append(linea_actual)

 
    for linea in lineas:
        render = fuente.render(linea, True, color_texto)
        pantalla.blit(render, (x, y))
        y += 25

    y += 20

    opciones = ["a", "b", "c"]
    textos = [pregunta["respuesta_a"], pregunta["respuesta_b"], pregunta["respuesta_c"]]
    rects = []

    for i in range(3):
        rect = pygame.Rect(50, y + i * 50, 500, 40)
        pygame.draw.rect(pantalla, (200, 200, 200), rect)
        texto_render = fuente.render(opciones[i] + ") " + textos[i], True, (0, 0, 0))
        pantalla.blit(texto_render, (rect.x + 10, rect.y + 10))
        rects.append((opciones[i], rect))

    
    return rects


    


def mostrar_texto_simple(pantalla, texto, fuente, color, x, y):
    '''
    Muestra un texto simple en la pantalla en la posición indicada.

    Parámetros:
    pantalla: superficie donde se dibuja el texto.
    texto: cadena de texto a mostrar.
    fuente: objeto de fuente de Pygame utilizado para renderizar el texto.
    color: color del texto.
    x: coordenada horizontal donde comienza el texto.
    y: coordenada vertical donde se dibuja el texto.
    '''
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))



def mostrar_tiempo(pantalla, tiempo_inicio_ticks, tiempo_limite_segundos):
    '''
    Muestra en pantalla el tiempo restante para responder una pregunta.

    Parámetros:
    pantalla: superficie donde se dibuja el texto.
    tiempo_inicio_ticks: tiempo (en milisegundos) al comenzar la cuenta regresiva.
    tiempo_limite_segundos: tiempo total permitido para responder (en segundos).

    Funcionamiento:
    Calcula cuántos segundos pasaron desde `tiempo_inicio_ticks`.
    Resta ese valor del tiempo límite para obtener el tiempo restante.
    Si el tiempo restante es menor a 0, lo determina a 0.
    Muestra el tiempo restante en la esquina superior derecha de la pantalla.
    '''

    negro = (0, 0, 0)
    fuente = pygame.font.SysFont(None, 30)
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido_segundos = (tiempo_actual - tiempo_inicio_ticks) / 1000
    tiempo_restante = tiempo_limite_segundos - tiempo_transcurrido_segundos
    if tiempo_restante < 0:
        tiempo_restante = 0
    texto = "Tiempo: " + str(int(tiempo_restante)) + "s"
    render = fuente.render(texto, True, negro)
    pantalla.blit(render, (450, 20))








def leer_puntajes():
    '''
    Lee el archivo "archivo.csv" y devuelve una lista de nombres y  puntajes.

    Retorna:
    - Una lista de listas con la forma [[nombre, puntaje], ...]
    '''
    archivo = open("archivo.csv", "r")
    datos = []
    for linea in archivo:
        nombre = ""
        puntaje = ""
        bandera = False
        
        for i in range (0,len(linea)):
            if not bandera:
                if linea[i] != ",":
                    nombre += linea[i]
                else:
                    bandera = True
            else:
                if linea[i] != "\n":
                    puntaje += linea[i]
            
        datos.append([nombre, str(puntaje)])
    archivo.close()
    return datos 


def ordenar_puntajes_asc(datos):

    """
    Ordena la lista de menor a mayor puntaje.
    La retorna una vez ordenada
    """
    for i in range(len(datos) - 1):
        for j in range(i + 1, len(datos)):
            if datos[i][1] > datos[j][1]:
               aux = datos[i]
               datos[i] = datos[j]
               datos[j] = aux
    return datos

def obtener_top_5(datos_ordenados):
    """
    Devuelve una lista con los primeros 5 elementos de una lista de datos ya ordenada.
    Retorna:
    Una nueva lista con los primeros 5 elementos de la lista original, o menos si no hay suficientes.


    """
    top_5 = []
    for i in range(0,5):
        top_5.append(datos_ordenados[i])

    return top_5

def finalizar_juego(estado, funcion_guardar):
    """
    Guarda el puntaje y cambia a la pantalla final con el mensaje.
    """
    funcion_guardar(estado["nombre"], estado["posicion"])
    estado["pantalla_actual"] = "fin"
    estado["resultado_final"] = f"{estado['nombre']}, terminaste en la posición {estado['posicion']}"


def reiniciar_estado_juego(estado, POS_INICIAL):
    """
    Reinicia todos los valores del estado del juego a sus condiciones iniciales.
    """
    estado["nombre"] = ""
    estado["pantalla_actual"] = "inicio"
    estado["preguntas_hechas"] = []
    estado["num_preguntas_hechas"] = 0
    estado["pregunta_actual"] = None
    estado["indice_pregunta_actual"] = -1
    estado["respuesta_seleccionada"] = ""
    estado["mostrar_feedback"] = False
    estado["respuesta_correcta"] = False
    estado["posicion"] = POS_INICIAL
    estado["resultado_final"] = ""
    estado["tiempo_feedback"] = 0


def obtener_siguiente_pregunta(estado, preguntas, funcion_buscar):
    """
    Selecciona aleatoriamente una pregunta no usada y actualiza el estado:
    Agrega el índice a estado['preguntas_hechas']
    Ajusta pregunta_actual, indice_pregunta_actual, num_preguntas_hechas
    Resetea feedback y temporizador
    """
    while True:
        valor = random.randint(0, len(preguntas) - 1)
        if funcion_buscar(valor, estado['preguntas_hechas']):
            estado['preguntas_hechas'].append(valor)
            estado['pregunta_actual'] = preguntas[valor]
            estado['indice_pregunta_actual'] = valor
            estado['num_preguntas_hechas'] = len(estado['preguntas_hechas'])
           
            estado['respuesta_seleccionada'] = ""
            estado['mostrar_feedback'] = False
            estado['respuesta_correcta'] = False
            estado['tiempo_inicio_pregunta'] = pygame.time.get_ticks()
            return
 
