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
    sql_file = open('DataBase/tablas.sql', 'r')
    sql_script = sql_file.read()
    conexion.executescript(sql_script)
    conexion.commit()
