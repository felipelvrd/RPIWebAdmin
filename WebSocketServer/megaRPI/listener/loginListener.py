from mega import MegaRequestListener, MegaError
import json


class LoginListener(MegaRequestListener):
    def __init__(self, webSocket, cli):
        super(LoginListener, self).__init__()
        self.webSocket = webSocket
        self.cli = cli

    def onRequestFinish(self, api, request, e):
        data = {
            'cmd': 'login',
            'errorCode': e.getErrorCode(),
            'errorString': MegaError.getErrorString(e.getErrorCode()),
        }
        jData = json.dumps(data)
        self.webSocket.write_message(jData)
        self.cli.remove(self)
