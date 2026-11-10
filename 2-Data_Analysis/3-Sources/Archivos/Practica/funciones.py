import os
import shutil
from variables import *

def ordenar_directorios(ruta):
    # guardar ruta desde la que se ejecuta la función para volver a ella antes de terminar la ejecución
    ruta_inicial = os.getcwd()

    # cambiar directorio a la ruta que se ha puesto como argumento
    os.chdir(ruta)

    carpetas_destino = {
        "Documentos": doc_types,
        "Imagenes": img_types,
        "Software": software_types,
        "Otros": ()
    }

    for carpeta in carpetas_destino.keys():
        try:
            os.mkdir(carpeta)
        except FileExistsError:
            pass # Si ya existe, sigue continúa sin romperse

    lista_archivos = os.listdir() # para que guarde todo los archivos antes de entrar en el bucle for para que no sobreesccriba

    for nombre_carpeta, extensiones in carpetas_destino.items():
        if nombre_carpeta == "Otros":
            continue 

        for extension in extensiones:
            for archivo in lista_archivos:
                if archivo.endswith(extension):
                    shutil.move(archivo, f"{nombre_carpeta}/")

    # gestionando resto archivos para Otros
    for archivo in os.listdir():
        if archivo not in carpetas_destino.keys():
            shutil.move(archivo, "Otros/")

    # guardar el orden de los archivos
    resultado = os.walk(os.getcwd()) 

    # volviendo a la ruta inicial desde la que se ha ejecutado la función
    os.chdir(ruta_inicial)
    
    return  [x for x in resultado]