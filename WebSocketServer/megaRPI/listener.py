from mega import MegaRequestListener, MegaError, MegaTransferListener
from WebSocketServer.megaRPI.utils import enviar_cliente


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
    def __init__(self, cli):
        super(DownloadListener, self).__init__()
        self.cli = cli

    def onRequestStart(self, api, request):
        print 'inicia'

    def onTransferUpdate(self, api, transfer):
        data = {
            'cmd': 'downloadUpdate',
            'nombre': transfer.getFileName(),
            'bytesTransferidos': transfer.getTransferredBytes(),
            'totalBytes': transfer.getTotalBytes(),
            'velocidad': transfer.getSpeed()
        }
        for c in self.cli:
            enviar_cliente(c.web_socket_handler, data)
