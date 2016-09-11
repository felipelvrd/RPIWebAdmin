from mega import MegaRequestListener, MegaError, MegaTransferListener

from WebSocketServer.megaRPI.utils import iniciar_descarga
from WebSocketServer.megaRPI.utils import enviar_cliente
from WebSocketServer.DataBase.MegaSQLite import registrar_descarga


class LoginListener(MegaRequestListener):
    def __init__(self, web_socket_handler):
        super(LoginListener, self).__init__()
        self.webSocket = web_socket_handler

    def onRequestFinish(self, api, request, e):
        pass
        data = {
            'cmd': 'login',
            'errorCode': e.getErrorCode(),
            'errorString': MegaError.getErrorString(e.getErrorCode()),
        }
        enviar_cliente(self.webSocket, data)


class DownloadListener(MegaTransferListener):
    def __init__(self, cli, cola_descargas):
        super(DownloadListener, self).__init__()
        self.cli = cli
        self.descarga_activa = False
        self.cola_descargas = cola_descargas
        self.nodo_descarga_actual = None

    def onTransferFinish(self, api, transfer, error):
        if error.getErrorCode() == MegaError.API_OK:
            registrar_descarga(api.getNodePath(self.nodo_descarga_actual))
        self.descarga_activa = False
        self.nodo_descarga_actual = None
        iniciar_descarga(self, self.cola_descargas, api)


    def onTransferStart(self, api, transfer):
        self.descarga_activa = True

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
