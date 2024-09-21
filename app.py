from flask import Flask

from flask import render_template
from flask import request

import pusher

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    nombreapellido      = request.form["name"]
    comentario = request.form["comment"]
    calificacion = request.form["rating"]

    
    return f"Nombre {nombreapellido} Comentario {commentario} Calificacion {calificacion}"

@app.route("/evento")
def evento():
    pusher_client = pusher.Pusher(
        app_id="1714541",
        key="cda1cc599395d699a2af",
        secret="9e9c00fc36600060d9e2",
        cluster="us2",
        ssl=True
    )
    
    pusher_client.trigger("my-channel", "my-event", {})
