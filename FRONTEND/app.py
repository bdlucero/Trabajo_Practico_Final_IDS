from flask import Flask, render_template, redirect, url_for, request, session
import os, requests
from functools import wraps

app = Flask(__name__, static_folder="static", template_folder="templates")

#  CONFIGURACIÓN lOGUEO
app.secret_key = "clave_super_secreta_para_sesiones"
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:5050")
GOOGLE_CLIENT_ID = "469004002801-logurlhvbb0e682h0rfesar7vtl6f0o0.apps.googleusercontent.com"


# OBLIGAR A REGISTRARSE

def login_required(view_func):
    """Redirige a /registro si no hay usuario en sesión."""
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("registro"))
        return view_func(*args, **kwargs)
    return wrapped_view


#  RUTAS 

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
@login_required
def buscar():
    user = session.get("user")
    materias = []
    try:
        resp = requests.get(f"{BACKEND_URL}/api/materias", timeout=5)
        resp.raise_for_status()
        materias = resp.json()
    except Exception as e:
        print("Error al obtener materias del backend:", e)

    return render_template(
        "busqueda.html",
        materias=materias,
        backend_url=BACKEND_URL,
        user=user,
    )
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("buscar"))

@app.route("/resenas", methods=["GET", "POST"])
def resenas():
    user = session.get("user")

    materias = []
    error = None
    mensaje = None

    try:
        resp = requests.get(f"{BACKEND_URL}/api/materias", timeout=5)
        resp.raise_for_status()
        materias = resp.json()
    except Exception as e:
        print("Error al obtener materias del backend:", e)
        error = "No se pudieron cargar las materias."

    if request.method == "POST":
        form = request.form

        asignatura = (form.get("asignatura"))
        nombre = (form.get("nombre"))
        titulo_resena = (form.get("titulo_resena"))
        resena_texto = (form.get("resena"))
        satisfaccion = (form.get("satisfaccion"))

        if not asignatura or not nombre or not resena_texto or not satisfaccion:
            error = "Completá todos los campos obligatorios."
        else:
            comentario = f"{titulo_resena}\n{resena_texto}"

            try:
                puntuacion_int = int(satisfaccion)
            except ValueError:
                error = "La satisfacción debe ser un número entre 1 y 5."
                return render_template(
                    "resenas.html",
                    materias=materias,
                    user=user,
                    error=error,
                    mensaje=mensaje,
                )

            id_usuario = user.get("legajo")

            info_resenas = {
                "id_materia": asignatura,       
                "comentario": comentario,
                "puntuacion": puntuacion_int,
                "id_usuario": id_usuario,      
            }

            try:
                api_resp = requests.post(
                    f"{BACKEND_URL}/api/resenas_cursos",
                    json=info_resenas,
                    timeout=10,
                )

            except requests.RequestException as e:
                print("Error al llamar a /api/resenas_cursos:", e)
                error = "No se pudo guardar la reseña."

    return render_template(
        "resenas.html",
        materias=materias,
        user=user,
        error=error,
        mensaje=mensaje,
        api_resp=api_resp
    )

@app.route('/publicaciones')
def publicaciones():
    return render_template('publicaciones.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
