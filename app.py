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
@app.route("/form", methods=["POST"])
def registrar_experiencia():
    # Capturar datos del formulario
    nombre = request.form.get('name')
    comentario = request.form.get('comment')
    calificacion = request.form.get('rating')
    
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Consulta para insertar los datos
        query = "INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)"
        values = (nombre, comentario, calificacion)
        
        # Ejecutar la consulta
        cursor.execute(query, values)
        connection.commit()  # Asegura que los cambios se guarden

        # Cerrar la conexión
        cursor.close()
        connection.close()

        # Redirigir a una página de éxito o agradecimiento
        return redirect(url_for('agradecimiento'))

    except mysql.connector.Error as err:
        return f"Error: {err}"

# Ruta para la página de agradecimiento
@app.route("/agradecimiento")
def agradecimiento():
    return "<h1>Gracias por tu participación!</h1>"

if __name__ == "__main__":
    app.run(debug=True)

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

