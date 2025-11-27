# backend/usuarios.py
from flask import Blueprint, request, jsonify
from db import get_connection

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.post("/usuarios/registro")
def registrar_usuario():
    """
    Registra (o actualiza) un usuario en la tabla USERS.

    Espera JSON con:
      - legajo   (int, obligatorio)
      - email    (str, obligatorio)
      - nombre   (str, obligatorio)
      - apellido (str, obligatorio)
    """
    data = request.get_json(silent=True) or {}

    legajo_raw = data.get("legajo")
    email = (data.get("email") or "").strip()
    nombre = (data.get("nombre") or "").strip()
    apellido = (data.get("apellido") or "").strip()

    try:
        legajo = int(legajo_raw)
    except (TypeError, ValueError):
        return jsonify({"error": "legajo inválido"}), 400

    if not email:
        return jsonify({"error": "email es obligatorio"}), 400
    if not nombre:
        return jsonify({"error": "nombre es obligatorio"}), 400
    if not apellido:
        return jsonify({"error": "apellido es obligatorio"}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()

        cur.execute("SELECT legajo FROM USERS WHERE legajo = %s", (legajo,))
        row = next(cur, None) 

        if row is None:
            cur.execute(
                """
                INSERT INTO USERS (nombre, apellido, email, legajo)
                VALUES (%s, %s, %s, %s)
                """,
                (nombre, apellido, email, legajo),
            )
        else:
            cur.execute(
                """
                UPDATE USERS
                SET nombre = %s,
                    apellido = %s,
                    email = %s
                WHERE legajo = %s
                """,
                (nombre, apellido, email, legajo),
            )

        conn.commit()
    finally:
        cur.close()
        conn.close()

    return jsonify(
        {
            "legajo": legajo,
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
        }
    ), 201
