import json


def enviar_cliente(web_socket_handler, diccionario):
    jData = json.dumps(diccionario)
    if web_socket_handler.is_open:
        web_socket_handler.write_message(jData)
