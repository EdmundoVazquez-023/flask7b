from flask import Flask, render_template, request
import pusher

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
    pusher_client.trigger("my-channel", "my-event", {"message": "Evento enviado correctamente"})
    
    return "Evento enviado correctamente"

# Arrancando la aplicación
if __name__ == "__main__":
    app.run(debug=True)
