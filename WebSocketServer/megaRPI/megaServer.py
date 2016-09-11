import json

from mega import MegaApi
from WebSocketServer.megaRPI.utils import iniciar_descarga
from WebSocketServer.megaRPI.listener import DownloadListener
from WebSocketServer.megaRPI.megaCliente import MegaCliente

class MegaServer(object):
    def __init__(self):
        self.clientes = []
        self._api = MegaApi('oowWWYRZ', None, None, 'megaRPI')
        self.cola_descargas = []
        self.downloadListener = DownloadListener(self.clientes, self.cola_descargas)

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
            mega_cliente.esta_logueado()
        elif cmd == 'login':
            mega_cliente.login(j_data)
        elif cmd == 'listaNodos':
            mega_cliente.lista_nodos()
        elif cmd == 'descargar':
            self.agregar_descarga(j_data, web_socket_handler.cwd)
        elif cmd == 'cd':
            mega_cliente.cd(j_data)
        elif cmd == 'recargarNodos':
            mega_cliente.recargar_nodos()

    def agregar_descarga(self, j_data, cwd):
        nombre = str(j_data['nombre'])
        node = self._api.getNodeByPath(str(nombre), cwd)
        if node is None:
            print ('Node not found')
            return
        self.cola_descargas.append(node)
        self.iniciar_descarga()

    def iniciar_descarga(self):
        iniciar_descarga(self.downloadListener, self.cola_descargas, self._api)
