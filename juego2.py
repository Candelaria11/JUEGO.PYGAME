import pygame
import sys
from preguntas import preguntas
from fun_juego import *
from fun_par_2 import *

pygame.init()
pygame.mixer.init()

ANCHO_VENTANA = 600
ALTO_VENTANA = 400
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Trivia Serpientes y Escaleras")

fondo = pygame.image.load("fondo.png")
fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
sonido_correcto = pygame.mixer.Sound("correct.mp3")
sonido_incorrecto = pygame.mixer.Sound("incorrecto.mp3") 

NEGRO = (0, 0, 0)
AZUL = (0, 0, 200)
VERDE = (0, 200, 0)
ROJO = (200, 0, 0)
BLANCO = (255, 255, 255)

fuente = pygame.font.SysFont(None, 28)

TIEMPO_PREGUNTA = 15
POS_INICIAL = 14
POS_FINAL = 29
TABLERO = [0, 1, 0, 0 ,0 , 3, 0 , 0 , 0, 0, 0, 1, 0 , 0, 2, 1, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 1, 0, 0]

input_rect = pygame.Rect(150, 100, 300, 40)  
boton_jugar = pygame.Rect(100, 170, 400, 40)  
boton_puntaje = pygame.Rect(100, 230, 400, 40) 
boton_salir = pygame.Rect(100, 290, 400, 40)  
boton_terminar = pygame.Rect(200, 340, 200, 40) 

estado = {
    "nombre": "",
    "pantalla_actual": "inicio",
    "pregunta_actual": None,
    "indice_pregunta_actual": -1,
    "respuesta_seleccionada": "",
    "mostrar_feedback": False,
    "respuesta_correcta": False,
    "preguntas_hechas": [],
    "num_preguntas_hechas": 0,
    "tiempo_inicio_pregunta": 0,
    "posicion": POS_INICIAL,
    "resultado_final": "",
    "tiempo_feedback": 0
}

clock = pygame.time.Clock()

while True:
    pantalla.blit(fondo, (0, 0))

    if estado["pantalla_actual"] == "inicio":
        pygame.draw.rect(pantalla, AZUL, input_rect, 2)
        x_letra = input_rect.x + 10 
        for i in estado["nombre"]:
            letra_render = fuente.render(i, True, NEGRO)
            pantalla.blit(letra_render, (x_letra, input_rect.y + 5)) 
            x_letra += 20
        pantalla.blit(fuente.render("Ingrese su nombre:", True, NEGRO), (180, 60))
        dibujar_boton(pantalla, boton_jugar, VERDE, "JUGAR")
        dibujar_boton(pantalla, boton_puntaje, AZUL, "VER PUNTAJE")
        dibujar_boton(pantalla, boton_salir, ROJO, "SALIR")

    elif estado["pantalla_actual"] == "juego":
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - estado["tiempo_inicio_pregunta"]) / 1000
 
        dibujar_tablero(pantalla, estado["posicion"])
        rects_respuestas = mostrar_pregunta_pygame(pantalla, estado["pregunta_actual"], fuente)
        mostrar_tiempo(pantalla, estado["tiempo_inicio_pregunta"], TIEMPO_PREGUNTA)
        dibujar_boton(pantalla, boton_terminar, ROJO, "TERMINAR JUEGO")
       

        if not estado["mostrar_feedback"] and tiempo_transcurrido > TIEMPO_PREGUNTA:
            estado["respuesta_seleccionada"] = " "
            estado["respuesta_correcta"] = False
            estado["mostrar_feedback"] = True
            estado["tiempo_feedback"] = pygame.time.get_ticks()
            sonido_incorrecto.play()

        elif estado["mostrar_feedback"]:
            for letra, rect in rects_respuestas:
                color = VERDE if (estado["respuesta_seleccionada"] == letra and estado["respuesta_correcta"]) else ROJO if estado["respuesta_seleccionada"] == letra else NEGRO
                pygame.draw.rect(pantalla, color, rect, 3)
            if (pygame.time.get_ticks() - estado["tiempo_feedback"]) > 2000:
                estado["posicion"] = definir_movimiento(estado["posicion"], TABLERO, estado["respuesta_correcta"])
                resultado = definir_ganar_perder(estado["posicion"], TABLERO)
                if resultado == "no" or len(estado["preguntas_hechas"]) >= len(preguntas):
                    finalizar_juego(estado, guardar_puntaje_jugador)
                else:
                    obtener_siguiente_pregunta(estado, preguntas, buscar_preguntas_hechas)

    elif estado["pantalla_actual"] == "puntaje":
        datos = leer_puntajes()
        datos_asc = ordenar_puntajes_asc(datos)
        top5 = obtener_top_5(datos_asc)
        y = 80
        pantalla.blit(fuente.render("PUNTAJES:", True, NEGRO), (220, 40))
        for jugador, puntaje in top5:
            texto = jugador + " - " + str(puntaje)
            render = fuente.render(texto, True, NEGRO)
            pantalla.blit(render, (180, y))
            y += 30
        pantalla.blit(fuente.render("ESC para volver", True, NEGRO), (350, 200))

    elif estado["pantalla_actual"] == "fin":
        mensaje = fuente.render(estado["resultado_final"], True, NEGRO)
        pantalla.blit(mensaje, (100, 180))
        pantalla.blit(fuente.render("R: Reiniciar  ESC: Salir", True, NEGRO), (180, 330))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if estado["pantalla_actual"] == "inicio":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE and len(estado["nombre"]) > 0:
                    nuevo = ""
                    for i in range(len(estado["nombre"]) - 1):
                        nuevo += estado["nombre"][i]
                    estado["nombre"] = nuevo
                else:
                    letra = evento.unicode
                    if len(estado["nombre"]) < 15:
                        estado["nombre"] += letra

            if evento.type == pygame.MOUSEBUTTONDOWN:
                
                if boton_jugar.collidepoint(evento.pos):
                    if len(estado["nombre"]) > 0:
                        obtener_siguiente_pregunta(estado, preguntas, buscar_preguntas_hechas)
                        estado["pantalla_actual"] = "juego"
                        estado["tiempo_inicio_pregunta"] = pygame.time.get_ticks()
                        estado["posicion"] = POS_INICIAL
                        estado["respuesta_seleccionada"] = ""
                        estado["mostrar_feedback"] = False
                        estado["respuesta_correcta"] = False

                elif boton_puntaje.collidepoint(evento.pos):
                    estado["pantalla_actual"] = "puntaje"

                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        elif estado["pantalla_actual"] == "juego":
            if evento.type == pygame.MOUSEBUTTONDOWN and not estado["mostrar_feedback"]:
                x, y = evento.pos
                for letra, rect in rects_respuestas:
                    if rect.collidepoint((x, y)):
                        estado["respuesta_seleccionada"] = letra
                        estado["respuesta_correcta"] = evaluar_respuesta(letra, preguntas, estado["indice_pregunta_actual"])
                        estado["mostrar_feedback"] = True
                        estado["tiempo_feedback"] = pygame.time.get_ticks()
                        if estado["respuesta_correcta"]:
                            sonido_correcto.play()
                        else:
                            sonido_incorrecto.play()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_terminar.collidepoint(evento.pos):
                   finalizar_juego(estado, guardar_puntaje_jugador)

        elif estado["pantalla_actual"] == "puntaje":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado["pantalla_actual"] = "inicio"

        elif estado["pantalla_actual"] == "fin":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    reiniciar_estado_juego(estado, POS_INICIAL)
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    pygame.display.flip()
    clock.tick(60)
