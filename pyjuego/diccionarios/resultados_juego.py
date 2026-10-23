import pygame

from pyjuego.configuracion import crear_fuente

def crear_resultados(x:int,y:int,ancho:int,alto:int)-> dict:
    """crea un diccionario de resultados de jugador para dibujar
    Args:
     x: posicion horizontal
     y: posicion vertical
     ancho: ancho en pixeles
     alto: alto en pixeles
    Returns:
     dict: diccionario de resultados de jugador
    """
    resultados = {}
    resultados["x"] = x
    resultados["y"] = y
    resultados["ancho"] = ancho
    resultados["alto"] = alto
    resultados["columnas"] = ["sala", "puntaje Sala", "Puntaje Total"]
    resultados["resultados_salas"] = []

    return resultados

def completar_resultados(resultados:dict,numero_sala:int, puntaje_sala:int, puntaje_total:int)-> None:
    """agrega los puntajes de cada sala al diccionario del jugador
    Args:
     resultados:diccinario del jugador
     numero_sala: numero de salas completadas
     puntaje_sala : puntaje por sala
     puntaje_total: acumulador de puntaje por salas
    """
    resultados["resultados_salas"].append([numero_sala, puntaje_sala, puntaje_total])
    
def dibujar_encabezados(resultados:dict, fuente:pygame.font.Font, superficie:pygame.Surface, ancho:int)-> None:
    """dibujar las filas de encabezados del cuadro de resultados
    Args:
     resultados: diccionario del jugador
     fuente: fuente a usar
     superficie: superficie a dibujar
     ancho: espacio horizontal por encabezado
    """
    posicion_x = resultados["x"]
    posicion_y = resultados["y"]
    for encabezado in resultados["columnas"]:
        texto = fuente.render(encabezado, True, "black")
        superficie.blit(texto, (posicion_x, posicion_y))
        posicion_x += ancho

def dibujar_contenidos(resultados: dict, fuente: pygame.font.Font, superficie: pygame.Surface,ancho: int, alto: int) -> None:
    """dibuja el contenido de resultados de sala en formato matriz
    Args:
     resultados: diccionario de resultados de jugador
     fuente: fuente a usar
     superficie: superficie a dibujar
     ancho: espacio horizontal por cuadro
     alto: espacio vertical por cuadro
    """
    matriz = resultados["resultados_salas"]
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            x = resultados["x"] + j * ancho
            y = resultados["y"] + 30 + (i + 1) * alto
            texto = fuente.render(str(matriz[i][j]), True, "black")
            superficie.blit(texto, (x, y))

def dibujar_resultados(resultados: dict,superficie:pygame.Surface)-> None:
    """llama a las funciones de dibujo para graficar el cuadro de resultados de jugador
    Args:
     resultados: diccionario del jugador
     superficie: superficie a dibujar
    """
    fuente = crear_fuente(50)
    ancho = 250
    alto = 50
    dibujar_encabezados(resultados,fuente,superficie,ancho)
    dibujar_contenidos(resultados,fuente,superficie,ancho,alto)
