desde flask importar Flask, render_template, solicitud, jsonify, make_response
importar mysql.connector
empujador de importación
registro de importación

# Configura el registrador de Flask
registro.basicConfig(nivel=registro.INFO)

# Conexión a la base de datos
con = mysql.connector.connect(
anfitrión="185.232.14.52",
base de datos="u760464709_tst_sep",
usuario="u760464709_tst_sep_usr",
contraseña="dJ0CIAFF="
)

aplicación = Flask(__nombre__)

# Página principal que carga el CRUD de experiencias
@app.ruta("/")
definición índice():
logging.info ("Cargando página principal")
con.cerrar()
devolver render_template("app.html")

# Crear o actualizar una experiencia
@app.route("/experiencias/guardar", métodos=["POST"])
def experienciasGuardar():
Si no es con.is_connected():
con.reconectar()

id_experiencia = request.form.get("id_experiencia")
nombre_apellido = request.form["nombre_apellido"]
comentario = solicitud.formulario["comentario"]
calificacion = solicitud.formulario["calificacion"]

cursor = con.cursor()
if id_experiencia:#Actualizar
sql = """
ACTUALIZAR tst0_experiencias SET Nombre_Apellido = %s, Comentario = %s, Calificacion = %s WHERE Id_Experiencia = %s
"""
val = (nombre_apellido, comentario, calificación, id_experiencia)
logging.info (f"Actualizando experiencia con ID: {id_experiencia}")
más: # Crear nueva experiencia
sql = """
INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion) VALORES (%s, %s, %s)
"""
val = (nombre_apellido, comentario, calificación)
logging.info (f"Creando nueva experiencia: {nombre_apellido}")

cursor.execute(sql, val)
con.commit()
cursor.cerrar()
con.cerrar()

notificación_actualizacion_experiencias()

return make_response(jsonify({"message": "Experiencia guardada exitosamente"}))

# Obtener todas las experiencias
@app.route("/experiencias", métodos=["GET"])
def obtener_experiencias():
Si no es con.is_connected():
con.reconectar()

cursor = con.cursor(diccionario=Verdadero)
cursor.execute("SELECT * FROM tst0_experiencias")
experiencias = cursor.fetchall()
cursor.cerrar()
con.cerrar()

logging.info ("Obteniendo lista de experiencias")
devuelve make_response(jsonify(experiencias))

# Obtener una experiencia por su ID sin usar query string
@app.route("/experiencias/editar/<int:id_experiencia>", métodos=["GET"])
def editar_experiencia(id_experiencia):
Si no es con.is_connected():
con.reconectar()

cursor = con.cursor(diccionario=Verdadero)
sql = "SELECT * FROM tst0_experiencias WHERE Id_Experiencia = %s"
val = (id_experiencia,)
cursor.execute(sql, val)
experiencia = cursor.fetchone()
cursor.cerrar()
con.cerrar()

logging.info (f"Obteniendo datos de la experiencia con ID: {id_experiencia}")
devuelve make_response(jsonify(experiencia))

# Eliminar una experiencia usando el ID en la URL
@app.route("/experiencias/eliminar/<int:id_experiencia>", métodos=["POST"])
def eliminar_experiencia(id_experiencia):
logging.info (f"Intentando eliminar la experiencia con ID: {id_experiencia}")

Si no es con.is_connected():
con.reconectar()

cursor = con.cursor()
sql = "BORRAR DE tst0_experiencias DONDE Id_Experiencia = %s"
val = (id_experiencia,)
cursor.execute(sql, val)
con.commit()
cursor.cerrar()
con.cerrar()

notificación_actualizacion_experiencias()

logging.info (f"Experiencia con ID {id_experiencia} eliminada exitosamente.")
return make_response(jsonify({"message": "Experiencia eliminada exitosamente"}))

# Notificar a través de Pusher sobre actualizaciones en la tabla de experiencias
def notificación_actualizacion_experiencias():
pusher_client = pusher.Pusher(
aplicación_id="1766032",
clave="e7b4efacf7381f83e05e",
secreto="134ff4754740b57ad585",
grupo="us2",
ssl=Verdadero
)
pusher_client.trigger("canalExperiencias", "actualizacion", {})
logging.info ("Notificación enviada a través de Pusher")

si __nombre__ == "__principal__":
aplicación.run(debug=Verdadero)
