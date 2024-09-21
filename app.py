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

    
    return f"Nombre {nombreapellido} Comentario {comentario} Calificacion {calificacion}"

@app.route("/evento")
def evento():
    pusher_client = pusher.Pusher(
       app_id = "1766032"
       key = "e7b4efacf7381f83e05e"
       secret = "134ff4754740b57ad585"
       cluster = "us2"
        ssl=True
    )
    
    pusher_client.trigger("my-channel", "my-event", {})
