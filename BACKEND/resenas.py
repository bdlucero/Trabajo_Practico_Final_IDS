from flask import Blueprint, jsonify, request
from db import get_connection
import math


resenas_bp = Blueprint("resenas", __name__)


@resenas_bp.post("/resenas_cursos")
def crear_resena_curso():
    """
    Crea una reseña de curso en la tabla `Resenas_cursos`.

    Espera JSON con:
      - id_materia   (str) código de la materia, ej: "COM01"         [obligatorio]
      - comentario   (str) texto de la reseña                         [obligatorio]
      - puntuacion   (int, 1..5)                                      [obligatorio]
      - id_usuario   (int, legajo del usuario)                        [opcional por ahora]
    """
    data = request.get_json(silent=True) or {}

    id_materia = (data.get("id_materia") or "").strip()
    comentario = (data.get("comentario") or "").strip()
    puntuacion_raw = data.get("puntuacion")
    id_usuario_raw = data.get("id_usuario")

    # ---- Validaciones mínimas ----
    if not id_materia:
        return jsonify({"error": "id_materia es obligatorio"}), 400

    if not comentario:
        return jsonify({"error": "comentario es obligatorio"}), 400

    # puntuación
    try:
        puntuacion = int(puntuacion_raw)
    except (TypeError, ValueError):
        return jsonify({"error": "puntuacion inválida o faltante"}), 400

    if not (1 <= puntuacion <= 5):
        return jsonify({"error": "puntuacion debe estar entre 1 y 5"}), 400

    # id_usuario es OPCIONAL por ahora
    id_usuario = None
    if id_usuario_raw not in (None, "", "null"):
        try:
            id_usuario = int(id_usuario_raw)
        except (TypeError, ValueError):
            # si viene algo totalmente raro, devolvemos 400
            return jsonify({"error": "id_usuario inválido"}), 400

    # ---- Insert en la tabla Resenas_cursos ----
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            INSERT INTO Resenas_cursos
            (id_usuario, id_materia, comentario, puntuacion)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (id_usuario, id_materia, comentario, puntuacion))
        conn.commit()
        nuevo_id = cur.lastrowid
    finally:
        cur.close()
        conn.close()

    return jsonify({
        "id": nuevo_id,
        "mensaje": "Reseña de curso creada correctamente"
    }), 201