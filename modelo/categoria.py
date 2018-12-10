import mysql.connector
from modelo.conexion import conectarBD
from flask import Flask, render_template, json, request, jsonify

def listar_categorias():
    try:
        conn =conectarBD()
        cursor = conn.cursor()
        cursor.callproc('sp_listarCategoria')
        for result in cursor.stored_results():
            rv = result.fetchall()
        
        payload = []
        content = {}
        for result in rv:
            content = {'idCategoria': result[0], 'descripcion': result[1]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)
    finally:
        cursor.close() 
        conn.close()