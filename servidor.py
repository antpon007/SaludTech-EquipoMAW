
import mysql.connector
from modelo.conexion import conectarBD
from modelo.usuario import *
from modelo.medico import *
from modelo.categoria import *
from modelo.tarifa import *
from modelo.servicio import *
from mysql.connector import errorcode

app = Flask(__name__)

# pagina principal
@app.route("/<nombre>")
@app.route("/")
def iniciar_app(nombre="invitado"):
    contexto = {'nombre':nombre}
    return render_template("index.html",**contexto)

##--------------------
###Gestor de consultas
##--------------------

# lista de categorias
@app.route("/categoria")
def listar_categoria():
    try:
        return listar_categorias()
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)
        
# lista de tarifas
@app.route("/tarifa")
def listar_tarifa():
    try:
        return listar_tarifas()
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)
        
# lista de servicios
@app.route("/servicio")
def listar_servicio():
    try:
        return listar_servicios()
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)

# lista de usuarios
@app.route("/usuario")
def listar_usuarios():
    return listar_usuario()

##--------------------
###Gestor de usuarios
##--------------------

# registro de usuarios
@app.route('/registro',methods=['POST'])
def signUp():
    try:
        # read the posted values from the UI
        _usuario = request.form['usuario']
        _email = request.form['email']
        _clave = request.form['clave']
        _tipo = 0 #representa usuarios del común
        return registro_usuario(_usuario,_email,_clave,_tipo)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)

# registro de medicos
@app.route('/registro/medico',methods=['POST'])
def crearMedico():
    try:
        # read the posted values from the UI
        _primerNombre = request.form['primerNombre']
        _segundoNombre = request.form['segundoNombre']
        _primerApellido = request.form['primerApellido']
        _segundoApellido = request.form['segundoApellido']
        _documento = request.form['documento']
        _especialidad = request.form['especialidad']
        _fechaNacimiento = request.form['fechaNacimiento'] #enviarlo en formato AAAA-MM-DD
        
        return crear_medico(_primerNombre,_segundoNombre,_primerApellido,_segundoApellido,_documento,_especialidad,_fechaNacimiento)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)

# registro de usuarios medicos
@app.route('/registro/medico/usuario',methods=['POST'])
def signUpMedico():
    try:
        # read the posted values from the UI
        _usuario = request.form['usuario']
        _email = request.form['email']
        _clave = request.form['clave']
        _tipo = 1 #representa usuarios médicos
        _claveAdmin = request.form['claveAdmin']
               
        # validate the received values
        if _usuario and _email and _clave and _tipo:
            if verificarAdmin(_claveAdmin) == True:
                return registro_usuario(_usuario,_email,_clave,_tipo)
            else:
                return json.dumps({'mensaje':'Registro fallido, clave de administrador incorrecta!','respuesta':'CI'}, sort_keys=True)            
        else:
            return json.dumps({'mensaje':'Falta información!','respuesta':'FI'}, sort_keys=True)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)

#inicio de sesión
@app.route('/ingreso',methods=['POST'])
def signIn():
    try:
        # read the posted values from the UI
        _usuario = request.form['usuario']
        _clave = request.form['clave']
        return ingreso_usuario(_usuario,_clave)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)

##--------------------
###Gestor de configuración
##--------------------

# creación de servicios
@app.route('/servicio/crear',methods=['POST'])
def crearServicio():
    try:
        # read the posted values from the UI
        _idCategoria = request.form['idCategoria']
        _descripcion = request.form['descripcion']
        
        return crear_servicio(_idCategoria,_descripcion)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)

# creación de tarifas
@app.route('/tarifa/crear',methods=['POST'])
def crearTarifa():
    try:
        # read the posted values from the UI
        _idServicio = request.form['idServicio']
        _idMedico = request.form['idMedico']
        _precio = request.form['precio']
        return crear_tarifa(_idServicio,_idMedico,_precio)
    except Exception as e:
        return json.dumps({'mensaje':str(e),'respuesta':'ER'}, sort_keys=True)

##--------------------
###verifica conexión BD
##--------------------
try:
  conectarBD()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Por favor corrige la información de usuario o contraseña")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Base de datos no existe")
  else:
    print(err)
else:
    print("conexión exitosa")
    app.run(debug=True)








