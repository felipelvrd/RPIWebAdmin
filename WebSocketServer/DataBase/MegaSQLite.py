from WebSocketServer.DataBase.RpiSqlite import abrir_conexion


def registrar_descarga(uri_publico):
    conexion = abrir_conexion()
    conexion.execute("INSERT INTO mega_descargas (uri_publico, fecha) VALUES (?, current_date)", [uri_publico])
    conexion.commit()


def existe_descarga(uri_publico):
    conexion = abrir_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM mega_descargas WHERE uri_publico = ?", [uri_publico])
    data = cursor.fetchone()
    if data[0] > 0:
        return True
    return False
