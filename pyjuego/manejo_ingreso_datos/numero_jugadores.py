import pygame,sys

from pyjuego.configuracion import crear_fuente,crear_superficie_pantalla
from pyjuego.diccionarios.boton import *
from pyjuego.sonidos.manejo_sonido import *
from .ingresar_datos import manejo_rect_ingreso,validar_numero

pygame.init()

def manejo_click(botones:list,evento:tuple,cant_jugadores:str)-> str:
    """manejo de evento de mouse
    Args:
     botones: lista de diccionarios
     evento: posicion (x,y) del mouse
     cant_jugadores: string de cantidad de jugadores
    Returns:
     accion: string de accion a realizar
    """
    accion = ""
    if colision(botones[0], evento) and len(cant_jugadores) > 0:
        accion = "continuar"
    elif colision(botones[2], evento):
        entrar_sonido()
        manejar_musica()
    elif colision(botones[1], evento):
        salir_sonido()
        accion = "salir"

    return accion

def manejo_texto(cant_jugadores: str, evento: pygame.event.Event)-> str:
    """actualiza la cantidad de jugadores segun la tecla presionada
    Args:
     cant_jugadores: texto actual
     evento: tecla presionada
    Returns:
     str: el texto actualizado despues de presionar una tecla
    """
    resultado = cant_jugadores
    if evento.key == pygame.K_BACKSPACE:
       resultado = cant_jugadores[:-1]
    elif validar_numero(evento.unicode):
       nuevo = cant_jugadores + evento.unicode
       if nuevo[0] != "0" and 1 <= int(nuevo) <= 10:
          resultado = nuevo
    return resultado

def manejo_teclado(evento: pygame.event.Event, cant_jugadores:str, numero_activo: bool)-> tuple:
    """manejo de eventos de teclado
    Args:
     evento: tecla presionada
     cant_jugadores: texto actual
     numero_activo: si el campo esta seleccionado para escribir
    Returns:
     tuple: valor de accion varia si se presiona ESC y el texto del campo 
    """
    accion = ""
    if evento.key == pygame.K_ESCAPE:
        accion = "salir"
    elif numero_activo:
        cant_jugadores = manejo_texto(cant_jugadores,evento)
    return accion, cant_jugadores

def ingresar_jugadores() -> int | None:
    """pantalla de ingreso de numero de jugadores
    Returns:
     resultado: numero de jugadores o None si el jugador sale al menu
    """
    pantalla = crear_superficie_pantalla()
    clock = pygame.time.Clock()
    fuente = crear_fuente(50)
    fondo = pygame.image.load("pyjuego/imagenes/juego_imagenes/campo.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (1380, 920 ))

    titulo = fuente.render("Ingresa cantidad de jugadores", True, "black")
    cantidad = fuente.render("Minimo 1, maximo 10",True, "black")

    boton_continuar = crear_boton(500, 620, 200, 70, "white", "Continuar")
    boton_musica = crear_boton(1100, 620, 150,70, "white", "musica")
    boton_salir = crear_boton(100, 620, 200, 70, "white", "Salir")
    rect_ingreso_numero = pygame.Rect(500, 400, 200, 40)

    cant_jugadores = ''
    numero_activo = False
    botones = [boton_continuar,boton_salir,boton_musica]

    resultado = None 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                accion, cant_jugadores = manejo_teclado(event,cant_jugadores,numero_activo)
                if accion == "salir":
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                numero_activo = manejo_rect_ingreso(rect_ingreso_numero,event.pos)
                accion = manejo_click(botones, event.pos, cant_jugadores)
                if accion == "continuar":
                    resultado = int(cant_jugadores)
                    running = False
                elif accion == "salir":
                    running = False

        pantalla.blit(fondo_escalado, (-50,-100))
        mx, my = pygame.mouse.get_pos()
        pantalla.blit(titulo, (350,200))
        pantalla.blit(cantidad,(420,260))

        color_numero = lambda numero_activo: "white" if numero_activo else "darkgray" 
        pygame.draw.rect(pantalla, color_numero(numero_activo), rect_ingreso_numero)
        superficie_numero = fuente.render(cant_jugadores, True, "black")
        pantalla.blit(superficie_numero, (rect_ingreso_numero.x + 5,rect_ingreso_numero.y + 5))
        dibujar_botones(botones, pantalla, (mx, my))

        pygame.display.flip()
        clock.tick(60)

    return resultado
