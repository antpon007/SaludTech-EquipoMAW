import mysql.connector

def conectarBD():
    return mysql.connector.MySQLConnection(user='root', password='901011',
                                 host='localhost',
                                 database='saludtech')