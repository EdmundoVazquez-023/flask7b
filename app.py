


    # Codigo del profe a modifcarrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr


# python.exe -m venv .venv
# cd .venv/Scripts
# activate.bat
# py -m ensurepip --upgrade

from flask import Flask

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

# Código usado en las prácticas
def notificarActualizacionEncuesta():
    pusher_client = pusher.Pusher(
        app_id="1766032",
        key="e7b4efacf7381f83e05e",
        secret="134ff4754740b57ad585",
        cluster="us2",
        ssl=True

    )

    pusher_client.trigger("canalRegistroEncuesta", "registroEventoEncuests", args)

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_experiencias ORDER BY Id_Experiencia DESC")

    registros = cursor.fetchall()
    con.close()

    return registros

    return make_response(jsonify(registros))



@app.route("/guardar", methods=["POST"])
def guardar():
    if not con.is_connected():
        con.reconnect()

    id          = request.form["id"]
    nombreapellido = request.form["NombreApellido"]
    comentario     = request.form["Comentario"]
    calificacion     = request.form["Calificacion"]    
    cursor = con.cursor()

    if id:
        sql = """
        UPDATE tst0_experiencias SET
        Nombre_Apellido = %s,
        Comentario     = %s,
        Calificacion     = %s

        WHERE Id_Experiencia = %s
        """
        val = (nombreapellido, comentario, calificacion, id)
    else:
        sql = """
        INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion)
                        VALUES (%s,          %s,      %s       )
        """
        val =                  (nombreapellido, comentario, calificacion)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacionEncuesta()

    return make_response(jsonify({}))

@app.route("/editar/<int:id>", methods=["GET"])
def editar(id):
    if not con.is_connected():
        con.reconnect()

    id = request.args["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Experiencia, Nombre_Apellido, Comentario, Calificacion FROM tst0_experiencias
    WHERE Id_Experiencia = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    DELETE FROM tst0_experiencias
    WHERE Id_Experiencia = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacionEncuesta()

    return make_response(jsonify({}))





