import pygame,sys

from pyjuego.configuracion import crear_fuente,crear_superficie_pantalla
from pyjuego.diccionarios.boton import *
from .funciones_puntuacion import *


def puntuacion()-> None:
    """ ventana de puntuacion 
    """
    pantalla = crear_superficie_pantalla()
    clock = pygame.time.Clock()
    fuente = crear_fuente(50)
    fondo = pygame.image.load("pyjuego/imagenes/juego_imagenes/arbol.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (1380, 920 ))
    puntuacion_Vacia = fuente.render("No hay puntajes todavia, ve a jugar!", True, "black")
    titulo = fuente.render("Tabla de puntuaciones", True, "black")
    formato_puntaje = fuente.render("Jugador | estado final | puntaje", True, "black")

    boton_salir = crear_boton(40, 550, 240, 60, "grey", "salir")
    boton_borrar = crear_boton(40, 650, 240, 60, "grey", "borrar tabla")
    boton_musica = crear_boton(1100, 620, 150,70, None, "musica")
    boton_subir = crear_boton(1100, 150, 60, 50, "gray", "^")
    boton_bajar = crear_boton(1100, 500, 60, 50, "gray", "v")

    posicion_scroll = 0 
    velocidad_scroll = 50 
    lista_area = pygame.Rect(0, 140, 1280, 470) 
    botones = [boton_salir, boton_borrar, boton_subir, boton_bajar, boton_musica]
    puntajes = cargar_puntuacion()
    botones_puntaje = crear_rectangulos_puntuacion(puntajes)
        
    altura_lista = len(botones_puntaje) * 80
    maximo_scroll = (altura_lista - lista_area.height) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                accion = manejar_click(botones, event.pos)
                if accion == "borrar":
                    borrar_puntuacion()
                    botones_puntaje = [] 
                    puntajes = []
                elif accion == "subir":
                    posicion_scroll -= velocidad_scroll 
                    posicion_scroll = valor_maximo(0,posicion_scroll)
                elif accion == "bajar":
                    posicion_scroll += velocidad_scroll
                    minimo = valor_minimo(posicion_scroll, maximo_scroll)
                    posicion_scroll = valor_maximo(0, minimo)
                elif accion == "salir":
                    running = False
        
        mx, my = pygame.mouse.get_pos()
        pantalla.blit(fondo_escalado, (-50,-100))
        pantalla.blit(titulo, (470,60))
        pantalla.blit(formato_puntaje, (420,100))
        dibujar_botones(botones, pantalla, (mx, my))

        if not puntajes:
           pantalla.blit(puntuacion_Vacia,(330,380))    
        pantalla.set_clip(lista_area) 

        for boton in botones_puntaje:
            boton = aplicar_scroll(boton, posicion_scroll)
            dibujar_botones(boton, pantalla, (mx, my))

        pantalla.set_clip(None)
        pygame.display.flip()
        clock.tick(60)