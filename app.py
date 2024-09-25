from flask import Flask, render_template, request
import pusher
import mysql.connector
import pytz

con = mysql.connector.connect(
  host="185.232.14.52",
  database="u760464709_tst_sep",
  user="u760464709_tst_sep_usr",
  password="dJ0CIAFF="
)

app = Flask(__name__)

# Ruta principal que sirve una página de inicio
@app.route("/")
def index():
    return render_template("app.html")

# Ruta que sirve la página de alumnos
@app.route("/app")
def alumnos():
    return render_template("app.html")

# Ruta para guardar los datos de los alumnos enviados desde el formulario
@app.route("/app/guardar", methods=["POST"])
def alumnosGuardar():
    nombreapellido = request.form["name"]
    comentario = request.form["comment"]
    calificacion = request.form["rating"]

    # Devolviendo una respuesta con los datos recibidos
    return f"Nombre: {nombreapellido}, Comentario: {comentario}, Calificación: {calificacion}"
#buscar
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_experiencias ORDER BY Id_Experiencia DESC")

    registros = cursor.fetchall()
    con.close()

    return registros

# Ruta para manejar el formulario de registro
@app.route('/registrar', methods=['GET', 'POST'])
def registrarForm():
    msg = ''
    
    if request.method == 'POST':
        nombre = request.form['name']
        comentario = request.form['comment']
        calificacion = request.form['rating']
        
        # Conexión a la base de datos
        conexion_MySQLdb = connectionBD()
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        
        # Consulta para insertar los datos
        sql = "INSERT INTO tst0_experiencias(Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)"
        valores = (nombre, comentario, calificacion)
        
        # Ejecutar la consulta y hacer commit
        cursor.execute(sql, valores)
        conexion_MySQLdb.commit()
        
        # Cerrar cursor y conexión
        cursor.close()
        conexion_MySQLdb.close()

        msg = 'Registro con éxito'
        
        # Información adicional para depuración
        print(cursor.rowcount, "registro insertado")
        print("1 registro insertado, id", cursor.lastrowid)

        # Renderizar página con mensaje de éxito
        return render_template('public/app.html', msg='Formulario enviado con éxito')
    
    # Si se accede con GET, simplemente muestra el formulario
    else:
        return render_template('public/app.html', msg='Método HTTP incorrecto')

# Ruta que activa un evento de Pusher
@app.route("/evento")
def evento():
    # Conexión con Pusher utilizando las credenciales correctas
    pusher_client = pusher.Pusher(
        app_id="1766032",
        key="e7b4efacf7381f83e05e",
        secret="134ff4754740b57ad585",
        cluster="us2",
        ssl=True
    )

    # Disparando un evento a través de Pusher
    pusher_client.trigger("canalRegistroEncuesta", "registroEventoEncuests", args)
  #    pusher_client.trigger("my-channel", "my-event", args)

    
    return args

