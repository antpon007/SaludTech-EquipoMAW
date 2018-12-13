import mysql.connector
from modelo.conexion import conectarBD
from flask import Flask, render_template, json, request, jsonify
import datetime

def listar_medico():
    try:
        conn =conectarBD()
        cursor = conn.cursor()
        cursor.callproc('sp_listarMedico')
        for result in cursor.stored_results():
            rv = result.fetchall()
        
        payload = []
        content = {}
        for result in rv:
            content = {'idMedico': result[0], 'nombreCompleto': result[1],
                       'documento': result[2], 'idCategoria': result[3], 
                       'descripcionCategoria': result[4], 'fechaNacimiento': result[5]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)
    finally:
        cursor.close() 
        conn.close()


def crear_medico(_primerNombre,_segundoNombre,_primerApellido,_segundoApellido,_documento,_especialidad,_fechaNacimiento):
    try:
        conn = conectarBD()
        cursor = conn.cursor()
        # validate the received values
        if _primerNombre and _segundoNombre and _primerApellido and _segundoApellido and _documento and _especialidad and _fechaNacimiento:
            # All Good, let's call MySQL
            cursor.callproc('sp_crearMedico',(_primerNombre, _segundoNombre, _primerApellido, _segundoApellido, _documento, _especialidad, _fechaNacimiento))
            conn.commit()
            return json.dumps({'mensaje':'Registro satisfactorio!','respuesta':'OK'}, sort_keys=True)           
        else:
            return json.dumps({'mensaje':'Falta información!','respuesta':'FI'}, sort_keys=True)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)
    finally:
        cursor.close() 
        conn.close()