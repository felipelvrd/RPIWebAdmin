import json
from WebSocketServer.config import DIRECTORIO_DESCARGAS


def enviar_cliente(web_socket_handler, diccionario):
    jData = json.dumps(diccionario)
    if web_socket_handler.is_open:
        web_socket_handler.write_message(jData)


def iniciar_descarga(downloadListener, cola_descargas, api):
    if not downloadListener.descarga_activa:
        if len(cola_descargas) > 0:
            nodo = cola_descargas.pop(0)
            downloadListener.nodo_descarga_actual = nodo
            api.startDownload(nodo, DIRECTORIO_DESCARGAS, downloadListener)
