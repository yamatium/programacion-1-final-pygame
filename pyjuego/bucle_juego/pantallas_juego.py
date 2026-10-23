import pygame,sys

from pyjuego.configuracion import *
from pyjuego.diccionarios.boton import *
from pyjuego.sonidos.manejo_sonido import *

pantalla = crear_superficie_pantalla()
clock = pygame.time.Clock()
fuente = crear_fuente(50) 

def respuesta_correcta() -> None:
    """ dibuja la animacion de respuesta correcta al responder bien la pregunta
    """ 
    boton_musica = crear_boton(1100, 620, 150,70, None, "musica")
    boton_continuar = crear_boton(450, 600, 300,80,"white", "continuar")
    botones = [boton_musica,boton_continuar]
    bien = pygame.image.load("pyjuego/imagenes/juego_imagenes/thumbs-up.png").convert()
    bien_scale = pygame.transform.scale(bien, (498,390))
    fondo_puerta = pygame.image.load("pyjuego/imagenes/juego_imagenes/doorTrans.png").convert_alpha()
    fondo_real = pygame.image.load("pyjuego/imagenes/juego_imagenes/campo2.png").convert()
    fondo_scale = pygame.transform.scale(fondo_puerta, (1500,700))

    puerta_izquierda = pygame.image.load("pyjuego/imagenes/juego_imagenes/door2.png").convert_alpha()
    izquierda_scale = pygame.transform.scale(puerta_izquierda, (300,450))
    puerta_derecha = pygame.image.load("pyjuego/imagenes/juego_imagenes/door1.png").convert_alpha()
    derecha_scale = pygame.transform.scale(puerta_derecha, (300,450))
    mensaje = fuente.render("Respuesta Correcta!", True, "black")

    x = 305
    z = 600
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if colision(boton_continuar,event.pos):
                        running = False
                    if colision(boton_musica, event.pos):
                        entrar_sonido()
                        manejar_musica()

        mx, my = pygame.mouse.get_pos()
        pantalla.blit(fondo_real, (0,0))
        pantalla.blit(bien_scale, (340,160))
        pantalla.blit(mensaje, (410,120))
        pantalla.blit(fondo_scale, (-100, -120))
        pantalla.blit(izquierda_scale, (x,100))
        pantalla.blit(derecha_scale, (z,100))

        dibujar_botones(botones,pantalla,(mx,my))
        x -= 0.6
        z += 0.6
        
        pygame.display.flip()
        clock.tick(60)


def eliminados_sala_1(lista:list)-> list:
    """ crea una lista con los nombres de quienes no pasaron la sala 1
    Args:
     lista: lista de diccionarios
    Returns:
     list: lista de nombres
    """ 
    sala_1 = []
    for diccionario in lista:
        if diccionario["salas"] < 2 :
            sala_1.append(diccionario["nombre"])
    return sala_1

def encontrar_maximo(lista:list, clave: str)-> int:
    """ encuentra el valor maximo segun la clave
    Args:
     lista: lista de diccionarios de puntaje
     clave: valor maximo a comparar
    Returns:
     int: valor maximo
    """ 
    maximo = lista[0][clave]
    for diccionario in lista:
        if diccionario[clave] > maximo:
            maximo = diccionario[clave]
    return  maximo

def encontrar_ganadores_valor(lista:list, clave:str, valor:int)-> list:
    """devuelve los nombres de quienes tienen valor segun el valor de llave
    Args:
     lista: lista de diccionarios de jugadores
     clave: llave de diccionario a buscar
     valor: valor a comparar en el diccionario
    Returns:
     list: lista de nombres de jugadores que cumplan la condicion
    """
    nombres = []
    for jugador in lista:
        if jugador[clave] == valor:
            nombres.append(jugador["nombre"])
    return nombres

def formatear_nombres(jugadores:list) -> str:
    """formatea la lista de jugadores para usar en los mensajes
    Args:
     jugadores: lista de jugadores
    Returns:
     str: string de nombre de jugador
    """
    mensaje = ""
    separador = ", "
    for i in range(len(jugadores)):
        if i > 0:
            mensaje += separador
        mensaje += jugadores[i]
    return mensaje

def mensaje_sala_1(eliminados_sala:list)-> pygame.Surface:
    """crea el texto de mensaje de sala 1 para dibujar
    Args:
     eliminados_sala: lista de eliminados
    Returns:
     pygame.Surface: superficie con mensaje
    """
    if eliminados_sala:
        nombres = formatear_nombres(eliminados_sala)
        mensaje_eliminados = fuente.render(f"No superaron sala 1: {(nombres)}", True, "red")
    else:
        mensaje_eliminados = fuente.render("Todos superaron la sala 1!", True, "green")
    return mensaje_eliminados

def mensaje_mayor_puntaje(puntaje_maximo:int, ganadores_puntaje:list) -> pygame.Surface:
    """crea un texto de mensaje de jugadores con mayor puntaje
    Args:
     puntaje_maximo: int
     ganadores_puntaje:lista
    Returns:
     pygame.Surface: superficie con mensaje
    """
    nombres = formatear_nombres(ganadores_puntaje)
    return fuente.render(f"Mayor puntaje ({puntaje_maximo} pts): {nombres}", True, "yellow")

def mensaje_mayor_sala(sala_maxima:int, ganadores:list)-> pygame.Surface:
    """crea un texto de mensaje de jugadores con mayor sala
    Args:
        sala_maxima: int
        ganadores:lista
    Returns:
        pygame.Surface: superficie con mensaje
    """
    nombres = formatear_nombres(ganadores)
    return fuente.render(f"Llegaron mas lejos (sala {sala_maxima}): {nombres}", True, "aqua")

def mostrar_torneo(resultados:list) -> None:
    """muestra los resultados del modo torneo
    Args:
     resultados: lista con los datos de los jugadores del torneo
    """
    fondo = pygame.image.load("pyjuego/imagenes/juego_imagenes/forest.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (1380, 920 ))
    boton_musica = crear_boton(1100, 620, 150,70, "white", "musica")
    boton_salir = crear_boton(400, 600, 450,100,"white", "Salir")
    botones = [boton_musica,boton_salir]

    puntaje_maximo = encontrar_maximo(resultados,"puntuacion")
    ganadores_puntaje = encontrar_ganadores_valor(resultados,"puntuacion",puntaje_maximo)
    sala_maxima = encontrar_maximo(resultados, "salas")
    ganadores_salas = encontrar_ganadores_valor(resultados,"salas",sala_maxima)
    eliminados_sala = eliminados_sala_1(resultados)
    titulo = fuente.render("Resultados del Torneo", True, "white")
    puntaje_superficie = mensaje_mayor_puntaje(puntaje_maximo,ganadores_puntaje)
    sala_superficie = mensaje_mayor_sala(sala_maxima,ganadores_salas)
    texto_superficie = mensaje_sala_1(eliminados_sala)

    dibujar = [titulo,puntaje_superficie,sala_superficie,texto_superficie]
    posiciones = [(380, 40),(380, 240),(380, 290),(380, 340)]  

    # --- pantalla de resultados ---
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if colision(boton_salir, event.pos):
                    running = False
                elif colision(boton_musica, event.pos):
                    entrar_sonido()
                    manejar_musica()

        pantalla.blit(fondo_escalado, (-50,-100))
        mx, my = pygame.mouse.get_pos()
        for i in range(len(dibujar)):
            pantalla.blit(dibujar[i], (posiciones[i]))
        dibujar_botones(botones,pantalla,(mx,my))

        pygame.display.flip()
        clock.tick(60)