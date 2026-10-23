import pygame

from .configuracion import crear_superficie_pantalla,crear_fuente,elejir_numero
from .manejo_puntaje.puntuacion import puntuacion
from .bucle_juego.juego import jugar
from .bucle_juego.pantallas_juego import mostrar_torneo
from .manejo_ingreso_datos.ingresar_datos import ingreso_datos
from .manejo_ingreso_datos.numero_jugadores import ingresar_jugadores
from .diccionarios.boton import *
from .sonidos.manejo_sonido import *

def empezar() -> None:
    """ manejo de logica de bucle del juego segun la cantidad de jugadores ingresados
    """ 
    jugadores = ingresar_jugadores()
    if jugadores:
        pygame.mixer.music.fadeout(500)
        musica_menu(2)
        resultados = []
        while len(resultados) < jugadores:
          nombre_jugador = ingreso_datos()
          resultado_jugador = jugar(nombre_jugador)
          resultados.append(resultado_jugador)
        if jugadores > 1:
            mostrar_torneo(resultados)
        musica_menu(1)

def definir_icono_nombre_ventana(icono:pygame.Surface)->None:
    """ configura el icono y el nombre de la ventana del juego
    Args:
     icono: superficie de pygame
    """ 
    pygame.display.set_icon(icono)
    pygame.display.set_caption("FINAL")

def elegir_imagen_gato(numero:int)-> pygame.Surface: 
    """ crea y configura la imagen segun el parametro
    Args:
     numero: numero elejido para la imagen
    Returns:
     superficie de pygame
    """ 
    img_elejida = pygame.image.load(f"pyjuego/imagenes/gatos/{numero}.png").convert_alpha()
    imagen_escalada = pygame.transform.scale(img_elejida, (400, 400))
    return imagen_escalada

def manejar_teclado(evento:pygame.event.Event)-> bool:
    """manejo de eventos del teclado
    Args:
      evento: evento keydown de pygame
    Returns: 
      booleano de estado de la pantalla
    """
    running = True
    if evento.key == pygame.K_SPACE:
        manejar_musica()
    elif evento.key == pygame.K_ESCAPE:
        running = False
    return running

def manejar_click (botones:list,pos:tuple)-> bool:
    """manejo de eventos de mouse
    Args:
      botones: lista de botones
      pos: posicion (x,y) del mouse
    Returns:
      booleano del estado de menu
    """
    running = True
    if colision(botones[0],pos):
        entrar_sonido()
        empezar()
    elif colision(botones[1], pos):
        entrar_sonido()
        puntuacion()
    elif colision(botones[2],pos):
        entrar_sonido()
        manejar_musica()
    elif colision(botones[3], pos):
        salir_sonido()
        running = False
    return running


def iniciar()-> None:
    """configuracion inicial y manejo del menu principal 
    """
    pygame.init()
    pantalla = crear_superficie_pantalla()
    fuente_final = crear_fuente(150)
    clock = pygame.time.Clock()
    icono = pygame.image.load("pyjuego/imagenes/juego_imagenes/fred.png")
    definir_icono_nombre_ventana(icono)

    numero = elejir_numero(1,10)
    imagen_gato = elegir_imagen_gato(numero)
    fondo = pygame.image.load("pyjuego/imagenes/juego_imagenes/cloud.jpg").convert()
    fondo_escalado = pygame.transform.scale(fondo,(1380, 920))
    titulo = fuente_final.render("FINAL", True, "green")

    boton_jugar = crear_boton(40,360,220,100,"white", "Jugar") 
    boton_puntuacion = crear_boton(40,480,220,100, "white", "puntajes")
    boton_musica = crear_boton(1100, 620, 150,70, None, "musica")  # none lo convierte en transparente
    boton_salir = crear_boton(40,600,220,100,"white","Salir")
    botones = [boton_jugar,boton_puntuacion,boton_musica, boton_salir]

    musica_menu(1)
    running = True
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = manejar_teclado(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                running = manejar_click(botones,event.pos)
            
        mx, my = pygame.mouse.get_pos()
        pantalla.blit(fondo_escalado, (-50,-100))
        pantalla.blit(titulo, (30,50))
        pantalla.blit(imagen_gato, (800, 100))
        
        dibujar_botones(botones,pantalla, (mx, my))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


