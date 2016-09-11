from WebSocketServer.config import RUTA_ARCHIVO_BASE_DATOS
from os.path import exists
import sqlite3


def abrir_conexion():
    if not exists(RUTA_ARCHIVO_BASE_DATOS):
        conexion = sqlite3.connect(RUTA_ARCHIVO_BASE_DATOS)
        crearTablas(conexion)
    else:
        conexion = sqlite3.connect(RUTA_ARCHIVO_BASE_DATOS)
    return conexion


def crearTablas(conexion):
    conexion.execute("""CREATE TABLE mega_descargas
                                        (
                                            ID INTEGER PRIMARY KEY,
                                            URI_PUBLICO TEXT NOT NULL,
                                            FECHA DATETIME NOT NULL
                                        )""")
    conexion.commit()
