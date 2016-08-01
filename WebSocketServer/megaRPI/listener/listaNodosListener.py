from mega import MegaRequestListener, MegaError, MegaNode
import json


class ListaNodosListener(MegaRequestListener):
    def __init__(self, webSocket, cli):
        super(ListaNodosListener, self).__init__()
        self.webSocket = webSocket
        self.cli = cli

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
        self.webSocket.write_message(jData)
        self.cli.remove(self)
