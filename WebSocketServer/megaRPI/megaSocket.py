import json

from mega import MegaApi

from WebSocketServer.megaRPI.listener.loginListener import LoginListener


class MegaSocket:
    def __init__(self):
        self._api = MegaApi('oowWWYRZ', None, None, 'Python megacli')
        self.cli = []

    def login(self, usuario, contrasenna, webSocket):
        loginListener = LoginListener(webSocket, self.cli)
        self.cli.append(loginListener)
        self._api.login(str(usuario), str(contrasenna), loginListener)

    def getEmail(self,webSocket):
        if not self._api.isLoggedIn():
            print('INFO: Not logged in')
        else:
            print self._api.getMyEmail()
        #webSocket.write_message(email)

    def isLogged(self, webSocket):
        islogged = False
        if self._api.isLoggedIn():
            islogged = True
        data = {
            'cmd': 'isLogged',
            'status': islogged
        }
        jData = json.dumps(data)
        webSocket.write_message(jData)


    def recibidor(self, webSocket, data):
        jData = json.loads(data.decode('utf-8'))
        if jData['cmd'] == 'login':
            self.login(jData['email'], jData['contrasenna'], webSocket)
        if jData['cmd'] == 'getEmail':
            self.getEmail(webSocket)
        if jData['cmd'] == 'isLogged':
            self.isLogged(webSocket)










