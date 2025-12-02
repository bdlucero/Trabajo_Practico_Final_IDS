from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from db import get_connection
import os
import uuid

publicaciones_bp = Blueprint("publicaciones", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@publicaciones_bp.post("/publicaciones")
def crear_publicacion():
    materia_codigo = (request.form.get("asignatura") or "").strip()
    titulo = (request.form.get("titulo_aporte") or "").strip()
    descripcion = (request.form.get("aportes") or "").strip()
    formato = (request.form.get("tipo_archivo") or "").strip()
    url_repo = (request.form.get("url_repo") or "").strip()

    autor_nombre = (request.form.get("autor_nombre") or "").strip()
    autor_email = (request.form.get("autor_email") or "").strip()
    legajo_usuario = (request.form.get("legajo_usuario") or "").strip()

    archivo = request.files.get("adjunto")

    if not materia_codigo or not titulo or not formato:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    if not url_repo and (archivo is None or not archivo.filename.strip()):
        return jsonify(
            {"error": "Debe adjuntar un archivo o enviar un enlace (URL)"}
        ), 400

    allowed_ext = {"pdf", "png","zip"} 

    if archivo and archivo.filename:
        nombre_archivo = archivo.filename
        if "." in nombre_archivo:
            ext = nombre_archivo.rsplit(".", 1)[1].lower()
        else:
            ext = ""

        if ext not in allowed_ext:
            return jsonify(
                {"error": "Formato de archivo no permitido. Solo se aceptan PDF o PNG."}
            ), 400

    try:
        legajo_int = int(legajo_usuario) if legajo_usuario else None
    except ValueError:
        legajo_int = None

  
    final_url = url_repo 

   
    if archivo and archivo.filename:
        filename = secure_filename(archivo.filename)
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        save_path = os.path.join(UPLOAD_FOLDER, unique_name)
        archivo.save(save_path)
        
        final_url = f"/api/uploads/{unique_name}"

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO publicaciones
            (titulo, descripcion, formato, url,
             autor_nombre, autor_email, materia_codigo, legajo_usuario)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                titulo,
                descripcion,
                formato,
                final_url,
                autor_nombre,
                autor_email,
                materia_codigo,
                legajo_int,
            ),
        )
        conn.commit()
        pub_id = cur.lastrowid
    finally:
        cur.close()
        conn.close()

    return jsonify({"id": pub_id, "mensaje": "Publicación creada"}), 201


@publicaciones_bp.get("/uploads/<path:filename>")
def servir_upload(filename):
    
    return send_from_directory(UPLOAD_FOLDER, filename)