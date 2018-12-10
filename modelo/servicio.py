import mysql.connector
from modelo.conexion import conectarBD
from flask import Flask, render_template, json, request, jsonify


def listar_servicios():
    try:
        conn =conectarBD()
        cursor = conn.cursor()
        cursor.callproc('sp_listarServicio')
        for result in cursor.stored_results():
            rv = result.fetchall()
        
        payload = []
        content = {}
        for result in rv:
            content = {'idServicio': result[0], 'descripcion': result[1], 'idCategoria': result[2],}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)
    finally:
        cursor.close() 
        conn.close()


def crear_servicio(_idCategoria,_descripcion):
    try:
        conn = conectarBD()
        cursor = conn.cursor()
        # validate the received values
        if _idCategoria and _descripcion:
            # All Good, let's call MySQL
            cursor.callproc('sp_crearServicio',(_idCategoria,_descripcion))
            conn.commit()
            return json.dumps({'mensaje':'Registro satisfactorio!','respuesta':'OK'}, sort_keys=True)           
        else:
            return json.dumps({'mensaje':'Falta información!','respuesta':'FI'}, sort_keys=True)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)
    finally:
        cursor.close() 
        conn.close()