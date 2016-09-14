import json


def enviar_cliente(web_socket_handler, diccionario):
    j_data = json.dumps(diccionario)
    if web_socket_handler.is_open:
        web_socket_handler.write_message(j_data)
