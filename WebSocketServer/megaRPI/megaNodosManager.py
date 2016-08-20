from WebSocketServer.megaRPI.utils import enviar_cliente
from mega import MegaRequestListener, MegaNode


class MegaNodosManager(object):
    def __init__(self, api, web_socket_handler):
        self.api = api
        self.cwd = None
        self.web_socket_handler = web_socket_handler
        self.obtenerNodosListener = ObtenerNodosListener(web_socket_handler)

    def CargarNodos(self):
        self.api.fetchNodes(self.obtenerNodosListener)

    def ListarNodos(self):
        if self.cwd == None:
            self.cwd = self.api.getRootNode()
        if self.cwd == None:
            self.CargarNodos()
        else:
            data = self.ListarNodosStatic(self.api, self.cwd)
            enviar_cliente(self.web_socket_handler, data)

    @staticmethod
    def ListarNodosStatic(api, cwd):
        nodos = []
        path = cwd
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

        nodePath = api.getNodePath(cwd)
        data = {
            'cmd': 'listaNodos',
            'path': nodePath,
            'nodos': nodos
        }
        return data

    def CambiarNodo(self, dir):
        if self.cwd == None:
            self.cwd = self.api.getRootNode()
        node = self.api.getNodeByPath(dir, self.cwd)
        if node == None:
            print('{}: No such file or directory'.format(dir))
            return
        if node.getType() == MegaNode.TYPE_FILE:
            print('{}: Not a directory'.format(dir))
            return
        self.cwd = node
        self.ListarNodos()

class ObtenerNodosListener(MegaRequestListener):
    def __init__(self, webSocket):
        super(ObtenerNodosListener, self).__init__()
        self.webSocket = webSocket

    def onRequestFinish(self, api, request, e):
        cwd = api.getRootNode()
        data = MegaNodosManager.ListarNodosStatic(api, cwd)
        enviar_cliente(self.webSocket, data)


