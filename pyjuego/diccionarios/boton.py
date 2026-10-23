import pygame

from pyjuego.configuracion import crear_fuente

def crear_superficie_texto(texto:str, fuente: pygame.font.Font) -> pygame.Surface:
    """crea un texto con superficie para usar
    Args:
     texto: texto a usar
     fuente: fuente a usar con el
    Returns:
     pygame.Surface: superficie con texto
    """
    texto_superficie = fuente.render(texto, True, "black")
    return texto_superficie

def crear_rectangulo(x:int, y:int, ancho:int, alto:int) -> pygame.Rect:
    """ crea el rectangulo de un boton
    Args:
     x: posicion x a usar 
     y: posicion y a usar
     ancho: dimension a usar
     alto: dimension a usar
    Returns:
     pygame.Rect: rectangulo de un boton
    """
    rectangulo = pygame.Rect(x, y, ancho, alto)  
    return rectangulo

def traer_rectangulo_texto(superficie:pygame.Surface, rect_boton:pygame.Rect)-> pygame.Rect:
    """ trae un rectangulo con el texto centrado
    Args:
     superficie: superficie del rectangulo a usar
     rect_boton: rectangulo del boton a usar
    Returns:
     pygame.Rect: rectangulo
    """
    texto_rectangulo = superficie.get_rect(center=rect_boton.center)
    return texto_rectangulo

def formatear_diccionario(x:int, y:int, ancho:int, alto:int, color:str, texto:str,rectangulo, superficie,texto_rectangulo)-> dict:
    """ crea un diccionario formateado para crear un boton
    Args:
     x: posicion horizontal del boton 
     y: posicion vertical del boton
     alto: ancho en pixeles
     ancho: alto en pixeles
     color: color de fondo o valor None para que sea transparente
     texto: texto del boton
     rectangulo: rectagulo del boton
     superficie: superficie del texto
     texto_rectangulo: rect con la posicion del texto centrado
    Returns:
     dict: diccionario de un boton 
    """
    boton = {}
    boton["x"] = x
    boton["y"] = y
    boton["ancho"] = ancho
    boton["alto"] = alto
    boton["color"] = color
    boton["color_constante"] = color
    boton["texto"] = texto
    boton["rectangulo"] = rectangulo
    boton["superficie"] = superficie
    boton["texto_rectangulo"] = texto_rectangulo
    return boton


def crear_boton(x:int, y:int, ancho:int, alto:int, color:str, texto:str) -> dict:
    """crea un boton con su rectangulo y texto centrado
    Args:
     x: posicion horizontal 
     y: posicion vertical
     ancho: ancho en pixeles
     alto: alto en pixeles
     color: color de fondo o None para transparencia
     texto: texto del boton
    Returns:
     dict: diccionario del boton listo para usarse 
    """
    fuente = crear_fuente(50)
    rectangulo = crear_rectangulo(x,y,ancho,alto)
    superficie_texto = crear_superficie_texto(texto, fuente)

    texto_rectangulo = traer_rectangulo_texto(superficie_texto, rectangulo)
    boton = formatear_diccionario(x, y, ancho, alto, color, texto,rectangulo, superficie_texto,texto_rectangulo)
    return boton

def colision(boton:dict,pos:tuple)-> bool:
    """regresa un booleano indicando si el mouse esta dentro del rectangulo
    Args:
     boton: diccionario del boton
     pos: posicion (x,y) del mouse 
    Returns:
      bool: true si esta dentro , false si esta afuera
    """
    return boton["rectangulo"].collidepoint(pos)

def dibujar_boton(boton:dict,color:str ,superficie:pygame.Surface)->None:
    """dibuja el fondo y texto de un boton
    Args:
     boton: diccionario de boton
     color: color de fondo
     superficie: superficie de pygame, si es None es transparente el boton
    """
    if color:
        pygame.draw.rect(superficie, color, boton["rectangulo"])
    superficie.blit(boton["superficie"], boton["texto_rectangulo"])

def boton_color_colision(boton:dict, pos:tuple) -> str | None:
    """ elije el color de un boton segun la posicion del mouse
    Args:
     boton: diccionario de boton
     pos: posicion (x,y) del mouse
    Returns:
     str: cambio de str si hay colision, none si no
    """
    return "lightblue" if colision(boton, pos) else boton["color_constante"]

def actualizar_boton(boton: dict, pantalla: pygame.Surface, mouse_pos: tuple) -> None:
    """actualiza el color del boton si hay colision
    Args:
     boton:diccionario del boton
     pantalla: superficie donde se dibuja
    """
    color = boton_color_colision(boton, mouse_pos)
    dibujar_boton(boton,color,pantalla)

def dibujar_botones(botones:list | dict, pantalla: pygame.Surface, mouse_pos: tuple)-> None:
    """dibuja una lista de botones o solo uno, revisando si es una lista
    Args:
     botones: lista de botones o solo uno
     pantalla: superficie donde se dibuja
     mouse_pos: posicion (x,y) del mouse
    """
    if type(botones) == list: 
        for boton in botones:
            actualizar_boton(boton,pantalla,mouse_pos)
    else: 
        actualizar_boton(botones,pantalla,mouse_pos)


