import pygame

from pyjuego.configuracion import crear_fuente,crear_superficie_pantalla
from pyjuego.diccionarios.boton import crear_boton

pantalla = crear_superficie_pantalla()
fuente = crear_fuente(50)

def dibujar_texto_opciones(screen:pygame.surface,preguntas:dict ,pregunta_aleatoria:int) -> None:
    """ dibuja los textos de opciones de respuesta en los botones
    Args:
     screen: superficie de pygame
     preguntas: diccionario de preguntas
     pregunta_aleatoria: numero int para elejir la pregunta
    """ 
    opciones = preguntas[pregunta_aleatoria]["opciones"]
    posiciones = [(250, 330), (650, 330), (250, 430), (650, 430)]

    for i in range(4):
        fuente_opcion = fuente.render(opciones[i], True, "black")
        x, y = posiciones[i]
        screen.blit(fuente_opcion, (x, y))

def dibujar_estado(nombre:str, estado_final:bool) -> tuple:
    """ dibuja el mensaje de final de partida
    Args:
     nombre: nombre del jugador
     estado_final: booleano de estado de partida
    Returns:
     tuple: tupla de nombre y texto de fin de partida
    """ 
    nombre = fuente.render(f"Jugador: {nombre}", True, "black")
    if estado_final:
        final = fuente.render("Ganaste!", True, "black")
    else:
        final = fuente.render("Perdiste!", True, "black")

    resultado = (nombre ,final)
    return resultado

def dibujar_pregunta(pregunta:str, x:int,y:int) ->None:
    """ dibuja la pregunta en la pantalla
    Args:
     pregunta: string de texto 
     x:coordenada x de la pantalla
     y:coordenada y de la pantalla
    """ 
    texto = fuente.render(pregunta, True, "black")
    pantalla.blit(texto, (x,y))

def crear_botones_opciones(preguntas:dict,pregunta_aleatoria:int) -> list:
    """ crea los botones de respuesta para la pregunta
    Args:
     preguntas: diccionario de pregunta
     pregunta_aleatoria: numero para elejir pregunta
    Returns:
     list:lista de botones creados
    """ 
    #crea los botones donde van las respuestas
    #regresa una lista de botones
    cantidad = 4
    lista = []
    opciones = preguntas[pregunta_aleatoria]["opciones"]
    posiciones = [(280, 400), (730, 400), (280, 510), (730, 510)]
    ancho = 150
    alto = 100

    for i in range(cantidad):
        x,y = posiciones[i]
        boton = crear_boton(x,y,ancho,alto, None, opciones[i])
        lista.append(boton)
    return lista