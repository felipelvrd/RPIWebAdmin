import json

from WebSocketServer.megaRPI.listener import LoginListener, ListaNodosListener


class MegaCliente:
    def __init__(self, api, web_socket_handler):
        self._api = api
        self.web_socket_handler = web_socket_handler
        self.loginListener = LoginListener(self.web_socket_handler)
        self.listaNodosListener = ListaNodosListener(self.web_socket_handler)

    def login(self, usuario, contrasenna):
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
        j_data = json.dumps(data)
        self.web_socket_handler.write_message(j_data)

    def lista_nodos(self):
        self._api.fetchNodes(self.listaNodosListener)

    def enrutador(self, data):
        pass
