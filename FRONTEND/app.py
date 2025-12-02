from flask import Flask, Response, abort, render_template, redirect, url_for, request, session
import os, requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from functools import wraps
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")

#  CONFIGURACIÓN lOGUEO
app.secret_key = os.environ.get("SECRET_KEY")
BACKEND_URL = os.environ.get("BACKEND_URL")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")


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
    usuario = session.get("user") or {}
    reseñas = []
    estadisticas = []

    try:
        resp = requests.get(f"{BACKEND_URL}/api/home/resenas", timeout=5)
        if resp.status_code == 200:
            reseñas = resp.json()
    except Exception as e:
        print("Error al obtener reseñas del backend:", e)

    try:
        resp_stats = requests.get(f"{BACKEND_URL}/api/home/stats", timeout=5)
        if resp_stats.status_code == 200:
            estadisticas = resp_stats.json()
    except Exception as e:
        print("Error al obtener estadísticas del backend:", e)

    return render_template(
        "home.html",
        usuario=usuario,
        reseñas=reseñas,
        estadisticas=estadisticas
    )

@app.route("/buscar", methods=["GET", "POST"])
@login_required
def buscar():
    user = session.get("user")

    # guardar reseña
    if request.method == "POST":
        pub_id = request.form.get("pub_id")
        comentario = request.form.get("comentario")
        calificacion = request.form.get("calificacion")

        # Filtros
        q = request.form.get("q")
        sort = request.form.get("sort") or "-fecha"
        page = request.form.get("page") or "1"
        page_size = request.form.get("page_size") or "12"
        materias_sel = request.form.getlist("materias")
        formatos_sel = request.form.getlist("formato")

        payload = {
            "comentario": comentario,
            "calificacion": calificacion,
            "id_usuario": user.get("legajo"),
        }

        if pub_id:
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/api/publicaciones/{pub_id}/comentarios",
                    json=payload,
                    timeout=10,
                )
                if resp.status_code != 201:
                    print("Error al crear reseña:")
            except Timeout:
                print("Timeout al llamar al backend")
            except ConnectionError:
                print("No se pudo conectar al backend")
            except RequestException as e:
                print("Error HTTP")

        # vuelvo a buscar
        redirect_url = url_for(
            "buscar",
            q=q,
            sort=sort,
            page=page,
            page_size=page_size,
            materias=materias_sel,
            formato=formatos_sel,
        ) + (f"#pub-{pub_id}" if pub_id else "")
        return redirect(redirect_url)

    # mostrar búsqueda + reseñas

    q = request.args.get("q")
    sort = request.args.get("sort") or "-fecha"

    try:
        page = max(int(request.args.get("page", 1)), 1)
    except ValueError:
        page = 1

    try:
        page_size = max(int(request.args.get("page_size", 12)), 1)
    except ValueError:
        page_size = 12

    materias_sel = request.args.getlist("materias")
    formatos_sel = request.args.getlist("formato")

    # Materias
    materias = []
    try:
        resp_m = requests.get(f"{BACKEND_URL}/api/materias", timeout=5)
        resp_m.raise_for_status()
        materias = resp_m.json()
    except RequestException as e:
        materias = []

    # Parámetros
    api_params = {
        "q": q,
        "sort": sort,
        "page": page,
        "page_size": page_size,
    }
    for cod in materias_sel:
        api_params.setdefault("materias", []).append(cod)
    for fmt in formatos_sel:
        api_params.setdefault("formato", []).append(fmt)

    resultados = []
    total = 0
    pages = 1
    error = None

    try:
        resp_pub = requests.get(
            f"{BACKEND_URL}/api/publicaciones",
            params=api_params,
            timeout=10,
        )
        resp_pub.raise_for_status()
        data = resp_pub.json() or {}
        resultados = data.get("items", [])
        total = int(data.get("total", 0) or 0)
        page = int(data.get("page", page) or page)
        pages = int(data.get("pages", 1) or 1)
    except RequestException as e:
        error = "No se pudieron cargar las publicaciones"

    for p in resultados:
        url = p.get("url") or ""
        if url.startswith("/"):
            p["url"] = f"{BACKEND_URL}{url}"
            p["es_archivo_subido"] = "/uploads/" in url
        else:
            p["es_archivo_subido"] = False

        p["resenas"] = []
        pub_id = p.get("id")
        if pub_id is not None:
            try:
                resp_r = requests.get(
                    f"{BACKEND_URL}/api/publicaciones/{pub_id}/comentarios",
                    timeout=10,
                )
                if resp_r.status_code == 200:
                    p["resenas"] = resp_r.json() or []
            except RequestException as e:
                print("Error al obtener reseñas")

    return render_template(
        "busqueda.html",
        user=user,
        materias=materias,
        resultados=resultados,
        total=total,
        page=page,
        pages=pages,
        page_size=page_size,
        q=q,
        sort=sort,
        materias_seleccionadas=materias_sel,
        formatos_seleccionados=formatos_sel,
        error=error,
    )


@app.route("/descargar_archivo")
@login_required
def descargar_archivo():
    file_url = request.args.get("file_url")
    if not file_url:
        abort(400)

    try:
        backend_resp = requests.get(file_url, stream=True, timeout=10)
        backend_resp.raise_for_status()
    except Timeout:
        print("Timeout al descargar archivo")
        abort(502)
    except ConnectionError:
        print("No se pudo conectar al backend para descargar el archivo")
        abort(502)
    except RequestException as e:
        print("Error HTTP al descargar archivo")
        abort(502)

    filename = file_url.rsplit("/", 1)[-1]

    resp = Response(
        backend_resp.content,
        status=200,
        mimetype=backend_resp.headers.get(
            "Content-Type",
            "application/octet-stream",
        ),
    )
    resp.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp

    
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        form = request.form

        nombre = (form.get("nombre"))
        apellido = (form.get("apellido"))
        legajo = (form.get("legajo") or "").strip()
        email = (form.get("email") or "").strip()

        # Validaciones del lado del front
        if not nombre or not apellido or not legajo or not email:
            return render_template(
                "registro.html",
                google_client_id=GOOGLE_CLIENT_ID,
                error="Completá nombre, apellido, legajo y correo institucional.",
            )

        if not email.endswith("@fi.uba.ar"):
            return render_template(
                "registro.html",
                google_client_id=GOOGLE_CLIENT_ID,
                error="Solo se permiten correos institucionales (@fi.uba.ar).",
            )

        payload = {
            "nombre": nombre,
            "apellido": apellido,
            "legajo": legajo,
            "email": email,
        }

        try:
            resp = requests.post(
                f"{BACKEND_URL}/api/usuarios/registro",
                json=payload,
                timeout=5,
            )
        except requests.RequestException as e:
            print("Error llamando al backend de registro:", e)
            return render_template(
                "registro.html",
                google_client_id=GOOGLE_CLIENT_ID,
                error="No se pudo registrar el usuario. Intentá de nuevo más tarde.",
            )

        if resp.status_code not in (200, 201):
            print("Error en API de registro:", resp.status_code, resp.text)
            return render_template(
                "registro.html",
                google_client_id=GOOGLE_CLIENT_ID,
                error="No se pudo registrar el usuario. Intentá de nuevo más tarde.",
            )

        user_data = resp.json() or {}

        # Guardar en sesión para usar en publicaciones, reseñas, home, etc.
        session["user"] = {
            "nombre": user_data.get("nombre") or nombre,
            "apellido": user_data.get("apellido") or apellido,
            "email": user_data.get("email") or email,
            "legajo": str(user_data.get("legajo") or legajo),
        }

        
        return redirect(url_for("home"))

    
    return render_template("registro.html", google_client_id=GOOGLE_CLIENT_ID)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("registro"))

@app.route("/resenas", methods=["GET", "POST"])
@login_required
def resenas():
    user = session.get("user") 

    materias = []
    error = None
    mensaje = None

    try:
        resp = requests.get(f"{BACKEND_URL}/api/materias", timeout=5)
        resp.raise_for_status()
        materias = resp.json()
    except ConnectionError:
        print("No se pudo conectar al backend para obtener las materias")
        abort(502)    

    if request.method == "POST":
        form = request.form

        asignatura = (form.get("asignatura") or "").strip()
        nombre = (form.get("nombre") or "").strip()
        titulo_resena = (form.get("titulo_resena") or "").strip()
        resena_texto = (form.get("resena") or "").strip()
        satisfaccion = (form.get("satisfaccion") or "").strip()

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

            payload = {
                "id_materia": asignatura,      
                "comentario": comentario,
                "puntuacion": puntuacion_int,
                "id_usuario": id_usuario,       
            }

            try:
                api_resp = requests.post(
                    f"{BACKEND_URL}/api/resenas_cursos",
                    json=payload,
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
    )

@app.route('/publicaciones', methods=["GET", "POST"])
@login_required
def publicaciones():
    
    materias = []
    try:
        resp = requests.get(f"{BACKEND_URL}/api/materias", timeout=5)
        resp.raise_for_status()
        materias = resp.json()

    except ConnectionError:
        print("No se pudo conectar al backend para obtener las materias")
        abort(502)  

    if request.method == "POST":
        form = request.form
        file_obj = request.files.get("adjunto")

        
        data = {
            
            "asignatura": form.get("asignatura", "").strip(),
            
            "titulo_aporte": form.get("titulo_aporte", "").strip(),
            
            "aportes": form.get("aportes", "").strip(),
            
            "tipo_archivo": form.get("tipo_archivo", "").strip(),
            
            "url_repo": form.get("url_repo", "").strip(),
            
            "autor_nombre": session.get("user", {}).get("nombre", ""),
            "autor_email": session.get("user", {}).get("email", ""),
            "legajo_usuario": session.get("user", {}).get("legajo", ""),
        }

        files = {}
        if file_obj and file_obj.filename:
            files["adjunto"] = (
                file_obj.filename,
                file_obj.stream,
                file_obj.mimetype or "application/octet-stream",
            )

        try:
            resp = requests.post(
                f"{BACKEND_URL}/api/publicaciones",
                data=data,
                files=files,
                timeout=15,
            )
            resp.raise_for_status()
            
            return redirect(url_for("buscar"))
        except requests.RequestException as e:
            print("Error al crear publicación en backend:", e)
            error = "No se pudo crear la publicación. Intentalo de nuevo."
            return render_template(
                "publicaciones.html",
                API_URL=BACKEND_URL,
                materias=materias,
                error=error,
            )

    return render_template(
        "publicaciones.html",
        API_URL=BACKEND_URL,
        materias=materias,
    )

@app.route("/cursos")
@login_required
def cursos():
    user = session.get("user") 
    materias = []
    resenas = []

    # Traer materias
    try:
        resp = requests.get(f"{BACKEND_URL}/api/materias", timeout=5)
        resp.raise_for_status()
        materias = resp.json()
    except Exception as e:
        print("Error al obtener materias para cursos:", e)

    # Traer reseñas de cursos
    try:
        resp_r = requests.get(f"{BACKEND_URL}/api/resenas_cursos", timeout=5)
        if resp_r.status_code == 200:
            resenas = resp_r.json()
        else:
            print("Error al obtener reseñas de cursos:", resp_r.status_code, resp_r.text)
    except Exception as e:
        print("Error al llamar a /api/resenas_cursos:", e)

    return render_template(
        "cursos.html",
        materias=materias,   
        resenas=resenas,     
        user=user,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
