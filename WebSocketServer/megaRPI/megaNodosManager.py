from WebSocketServer.megaRPI.utils import enviar_cliente
from WebSocketServer.megaRPI.config import DIRECTORIO_DESCARGAS
from mega import MegaRequestListener, MegaNode
from os.path import isfile


class MegaNodosManager(object):
    def __init__(self, api, web_socket_handler):
        self.api = api
        self.web_socket_handler = web_socket_handler
        self.obtenerNodosListener = ObtenerNodosListener(web_socket_handler)
        self.web_socket_handler.cwd = api.getRootNode()

    def CargarNodos(self):
        self.api.fetchNodes(self.obtenerNodosListener)

    def listar_nodos(self):
        if self.web_socket_handler.cwd is None:
            self.CargarNodos()
        else:
            data = self.listar_nodos_static(self.api, self.web_socket_handler.cwd)
            enviar_cliente(self.web_socket_handler, data)

    @staticmethod
    def listar_nodos_static(api, cwd):
        nodos = []
        path = cwd
        dict_nodo = {
            'nombre': '/',
            'tipo': 'F'
        }
        nodos.append(dict_nodo)
        if api.getParentNode(path) is not None:
            dict_nodo = {
                'nombre': '..',
                'tipo': 'F'
            }
            nodos.append(dict_nodo)
        nodes = api.getChildren(path)

        for i in range(nodes.size()):
            node = nodes.get(i)
            descargado = False
            dict_nodo = {
                'nombre': node.getName(),
                'descargado': descargado
            }
            if node.getType() == MegaNode.TYPE_FILE:
                dict_nodo['tipo'] = 'A'
                dict_nodo['tamanno'] = node.getSize()
                if isfile(DIRECTORIO_DESCARGAS + node.getName()):
                    dict_nodo['descargado'] = True
            else:
                dict_nodo['tipo'] = 'F'
            nodos.append(dict_nodo)

        node_path = api.getNodePath(cwd)
        data = {
            'cmd': 'listaNodos',
            'path': node_path,
            'nodos': nodos
        }
        return data

    def CambiarNodo(self, directorio):
        node = self.api.getNodeByPath(directorio, self.web_socket_handler.cwd)
        if node is None:
            print('{}: No such file or directory'.format(directorio))
            return
        if node.getType() == MegaNode.TYPE_FILE:
            print('{}: Not a directory'.format(directorio))
            return
        self.web_socket_handler.cwd = node
        self.listar_nodos()


class ObtenerNodosListener(MegaRequestListener):
    def __init__(self, web_socket_handler):
        super(ObtenerNodosListener, self).__init__()
        self.webSocket = web_socket_handler

    def onRequestFinish(self, api, request, e):
        self.webSocket.cwd = api.getRootNode()
        data = MegaNodosManager.listar_nodos_static(api, self.webSocket.cwd)
        enviar_cliente(self.webSocket, data)


