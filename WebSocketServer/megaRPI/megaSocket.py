import json

from mega import MegaApi, MegaNode

from WebSocketServer.megaRPI.listener.loginListener import LoginListener
from WebSocketServer.megaRPI.listener.listener import AppListener
from WebSocketServer.megaRPI.listener.listaNodosListener import ListaNodosListener


class MegaSocket:
    def __init__(self, api, web_socket_handler):
        self._api = api
        self.webSocketHandler = web_socket_handler
        self.loginListener = LoginListener(self.webSocketHandler)
        self.listaNodosListener = ListaNodosListener(self.webSocketHandler)

    def login(self, usuario, contrasenna):
        self._api.login(str(usuario), str(contrasenna), self.loginListener)

    def get_email(self):
        if not self._api.isLoggedIn():
            print('INFO: Not logged in')
        else:
            print self._api.getMyEmail()
        #webSocket.write_message(email)

    def is_logged(self):
        is_logged = False
        if self._api.isLoggedIn():
            is_logged = True
        data = {
            'cmd': 'isLogged',
            'status': is_logged
        }
        j_data = json.dumps(data)
        self.webSocketHandler.write_message(j_data)

    def lista_nodos(self):
        self._api.fetchNodes(self.listaNodosListener)

    def recibidor(self, data):
        j_data = json.loads(data.decode('utf-8'))
        if j_data['cmd'] == 'login':
            self.login(j_data['email'], j_data['contrasenna'])
        if j_data['cmd'] == 'getEmail':
            self.get_email()
        if j_data['cmd'] == 'isLogged':
            self.is_logged()
        if j_data['cmd'] == 'listaNodos':
            self.lista_nodos()












