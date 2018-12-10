import mysql.connector
from modelo.conexion import conectarBD
from flask import Flask, render_template, json, request, jsonify
from werkzeug import generate_password_hash, check_password_hash

def listar_usuario():
    try:
        conn =conectarBD()
        cursor = conn.cursor()
        cursor.callproc('sp_listarUsuario')
        for result in cursor.stored_results():
            rv = result.fetchall()
        
        payload = []
        content = {}
        for result in rv:
            content = {'idUsuario': result[0], 'nombre': result[1],'email': result[2], 'tipo': result[3]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)
    finally:
        cursor.close() 
        conn.close()

def registro_usuario(_usuario,_email,_clave,_tipo):
    try:
        conn = conectarBD()
        cursor = conn.cursor()
        # validate the received values
        if _usuario and _email and _clave :
            # All Good, let's call MySQL
            _hashed_password = generate_password_hash(_clave)
            cursor.callproc('sp_crearUsuario',(_usuario,_email,_hashed_password,_tipo))
            conn.commit()
            return json.dumps({'mensaje':'Registro satisfactorio!','respuesta':'OK'}, sort_keys=True)
                            
        else:
            return json.dumps({'mensaje':'Falta información!','respuesta':'FI'}, sort_keys=True)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)
    finally:
        cursor.close() 
        conn.close()


def ingreso_usuario(_usuario,_clave):
    try:
        conn = conectarBD()
        cursor = conn.cursor() 
        # validate the received values
        if _usuario and _clave:
            args = [_usuario,0,1]
            result_args = cursor.callproc('sp_verificarUsuario', args)
            if (result_args[1] != None):
                if (check_password_hash(result_args[2], _clave) == True):
                    return json.dumps({'mensaje':'Bienvenido {}!'.format(_usuario),
                                    'respuesta':'OK'}, sort_keys=True)
                else:
                    return json.dumps({'mensaje':'clave invalida!',
                                    'respuesta':'DI'}, sort_keys=True)
            else:
                return json.dumps({'mensaje':'Usuario no existe!',
                                    'respuesta':'UI'}, sort_keys=True)
        else:
            return json.dumps({'mensaje':'Falta información!',
                               'respuesta':'FI'}, sort_keys=True)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)
    finally:
        cursor.close() 
        conn.close()

def verificarAdmin(_claveAdmin):
    _usuarioAdmin='admin'
    con = conectarBD()
    cursor = con.cursor()
    args = [_usuarioAdmin,0,1]
    result_args = cursor.callproc('sp_verificarUsuario', args)
    if (result_args[1] != None) and (check_password_hash(result_args[2], _claveAdmin) == True):
        return True
    else:
        return False
