from WebSocketServer.DataBase.RpiSqlite import abrir_conexion


def registrar_descarga(nombre_archivo):
    conexion = abrir_conexion()
    conexion.execute("INSERT INTO mega_descargas (nombre_archivo,Fecha) VALUES (?, current_date)", [nombre_archivo])
    conexion.commit()

def existe_descarga(nombre_archivo):
    conexion = abrir_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM mega_descargas WHERE nombre_archivo = ?", [nombre_archivo])
    data = cursor.fetchone()
    if data[0] > 0:
        return True
    return False
