from mega import MegaRequestListener, MegaError, MegaNode, MegaTransferListener

from WebSocketServer.megaRPI.utils import enviar_cliente


class LoginListener(MegaRequestListener):
    def __init__(self, webSocket):
        super(LoginListener, self).__init__()
        self.webSocket = webSocket

    def onRequestFinish(self, api, request, e):
        data = {
            'cmd': 'login',
            'errorCode': e.getErrorCode(),
            'errorString': MegaError.getErrorString(e.getErrorCode()),
        }
        enviar_cliente(self.webSocket, data)
        #api.fetchNodes()




class downloadListener(MegaTransferListener):
    def __init__(self, cli):
        super(downloadListener, self).__init__()
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
