import json
import os


def enviar_cliente(web_socket_handler, diccionario):
    j_data = json.dumps(diccionario)
    if web_socket_handler.is_open:
        web_socket_handler.write_message(j_data)


def mkdir_recursivo(path):
    sub_path = os.path.dirname(path)
    if not os.path.exists(sub_path):
        mkdir_recursivo(sub_path)
    if not os.path.exists(path):
        os.mkdir(path)
