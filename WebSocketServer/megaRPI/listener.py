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
        api.fetchNodes()


class ListaNodosListener(MegaRequestListener):
    def __init__(self, webSocket):
        super(ListaNodosListener, self).__init__()
        self.webSocket = webSocket
        self.cwd = None

    def onRequestFinish(self, api, request, e):
        nodos = []
        if not self.cwd:
            self.cwd = api.getRootNode()
        path = self.cwd

        dictNodo = {
            'nombre': '/',
            'tipo': 'F'
        }
        nodos.append(dictNodo)

        if api.getParentNode(path) != None:
            dictNodo = {
                'nombre': '..',
                'tipo': 'F'
            }
            nodos.append(dictNodo)
        nodes = api.getChildren(path)

        for i in range(nodes.size()):
            node = nodes.get(i)
            dictNodo = {
                'nombre': node.getName()
            }
            if node.getType() == MegaNode.TYPE_FILE:
                dictNodo['tipo'] = 'A'
                dictNodo['tamanno'] = node.getSize()
            else:
                dictNodo['tipo'] = 'F'
            nodos.append(dictNodo)

        data = {
            'cmd': 'listaNodos',
            'nodos': nodos
        }
        enviar_cliente(self.webSocket, data)


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
