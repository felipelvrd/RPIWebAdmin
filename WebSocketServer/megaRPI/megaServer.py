import json
from mega import MegaApi, MegaError, MegaTransferListener
from WebSocketServer.megaRPI.utils import enviar_cliente, mkdir_recursivo
from WebSocketServer.megaRPI.megaCliente import MegaCliente
from WebSocketServer.DataBase.MegaSQLite import registrar_descarga
from WebSocketServer.config import DIRECTORIO_DESCARGAS
from WebSocketServer.DataBase.MegaSQLite import get_parametro

class MegaServer(object):
    def __init__(self):
        self.clientes = []
        self._api = MegaApi('oowWWYRZ', None, None, 'megaRPI')
        self.cola_descargas = []
        self.downloadListener = DownloadListener(self.clientes, self.cola_descargas)
        self.auto_login()

    def auto_login(self):
        if not self._api.isLoggedIn():
            id = get_parametro('ID')
            contrasenna = get_parametro('PASSWORD')
            if id is not None and contrasenna is not None:
                self._api.login(id, contrasenna)

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
        j_data = json.loads(mensaje.encode('utf-8'))
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
        nombre = str(j_data['nombre'].encode('utf-8'))
        node = self._api.getNodeByPath(str(nombre), cwd)
        path = self._api.getNodePath(node)
        if node is None:
            print ('Node not found')
            return
        # Verifica que no se este descargando ya el archivo
        if self.downloadListener.nodo_descarga_actual:
            if self._api.getNodePath(self.downloadListener.nodo_descarga_actual) == path:
                return
        # Verifica que el archivo no este en la lista de descargas
        if next((c for c in self.cola_descargas if self._api.getNodePath(c) == path), None) is not None:
            return
        self.cola_descargas.append(node)
        self.iniciar_descarga()

    def iniciar_descarga(self):
        iniciar_descarga(self.downloadListener, self.cola_descargas, self._api)


class DownloadListener(MegaTransferListener):
    def __init__(self, cli, cola_descargas):
        super(DownloadListener, self).__init__()
        self.cli = cli
        self.cola_descargas = cola_descargas
        self.nodo_descarga_actual = None

    def onTransferFinish(self, api, transfer, error):
        if error.getErrorCode() == MegaError.API_OK:
            registrar_descarga(api.getNodePath(self.nodo_descarga_actual))
        self.nodo_descarga_actual = None
        iniciar_descarga(self, self.cola_descargas, api)

    def onTransferStart(self, api, transfer):
        pass

    def onTransferData(self, api, transfer, buffer, size):
        return super(DownloadListener, self).onTransferData(api, transfer, buffer, size)

    def onTransferTemporaryError(self, api, transfer, error):
        return super(DownloadListener, self).onTransferTemporaryError(api, transfer, error)

    def onTransferUpdate(self, api, transfer):
        cola_descargas_str = []
        for i in self.cola_descargas:
            cola_descargas_str.append(i.getName())
        data = {
            'cmd': 'downloadUpdate',
            'nombre': transfer.getFileName(),
            'bytesTransferidos': transfer.getTransferredBytes(),
            'totalBytes': transfer.getTotalBytes(),
            'velocidad': transfer.getSpeed(),
            'cola_descargas': cola_descargas_str
        }
        for c in self.cli:
            enviar_cliente(c.web_socket_handler, data)


def iniciar_descarga(download_listener, cola_descargas, api):
    if download_listener.nodo_descarga_actual is None:
        if len(cola_descargas) > 0:
            nodo = cola_descargas.pop(0)
            download_listener.nodo_descarga_actual = nodo
            dir_descarga = DIRECTORIO_DESCARGAS + api.getNodePath(api.getParentNode(nodo)) + '/'
            mkdir_recursivo(dir_descarga)
            api.startDownload(nodo, dir_descarga, download_listener)
