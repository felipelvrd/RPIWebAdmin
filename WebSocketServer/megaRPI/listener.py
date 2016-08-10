from mega import MegaRequestListener, MegaError, MegaNode, MegaTransferListener
import json


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
        jData = json.dumps(data)
        self.webSocket.write_message(jData)


class ListaNodosListener(MegaRequestListener):
    def __init__(self, webSocket):
        super(ListaNodosListener, self).__init__()
        self.webSocket = webSocket

    def onRequestFinish(self, api, request, e):

        nodos = []
        cwd = api.getRootNode()
        path = cwd
        #salida.append('    .')
        if api.getParentNode(path) != None:
            #salida.append('    ..')
            pass
        nodes = api.getChildren(path)

        for i in range(nodes.size()):
            node = nodes.get(i)
            dictNodo = {
                'nombre': node.getName()
            }
            if node.getType() == MegaNode.TYPE_FILE:
                dictNodo['tipo'] = 'A'
                dictNodo['tamanno'] = node.getSize()
                pass
            else:
                dictNodo['tipo'] = 'F'
                pass
            nodos.append(dictNodo)

        data = {
            'cmd': 'listaNodos',
            'nodos': nodos
        }

        jData = json.dumps(data)

        if self.webSocket.is_open:
            self.webSocket.write_message(jData)


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
        jData = json.dumps(data)
        print jData
        print len(self.cli)
        #self.cli[0].
        for c in self.cli:
            if c.web_socket_handler.is_open:
                c.web_socket_handler.write_message(jData)


