from tornado import web, ioloop
from tornado.websocket import WebSocketHandler
from WebSocketServer.megaRPI.megaSocket import MegaSocket

megaRPI = MegaSocket()

cli = []

class MegaWebSocket(WebSocketHandler):
    def open(self):
        #global megaRPI
        #megaRPI.recibidor(self)
        cli.append(self)
        print("WebSocket opened")

    def on_message(self, message):
        global megaRPI
        megaRPI.recibidor(self, message)
        #self.write_message(message)

    def on_close(self):
        cli.remove(self)
        print("WebSocket closed")

    def check_origin(self, origin):
        return True


app = web.Application([
    (r'/mega', MegaWebSocket)
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
