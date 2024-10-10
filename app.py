from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import pusher
import logging

# Configura el logger de Flask
logging.basicConfig(level=logging.INFO)

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Página principal que carga el CRUD de experiencias
@app.route("/")
def index():
    logging.info("Cargando página principal")
    con.close()
    return render_template("app.html")

# Crear o actualizar una experiencia
@app.route("/guardar", methods=["POST"])
def experienciasGuardar():
    if not con.is_connected():
        con.reconnect()

    id_experiencia = request.form.get("id_experiencia")
    nombre_apellido = request.form["nombre_apellido"]
    comentario = request.form["comentario"]
    calificacion = request.form["calificacion"]

    cursor = con.cursor()
    if id_experiencia:  # Actualizar
        sql = """
        UPDATE tst0_experiencias SET Nombre_Apellido = %s, Comentario = %s, Calificacion = %s WHERE Id_Experiencia = %s
        """
        val = (nombre_apellido, comentario, calificacion, id_experiencia)
        logging.info(f"Actualizando experiencia con ID: {id_experiencia}")
    else:  # Crear nueva experiencia
        sql = """
        INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)
        """
        val = (nombre_apellido, comentario, calificacion)
        logging.info(f"Creando nueva experiencia: {nombre_apellido}")

    cursor.execute(sql, val)
    con.commit()
    cursor.close()
    con.close()

    notificar_actualizacion_experiencias()

    return make_response(jsonify({"message": "Experiencia guardada exitosamente"}))

# Obtener todas las experiencias
@app.route("/experiencias", methods=["GET"])
def obtener_experiencias():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_experiencias")
    experiencias = cursor.fetchall()
    cursor.close()
    con.close()

    logging.info("Obteniendo lista de experiencias")
    return make_response(jsonify(experiencias))

# Obtener una experiencia por su ID sin usar query string
@app.route("/editar/<int:id_experiencia>", methods=["GET"])
def editar_experiencia(id_experiencia):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql = "SELECT * FROM tst0_experiencias WHERE Id_Experiencia = %s"
    val = (id_experiencia,)
    cursor.execute(sql, val)
    experiencia = cursor.fetchone()
    cursor.close()
    con.close()

    logging.info(f"Obteniendo datos de la experiencia con ID: {id_experiencia}")
    return make_response(jsonify(experiencia))

# Eliminar una experiencia usando el ID en la URL
@app.route("/eliminar/<int:id_experiencia>", methods=["POST"])
def eliminar_experiencia(id_experiencia):
    logging.info(f"Intentando eliminar la experiencia con ID: {id_experiencia}")
   
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "DELETE FROM tst0_experiencias WHERE Id_Experiencia = %s"
    val = (id_experiencia,)
    cursor.execute(sql, val)
    con.commit()
    cursor.close()
    con.close()

    notificar_actualizacion_experiencias()

    logging.info(f"Experiencia con ID {id_experiencia} eliminada exitosamente.")
    return make_response(jsonify({"message": "Experiencia eliminada exitosamente"}))

# Notificar a través de Pusher sobre actualizaciones en la tabla de experiencias
def notificar_actualizacion_experiencias():
    pusher_client = pusher.Pusher(
        app_id="1766032",
        key="e7b4efacf7381f83e05e",
        secret="134ff4754740b57ad585",
        cluster="us2",
        ssl=True
    )
    pusher_client.trigger("canalExperiencias", "actualizacion", {})
    logging.info("Notificación enviada a través de Pusher")

if __name__ == "__main__":
    app.run(debug=True)
