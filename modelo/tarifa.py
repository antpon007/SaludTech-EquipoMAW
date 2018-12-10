import mysql.connector
from modelo.conexion import conectarBD
from flask import Flask, render_template, json, request, jsonify


def listar_tarifas():
    try:
        conn =conectarBD()
        cursor = conn.cursor()
        cursor.callproc('sp_listarTarifa')
        for result in cursor.stored_results():
            rv = result.fetchall()
        
        payload = []
        content = {}
        for result in rv:
            content = {'idtarifa': result[0], 'descripcion': result[1],'Médico': result[2], 'Precio': result[3]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)
    finally:
        cursor.close() 
        conn.close()


def crear_tarifa(_idServicio,_idMedico,_precio):
    try:
        conn = conectarBD()
        cursor = conn.cursor()
        # validate the received values
        if _idServicio and _idMedico and _precio:
            # All Good, let's call MySQL
            cursor.callproc('sp_crearTarifa',(_idServicio,_idMedico,_precio))
            conn.commit()
            return json.dumps({'mensaje':'Registro satisfactorio!','respuesta':'OK'}, sort_keys=True)           
        else:
            return json.dumps({'mensaje':'Falta información!','respuesta':'FI'}, sort_keys=True)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)
    finally:
        cursor.close() 
        conn.close()