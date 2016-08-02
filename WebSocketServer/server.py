from tornado import web, ioloop
from tornado.websocket import WebSocketHandler
from WebSocketServer.megaRPI.megaSocket import MegaSocket
from mega import MegaApi

_api = MegaApi('oowWWYRZ', None, None, 'megaRPI')


class MegaWebSocketHandler(WebSocketHandler):
    def __init__(self, *args, **kwargs):
        global _api
        self.megaRPI = MegaSocket(_api, self)
        self.isOpen = False
        super(MegaWebSocketHandler, self).__init__(*args, **kwargs)

    def data_received(self, chunk):
        pass

    def open(self):
        self.isOpen = True
        print("WebSocket opened")

    def on_message(self, message):
        self.megaRPI.recibidor(message)

    def on_close(self):
        self.isOpen = False
        print("WebSocket closed")

    def check_origin(self, origin):
        return True


app = web.Application([
    (r'/mega', MegaWebSocketHandler)
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
