import os

from pyjuego.diccionarios.boton import *
from pyjuego.sonidos.manejo_sonido import *

def guardar_puntaje(nombre:str, estado_final: bool,puntaje:int) -> None:
    """guarda el resultado del jugador en un archivo csv 
    Args:
     nombre: nombre del jugador
     estado_final: estado de juego del jugador
     puntaje: puntaje del jugador
    """
    revisar_estado = lambda estado: "Completo" if estado else "No completo"
    estado = revisar_estado(estado_final)

    with open("pyjuego/manejo_puntaje/puntuacion.csv", "a") as archivo:
        archivo.write(f"{nombre},{estado},{puntaje}\n")

def ordenar_puntajes(lista:list)-> list:
    """ordena la puntuacion de jugadores con algoritmo de burbuja
    Args:
     lista: lista a ordenar
    Returns:
     list: lista ordenada de mayor a menor
    """
    recorrido = len(lista)

    for i in range(recorrido-1):
        for j in range(recorrido-i-1):
            if lista[j]["puntaje"] < lista[j+1]["puntaje"]:
                temp = lista[j]
                lista[j] = lista[j+1]
                lista[j+1] = temp
    return lista

def cargar_puntuacion()-> list:
    """transforma el csv en una lista para mostrar en la pantalla de puntuacion
    Returns:
     list: lista ordenado con ordenar_puntajes
    """
    puntuacion = []
    try:
        with open("pyjuego/manejo_puntaje/puntuacion.csv", "r") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")  # strip saca el \n invisible
                nombre = partes[0]
                estado = partes[1]
                puntaje = int(partes[2]) 
                puntuacion.append({"nombre": nombre, "estado": estado, "puntaje": puntaje}) 
    except FileNotFoundError:
        print("Archivo no encontrado")
    return ordenar_puntajes(puntuacion) 

def borrar_puntuacion() -> None:
    """borra el archivo de puntuacion si existe
    """
    try:
        os.remove("pyjuego/manejo_puntaje/puntuacion.csv")
    except FileNotFoundError:
        pass 

def aplicar_scroll(boton:dict, posicion_scroll:int) -> dict:
    """cambia la posicion de las puntuaciones segun el boton de scroleo
    Args:
     boton: diccionario de boton 
     posicion_scroll: posicion vertical del movimiento 
    Returns:
     dict: diccionario con la posicion vertidal cambiada
    """
    y_scroll = boton["y_base"] - posicion_scroll
    boton["rectangulo"].y = y_scroll
    boton["texto_rectangulo"].center = boton["rectangulo"].center
    return boton

def crear_rectangulos_puntuacion(puntajes:list) -> list:
    """crea una lista de botones con datos de cada puntajes
    Args:
     puntajes: lista de puntajes
    Returns:
     lista de botones de puntajes para ser dibujada
    """
    botones_puntaje = []
    y = 170
    for p in puntajes:
        texto = f"{p['nombre']} | {p['estado']} | {p['puntaje']}"
        box = crear_boton(350, y, 700,60,"gray", texto)
        box["y_base"] = y
        botones_puntaje.append(box)
        y += 70
    return botones_puntaje

def valor_maximo(a:int,b:int)-> int:
    """busca el valor maximo entre 2 numeros
    Args:
     a: primer numero
     b: segundo numero
    Returns:
     int: valor maximo para la posicion vertical del scroll
    """
    maximo = 0
    if a > b:
        maximo = a
    else:
        maximo = b
    return maximo

def valor_minimo(a:int,b:int)-> int:
    """busca el valor minimo entre 2 numeros
    Args:
        a: primer numero
        b: segundo numero
    Returns:
        int: valor minimo para la posicion vertical del scroll
    """
    minimo = 0
    if a < b:
        minimo = a
    else:
        minimo = b
    return minimo

def manejar_click(botones:list,evento:tuple)-> str:
    """manejo de evento de mouse
    Args:
     botones: lista de botones
     evento: posicion (x,y) del mouse
    Returns:
     str: accion a realizar segun el click del mouse
    """
    accion = ""
    if colision(botones[0], evento):
        salir_sonido()
        accion = "salir"
    elif colision(botones[1],evento):
        salir_sonido()
        accion = "borrar"
    elif colision(botones[2], evento):
        accion = "subir"
    elif colision(botones[3], evento):
        accion = "bajar"
    elif colision(botones[4], evento):
        entrar_sonido()
        manejar_musica()

    return accion
    