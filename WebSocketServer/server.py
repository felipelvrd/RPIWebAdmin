from tornado import web, ioloop

from WebSocketServer.webSocketHandlers import MegaWebSocketHandler

app = web.Application([
    (r'/mega', MegaWebSocketHandler)
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
