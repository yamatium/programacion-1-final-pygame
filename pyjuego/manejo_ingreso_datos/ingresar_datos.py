import pygame,sys

from pyjuego.configuracion import crear_fuente,crear_superficie_pantalla,formatear_texto
from pyjuego.diccionarios.boton import *
from pyjuego.sonidos.manejo_sonido import *

def validar_ascii_letra(caracter:str)-> bool:
    """valida que el rango sea de la a a la z
    Args:
     caracter: letra a validar
    Returns:
      booleano que es true si esta validado o false si no
    """
    valor_ascii_minimo = 97
    valor_ascii_maximo = 122
    validado = valor_ascii_minimo <= ord(caracter) <= valor_ascii_maximo

    return validado

def validar_ascii_numero(caracter: str)-> bool:
    """valida que el numero sea del 0 al 9
    Args:
     caracter: numero en formato string
    Returns:
     bool: booleano que verifica la condicion
    """
    valor_ascii_minimo = 48
    valor_ascii_maximo = 57
    validado = valor_ascii_minimo <= ord(caracter) <= valor_ascii_maximo

    return validado

def validar_letra(caracter:str)-> str:
    """validacion de caracter con su valor ascii
    Args:
     caracter: letra a validar
    Returns:
     str: string verificado
    """
    resultado = ""
    if len(caracter) == 1 and validar_ascii_letra(caracter):
      resultado = caracter
    return resultado

def validar_numero(caracter: str)-> str:
    """ validacion de numero invocando a validar con ascii
    Args:
     caracter: numero a validar
    Returns:
     str: regresa el numero validado en formato string
    """
    resultado = ""
    if len(caracter) == 1 and validar_ascii_numero(caracter):
        #len(caracter) ==1 evita que flechas o no letras crasheen
        resultado = caracter
    return resultado

def dibujar_intrucciones(instrucciones:str,fuente:pygame.font.Font,pantalla:pygame.Surface) ->None:
    """dibuja las instrucciones del juego
    Args:
     instrucciones: string a dibujar
     fuente: fuente a usar
     pantalla: superficie a usar
    """
    superficie_linea = fuente.render(instrucciones, True, "black")
    pantalla.blit(superficie_linea, (250,300))

def manejo_rect_ingreso(rect:pygame.Rect,posicion:tuple) -> bool:
    """maneja la colision del rectangulo de ingreso de nombre con el mouse
    Args:
     rect: rectangulo 
     posicion: posicion (x,y) del mouse
    Returns:
     bool: booleano que verifica la colision
    """
    if rect.collidepoint(posicion): 
        texto_activo = True
    else:
        texto_activo = False
    return texto_activo


def ingreso_datos()->str:
    """pantalla de ingreso de nombre
    Returns:
     str: nombre del jugador
    """
    pantalla = crear_superficie_pantalla()
    clock = pygame.time.Clock()
    fuente = crear_fuente(50)
    fondo = pygame.image.load("pyjuego/imagenes/juego_imagenes/campo.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (1380, 920 ))

    titulo = fuente.render("Ingresa tu nombre", True, "black")
    instrucciones = "Son 4 preguntas a responder,2 intentos por pregunta para responder correctamente,espacio = pausar musica"
    texto_formateado = formatear_texto(instrucciones)

    boton_continuar = crear_boton(480, 620, 200, 70, "white", "Continuar")
    botones = [boton_continuar]
    color_nombre = lambda texto_activo: "white" if texto_activo else "darkgray" #uso de funcion lambda
    rect_ingreso = pygame.Rect(470, 100, 220, 40)
    texto_usuario = ''
    texto_activo = False
    resultado = ""
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    entrar_sonido()
                    manejar_musica()
                elif texto_activo:
                    if event.key == pygame.K_BACKSPACE:
                        texto_usuario = texto_usuario[:-1]   
                    else:
                        if len(texto_usuario) < 10 and validar_letra(event.unicode):
                            texto_usuario += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                texto_activo = manejo_rect_ingreso(rect_ingreso,event.pos)
                if colision(boton_continuar,event.pos) and len(texto_usuario) > 0:
                    resultado = texto_usuario
                    running = False 

        mx, my = pygame.mouse.get_pos()
        pantalla.blit(fondo_escalado, (-50,-100))
        pantalla.blit(titulo, (430,50))
        dibujar_intrucciones(texto_formateado,fuente,pantalla)
        dibujar_botones(botones, pantalla, (mx, my))

        pygame.draw.rect(pantalla, color_nombre(texto_activo), rect_ingreso)
        superficie_texto = fuente.render(texto_usuario, True, (0, 0, 0))
        pantalla.blit(superficie_texto, (rect_ingreso.x + 5, rect_ingreso.y + 5))

        pygame.display.flip()
        clock.tick(60) 
    return resultado