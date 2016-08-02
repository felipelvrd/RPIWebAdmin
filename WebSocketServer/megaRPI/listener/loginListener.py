from mega import MegaRequestListener, MegaError
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
