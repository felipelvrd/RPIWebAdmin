import json

from mega import MegaApi

from WebSocketServer.megaRPI.listener import DownloadListener
from WebSocketServer.megaRPI.megaCliente import MegaCliente
from WebSocketServer.megaRPI.config import DIRECTORIO_DESCARGAS


class MegaServer(object):
    def __init__(self):
        self.clientes = []
        self._api = MegaApi('oowWWYRZ', None, None, 'megaRPI')
        self.DownloadListener = DownloadListener(self.clientes)

    def agregar_cliente(self, web_socket_handler):
        mega_cliente = MegaCliente(self._api, web_socket_handler)
        web_socket_handler.is_open = True
        self.clientes.append(mega_cliente)
        return mega_cliente

    def eliminar_cliente(self, web_socket_handler):
        mega_cliente = next(c for c in self.clientes if c.web_socket_handler == web_socket_handler)
        web_socket_handler.is_open = False
        self.clientes.remove(mega_cliente)

    def enrutador(self, web_socket_handler, mensaje):
        j_data = json.loads(mensaje.decode('utf-8'))
        mega_cliente = next(c for c in self.clientes if c.web_socket_handler == web_socket_handler)
        cmd = j_data['cmd']

        if cmd == 'isLogged':
            mega_cliente.is_logged()
        elif cmd == 'login':
            mega_cliente.login(j_data)
        elif cmd == 'listaNodos':
            mega_cliente.listaNodos()
        elif cmd == 'descargar':
            self.descargar(j_data, web_socket_handler.cwd)
        elif cmd == 'cd':
            mega_cliente.cd(j_data)
        elif cmd == 'recargarNodos':
            mega_cliente.recargarNodos()

    def descargar(self, j_data, cwd):
        nombre = str(j_data['nombre'])
        node = self._api.getNodeByPath(str(nombre), cwd)
        if node is None:
            print ('Node not found')
            return
        self._api.startDownload(node, DIRECTORIO_DESCARGAS, self.DownloadListener)
