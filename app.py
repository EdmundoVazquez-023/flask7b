from flask import Flask
from flask_cors import CORS, cross_origin #linea nueva

from flask import render_template
from flask import request
from flask import jsonify, make_response

import pusher

import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)
CORS(app) #linea nueva

@app.route("/")
def index():
    con.close()

    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    con.close()

    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]

    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"


# Función para enviar notificación de actualización
def notificarActualizacionEncuesta():
    pusher_client = pusher.Pusher(
        app_id="1766032",
        key="e7b4efacf7381f83e05e",
        secret="134ff4754740b57ad585",
        cluster="us2",
        ssl=True
    )
    pusher_client.trigger("canalRegistroEncuesta", "registroEventoEncuesta", {})

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnos_guardar():
    matricula = request.form.get("txtMatriculaFA") or request.json.get("txtMatriculaFA")
    nombreapellido = request.form.get("txtNombreApellidoFA") or request.json.get("txtNombreApellidoFA")
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_experiencias ORDER BY Id_Experiencia DESC")
    registros = cursor.fetchall()
    con.close()
    return make_response(jsonify(registros))

@app.route("/guardar", methods=["POST"])
def guardar():
    if not con.is_connected():
        con.reconnect()

    # Obtener los datos ya sea de `form` o de `json`
    id = request.form.get("id") or request.json.get("id")
    nombreapellido = request.form.get("NombreApellido") or request.json.get("NombreApellido")
    comentario = request.form.get("Comentario") or request.json.get("Comentario")
    calificacion = request.form.get("Calificacion") or request.json.get("Calificacion")

    cursor = con.cursor()

    if id:
        sql = """
        UPDATE tst0_experiencias SET
        Nombre_Apellido = %s,
        Comentario = %s,
        Calificacion = %s
        WHERE Id_Experiencia = %s
        """
        val = (nombreapellido, comentario, calificacion, id)
    else:
        sql = """
        INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion)
        VALUES (%s, %s, %s)
        """
        val = (nombreapellido, comentario, calificacion)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()
    notificarActualizacionEncuesta()

    return make_response(jsonify({}))

@app.route("/editar", methods=["GET"])
def editar():
    if not con.is_connected():
        con.reconnect()

    # `id` se pasa en los parámetros de consulta
    id = request.args.get("id_experiencia")

    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT Id_Experiencia, Nombre_Apellido, Comentario, Calificacion 
    FROM tst0_experiencias
    WHERE Id_Experiencia = %s
    """
    cursor.execute(sql, (id,))
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/eliminar", methods=["POST"])
def eliminar():
    if not con.is_connected():
        con.reconnect()

    # Obtener `id` ya sea de `form` o de `json`
    id = request.form.get("id_experiencia") or request.json.get("id_experiencia")

    cursor = con.cursor()
    sql = "DELETE FROM tst0_experiencias WHERE Id_Experiencia = %s"
    cursor.execute(sql, (id,))
    con.commit()
    con.close()
    notificarActualizacionEncuesta()

    return make_response(jsonify({}))
