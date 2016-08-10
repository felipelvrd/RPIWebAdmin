import json

from mega import MegaApi

from WebSocketServer.megaRPI.listener import downloadListener
from WebSocketServer.megaRPI.megaCliente import MegaCliente


class MegaServer:
    def __init__(self):
        self.clientes = []
        self._api = MegaApi('oowWWYRZ', None, None, 'megaRPI')
        self.DownloadListener = downloadListener(self.clientes)

    def agregar_cliente(self, web_socket_handler):
        megaCliente = MegaCliente(self._api, web_socket_handler)
        web_socket_handler.is_open = True
        self.clientes.append(megaCliente)

    def eliminar_cliente(self, web_socket_handler):
        megaCliente = next(c for c in self.clientes if c.web_socket_handler == web_socket_handler)
        web_socket_handler.is_open = False
        self.clientes.remove(megaCliente)

    def enrutador(self, web_socket_handler, mensaje):
        j_data = json.loads(mensaje.decode('utf-8'))
        megaCliente = next(c for c in self.clientes if c.web_socket_handler == web_socket_handler)
        cmd = j_data['cmd']
        if cmd == 'isLogged':
            megaCliente.is_logged()
        elif cmd == 'login':
            megaCliente.login(str(j_data['email']), str(j_data['contrasenna']))
        elif cmd == 'listaNodos':
            megaCliente.lista_nodos()
        elif cmd == 'descargar':
            self.descargar(j_data['nombre'])

    def descargar(self, nombre):
        cwd = self._api.getRootNode()
        node = self._api.getNodeByPath(str(nombre), cwd)
        if node == None:
            self.write_message('Node not found')
            return
        self._api.startDownload(node, './', self.DownloadListener)

        """elif cmd == 'getEmail':
            self.get_email()"""
