from WebSocketServer.megaRPI.listener import LoginListener, ListaNodosListener, MegaNode
from WebSocketServer.megaRPI.utils import enviar_cliente

class MegaCliente:
    def __init__(self, api, web_socket_handler):
        self._api = api
        self.web_socket_handler = web_socket_handler
        self.loginListener = LoginListener(self.web_socket_handler)
        self.listaNodosListener = ListaNodosListener(self.web_socket_handler)


    def login(self, j_data):
        usuario = str(j_data['email'])
        contrasenna = str(j_data['contrasenna'])
        self._api.login(usuario, contrasenna, self.loginListener)

    def get_email(self):
        if not self._api.isLoggedIn():
            print('INFO: Not logged in')
        else:
            print self._api.getMyEmail()
            # webSocket.write_message(email)

    def is_logged(self):
        is_logged = False
        if self._api.isLoggedIn():
            is_logged = True
        data = {
            'cmd': 'isLogged',
            'status': is_logged
        }
        enviar_cliente(self.web_socket_handler, data)

    def listaNodos(self):
        #self._api.fetchNodes(self.listaNodosListener)

        self.cwd = self.listaNodosListener.cwd
        nodos = []
        if not self.cwd:
            self.cwd = self._api.getRootNode()
            self.listaNodosListener.cwd = self.cwd
        path = self.cwd

        dictNodo = {
            'nombre': '/',
            'tipo': 'F'
        }
        nodos.append(dictNodo)

        if self._api.getParentNode(path) != None:
            dictNodo = {
                'nombre': '..',
                'tipo': 'F'
            }
            nodos.append(dictNodo)
        nodes = self._api.getChildren(path)

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
        enviar_cliente(self.web_socket_handler, data)

    def cd(self, j_data):
        cwd = self.listaNodosListener.cwd
        dir = str(j_data['carpeta'])
        node = self._api.getNodeByPath(dir, cwd)
        if node == None:
            print('{}: No such file or directory'.format(dir))
            return
        if node.getType() == MegaNode.TYPE_FILE:
            print('{}: Not a directory'.format(dir))
            return
        cwd = node
        self.listaNodosListener.cwd = cwd
        self.listaNodos()
