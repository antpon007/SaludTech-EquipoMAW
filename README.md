# SaludTech-EquipoMAW

Pasos iniciales:
----------
descargar pyhton e instalarlo:

https://www.python.org/downloads/

seleccionar opcion (check) add patch al momento de la instalación

desde la consola de python o de comando ejecutar: 

+ pip install flask
+ pip install pymysql (creo que este no sirve)
+ pip install mysql-connector (o descargarlo desde: https://dev.mysql.com/downloads/connector/python/)
+ pip install Flask-Cors

importar Bd mysql saludtech.sql que se encuentra dentro de la carpeta del proyecto

+ cambiar los datos de conexión en el archivo: conexion.py dentro de la carpeta modelo

ejecutar desde la ruta del proyecto:

+ python servidor.py
