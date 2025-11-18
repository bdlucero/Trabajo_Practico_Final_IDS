from flask import Flask, render_template, redirect, url_for, request, session
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# ===== CONFIGURACIÓN =====
app.secret_key = "clave_super_secreta_para_sesiones"
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:5001")
GOOGLE_CLIENT_ID = "469004002801-logurlhvbb0e682h0rfesar7vtl6f0o0.apps.googleusercontent.com"

# ===== RUTAS =====

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'),404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error500.html'),500

@app.route("/")
def home():
    usuario = {"nombre": "Usuario"}
    estadisticas = [
        {"valor": "+1200", "descripcion": "Ofertas publicadas"},
        {"valor": "+800", "descripcion": "Estudiantes registrados"},
        {"valor": "+300", "descripcion": "Reseñas de materias"},
    ]
    resenas = obtener_ultimas_resenas()
    return render_template("home.html",
                        usuario=usuario,
                        estadisticas=estadisticas,
                        resenas=resenas)

def obtener_ultimas_resenas():
    return [
        {"materia": "Álgebra I", "comentario": "Muy buen enfoque del profe", "autor": "Lucía"},
        {"materia": "Física II", "comentario": "Explicaciones claras pero parciales exigentes", "autor": "Tomás"},
        {"materia": "Análisis Matemático", "comentario": "Excelente material complementario", "autor": "Sofía"},
    ]


@app.route("/buscar")
def buscar():
    materias = []
    user = session.get("user")  # recupera el usuario logueado
    return render_template("busqueda.html",
                        materias=materias,
                        backend_url=BACKEND_URL,
                        user=user)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        legajo = request.form.get("legajo", "").strip()
        email = request.form.get("email", "").strip()

        if not legajo or not email:
            return render_template("registro.html",
                                   google_client_id=GOOGLE_CLIENT_ID,
                                   error="Debes ingresar tu legajo y usar una cuenta institucional.")

        # Guarda el usuario en sesión
        session["user"] = {"nombre": email.split("@")[0], "email": email, "legajo": legajo}
        return redirect(url_for("buscar"))

    return render_template("registro.html", google_client_id=GOOGLE_CLIENT_ID)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("buscar"))

@app.route("/resenas")
def resenas():
    return render_template("resenas.html")

@app.route('/publicaciones')
def publicaciones():
    return render_template('publicaciones.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
