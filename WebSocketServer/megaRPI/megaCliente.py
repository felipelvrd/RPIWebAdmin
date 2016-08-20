from WebSocketServer.megaRPI.listener import LoginListener, MegaNode
from WebSocketServer.megaRPI.utils import enviar_cliente
from WebSocketServer.megaRPI.megaNodosManager import MegaNodosManager

class MegaCliente(object):
    def __init__(self, api, web_socket_handler):
        self._api = api
        self.web_socket_handler = web_socket_handler
        self.loginListener = LoginListener(self.web_socket_handler)
        self.mega_nodos_manager = MegaNodosManager(self._api, self.web_socket_handler)



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

    def esta_logueado(self):
        if self._api.isLoggedIn():
            return True
        data = {
            'cmd': 'no_logueado'
        }
        enviar_cliente(self.web_socket_handler, data)
        return False

    def listaNodos(self):
        #self._api.fetchNodes(self.listaNodosListener)
        if self.esta_logueado():
            self.mega_nodos_manager.ListarNodos()
            pass

    def cd(self, j_data):
        dir = str(j_data['carpeta'])
        self.mega_nodos_manager.CambiarNodo(dir)

