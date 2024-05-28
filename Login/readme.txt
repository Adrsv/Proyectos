Debe ejecutar el siguiente comando para poder crear la base de datos con su respectiva tabla para que funcione el programa.

CREATE DATABASE login CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE login;
CREATE TABLE usuariospass (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    gmail VARCHAR(40) NOT NULL,    
    pass VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

El archivo config.py debe ser modificado con los valores que tenga en su gestor de base de datos.
    MYSQL_HOST = '*host'
    MYSQL_USER = '*usuario'
    MYSQL_PASSWORD = '*contraseña'

Tambien debe de instalar los requerimientos necesarios en el documento requirements.txt.
pip install -r requirements.txt

Por ultimo ejecutar el archivo run.py y probar si funciona todo correctamente.
python .\run.py