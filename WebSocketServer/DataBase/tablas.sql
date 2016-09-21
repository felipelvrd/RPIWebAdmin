--------------------------------------
--  Tablas para la aplicación MEGA  --
--------------------------------------

-- Log de descargas completadas
CREATE TABLE mega_descargas
(
    ID INTEGER PRIMARY KEY,
    URI_PUBLICO TEXT NOT NULL,
    FECHA DATETIME NOT NULL
);

-- Parámetros para la app MEGA
CREATE TABLE mega_parametros
(
    ID INTEGER PRIMARY KEY,
    CLAVE TEXT NOT NULL UNIQUE,
    VALOR TEXT NOT NULL
);
