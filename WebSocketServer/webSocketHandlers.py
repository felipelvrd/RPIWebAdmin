from tornado.websocket import WebSocketHandler
from WebSocketServer.megaRPI.megaServer import MegaServer

mega_server = MegaServer()


class MegaWebSocketHandler(WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(MegaWebSocketHandler, self).__init__(*args, **kwargs)

    def data_received(self, chunk):
        pass

    def open(self):
        mega_cliente = mega_server.agregar_cliente(self)
        mega_cliente.lista_nodos()
        print("WebSocket opened")

    def on_message(self, message):
        mega_server.enrutador(self, message)

    def on_close(self):
        mega_server.eliminar_cliente(self)
        print("WebSocket closed")

    def check_origin(self, origin):
        return True
