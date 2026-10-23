import pygame, sys

from pyjuego.manejo_puntaje.puntuacion import guardar_puntaje
from .pantallas_juego import respuesta_correcta
from pyjuego.sonidos.manejo_sonido import entrar_sonido, manejar_musica
from pyjuego.diccionarios.resultados_juego import crear_resultados,completar_resultados,dibujar_resultados
from pyjuego.configuracion import * 
from pyjuego.diccionarios.boton import *
from pyjuego.diccionarios.cronometro import *
from .dibujar_elementos import *


def manejo_click_respuesta(botones:list,posicion:tuple)-> str:
    """devuelve el valor del boton clickeado 
    Args: 
      botones: lista de diccionarios 
      posicion: valores(x,y) del mouse
    Returns: 
      valor del boton o vacio si se clickea afuera
    """
    respuesta = ""
    for boton in botones:
        if colision(boton, posicion):
            respuesta = boton["texto"][0]#["texto"][0] saca solo a,b,c o d respectivamente
    return respuesta

def manejo_teclado_eventos(evento:pygame.event.Event) -> str:
    """manejo de eventos de teclado
    Args: 
      evento: evento keydown de pygame
    Returns: 
      accion segun evento presionado 
    """
    #manejo de eventos del teclado
    accion = ""
    if evento.key == pygame.K_ESCAPE:
        accion = "salir"
    elif evento.key == pygame.K_SPACE:
        accion = "musica"
        entrar_sonido()
        manejar_musica()
    return accion

def revisar_derrota(intentos:int, cronometro:dict,juego:bool) -> bool:
    """revisa que el jugador perdio
    Args:
     intentos: intentos restantes actuales
     cronometro: diccionario de cronometro
     juego: estado del juego
    Returns:
      booleano del estado del juego
    """
    if intentos < 1 or cronometro["tiempo_terminado"]:
        juego = True
    return juego

def guardar_puntuacion_juego(juego:bool,nombre_jugador:str,estado_final:bool,puntuacion:int)-> None:
    """guarda la puntuacion del jugador si el juego termina
    Args:
     juego: estado del juego
     nombre_jugador: nombre a guardar
     estado_final: si gano o perdio la partida
     puntuacion: puntaje del jugador
    """
    #si el juego termino guarda la puntuacion del jugador
    if juego:
      guardar_puntaje(nombre_jugador,estado_final,puntuacion)

def elegir_pregunta(preguntas:dict)-> int:
    """elije un numero al azar para una pregunta
    Args:
     preguntas: diccionario de preguntas
    Returns:
     int: numero elejido para seleccionar pregunta
    """
    total_preguntas = len(preguntas)
    numero = elejir_numero(1,total_preguntas)
    return numero

 
def jugar(nombre_jugador:str) -> dict:
    """ Ejecuta la partida del jugador y devuelve su resultado
    Args:
     nombre_jugador: nombre del jugador 
    Returns: 
     diccionario con los resultados del jugador
    """
    pantalla = crear_superficie_pantalla()
    clock = pygame.time.Clock()
    fuente = crear_fuente(50)
    fondo = pygame.image.load("pyjuego/imagenes/juego_imagenes/castle2.png").convert()
    fondo_escalado = pygame.transform.scale(fondo,(1380,920))

    # definir pregunta, opciones  y variantes
    numero_pregunta = elegir_pregunta(preguntas)
    pregunta_formateada = formatear_texto(preguntas[numero_pregunta]["pregunta"])

    juego_terminado = False
    puntuacion = 0
    preguntas_correctas = 0
    sala = 1
    intentos_por_sala = 2
    estado_final = False
    respuesta_final = ""
    resultados = crear_resultados(200,320,200,50)
    boton_salir = crear_boton(480, 610, 250,80,"white", "Salir")
    botones = crear_botones_opciones(preguntas,numero_pregunta)
    segundos_por_pregunta = 20
    cronometro = crear_cronometro(segundos_por_pregunta)

    puntuacion_actual = fuente.render(f"puntaje: {puntuacion}", True, "black")
    intentos_actual = fuente.render(f"Intentos: {intentos_por_sala}", True, "black")
    mensaje_final = fuente.render("Juego terminado", True, "black")
    victoria = lambda pregunta_correcta: True if pregunta_correcta >= 4 else False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                guardar_puntaje(nombre_jugador,estado_final,puntuacion)
                sys.exit() 
            elif event.type == pygame.KEYDOWN:
                accion = manejo_teclado_eventos(event)
                if accion =="salir":
                    if not juego_terminado:
                       guardar_puntaje(nombre_jugador,estado_final,puntuacion)
                       juego_terminado = True
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not juego_terminado:
                    respuesta_final  = manejo_click_respuesta(botones,event.pos)
                elif colision(boton_salir, event.pos):
                    running = False

        pantalla.blit(fondo_escalado, (-50,-100))
        mx, my = pygame.mouse.get_pos()
        actualizar_tiempo(cronometro)
        
        if not juego_terminado:
            # --- pantalla de cuestionario ---
                dibujar_pregunta(pregunta_formateada,400,50)
                dibujar_botones(botones,pantalla, (mx,my))
                dibujar_cronometro(cronometro,pantalla)
                
                if respuesta_final == preguntas[numero_pregunta]["respuesta"]:
                    puntuacion += preguntas[numero_pregunta]["valor_puntaje"]
                    preguntas_correctas += 1
                    respuesta_final = ""
                    respuesta_correcta()
                    puntaje_total = puntuacion
                    completar_resultados(resultados,sala,preguntas[numero_pregunta]["valor_puntaje"],puntaje_total)

                    #victoria = lambda preguntas_correctas: True if preguntas_correctas >= 4 else False #lambda
                    if victoria(preguntas_correctas): #revisar lambda
                        juego_terminado = True
                        estado_final = True
                    else:   
                        numero_pregunta = elegir_pregunta(preguntas)
                        pregunta_formateada = formatear_texto(preguntas[numero_pregunta]["pregunta"])
                        botones = crear_botones_opciones(preguntas, numero_pregunta)
                        intentos_por_sala = 2
                        sala +=1
                        resetear_cronometro(cronometro)
                #poner en funcion
                elif respuesta_final != "":
                   intentos_por_sala -= 1
                   respuesta_final = ""

                juego_terminado = revisar_derrota(intentos_por_sala,cronometro,juego_terminado)
                guardar_puntuacion_juego(juego_terminado,nombre_jugador,estado_final,puntuacion)
                puntuacion_actual = fuente.render(f"puntaje: {puntuacion}", True, "black")
                intentos_actual = fuente.render(f"Intentos: {intentos_por_sala}", True, "black")  
                pantalla.blit(puntuacion_actual, (2, 400))
                pantalla.blit(intentos_actual,(2,100))

        else:
            pantalla.blit(mensaje_final, (480,50))
            resultado_jugador = dibujar_estado(nombre_jugador,estado_final)
            pantalla.blit(resultado_jugador[0], (500,100))
            pantalla.blit(resultado_jugador[1], (540,180))
            dibujar_resultados(resultados,pantalla)
            dibujar_botones(boton_salir, pantalla, (mx, my))
               
        pygame.display.flip()
        clock.tick(60)

    resultados_jugador = {"nombre": nombre_jugador, "puntuacion": puntuacion, "salas": sala, "gano": estado_final}
    return resultados_jugador

