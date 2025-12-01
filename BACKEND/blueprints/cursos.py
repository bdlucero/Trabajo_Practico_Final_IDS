from flask import Blueprint, jsonify, request
from db import get_connection
import math

# Blueprint para las rutas del buscador (API de búsqueda)
cursos_bp = Blueprint("cursos", __name__)

@cursos_bp.get("/resenas_cursos")
def listar_resenas_cursos():
    q = (request.args.get("q") or "").strip()
    materias = request.args.getlist("materias")  # códigos de materia (COM01, etc.)

    conn = get_connection()
    try:
        cur = conn.cursor()

        sql = """
            SELECT
              r.id_resena,
              r.id_materia,
              m.materia      AS nombre_materia,
              r.comentario,
              r.puntuacion,
              u.nombre       AS nombre_usuario,
              u.apellido     AS apellido_usuario
            FROM Resenas_cursos r
            JOIN materias m ON r.id_materia = m.codigo
            LEFT JOIN USERS u ON r.id_usuario = u.legajo
        """

        where_clauses = []
        params = []

        # filtro simple por texto
        if q:
            where_clauses.append("""
              (
                m.materia    LIKE %s OR
                r.comentario LIKE %s OR
                u.nombre     LIKE %s OR
                u.apellido   LIKE %s
              )
            """)
            like = f"%{q}%"
            params.extend([like, like, like, like])

        # filtro por materias (códigos)
        if materias:
            placeholders = ", ".join(["%s"] * len(materias))
            where_clauses.append(f"r.id_materia IN ({placeholders})")
            params.extend(materias)

        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)

        sql += " ORDER BY r.fecha_resena DESC"

        cur.execute(sql, tuple(params))

        resenas = []

        # iteramos el cursor
        for (
            id_resena,
            id_materia,
            nombre_materia,
            comentario,
            puntuacion,
            nombre_usuario,
            apellido_usuario,
        ) in cur:
            comentario = comentario or ""

            # Separar líneas, sacar vacías
            lineas = [ln.strip() for ln in comentario.splitlines() if ln.strip()]

            titulo = ""
            cuerpo_lineas = []

            if lineas:
                titulo = lineas[0]
                cuerpo_lineas = lineas[1:]

            # Si hay línea "Autor: ..." vieja, la salto
            if cuerpo_lineas and cuerpo_lineas[0].lower().startswith("autor:"):
                cuerpo_lineas = cuerpo_lineas[1:]

            texto_cuerpo = " ".join(cuerpo_lineas) if cuerpo_lineas else ""

            # Comentario amigable para mostrar en cards
            if titulo and texto_cuerpo:
                comentario_vista = f"{titulo}: {texto_cuerpo}"
            elif titulo:
                comentario_vista = titulo
            else:
                comentario_vista = texto_cuerpo

            nombre_completo = (nombre_usuario or "") + (
                f" {apellido_usuario}" if apellido_usuario else ""
            )
            if not nombre_completo.strip():
                nombre_completo = "Anónimo"

            resenas.append(
                {
                    "id_resena": id_resena,
                    "id_materia": id_materia,          # código (COM01, etc.)
                    "asignatura": nombre_materia,      # nombre para mostrar
                    "comentario": comentario_vista,
                    "puntuacion": int(puntuacion) if puntuacion is not None else 0,
                    "nombre": nombre_completo,
                }
            )

    finally:
        cur.close()
        conn.close()

    return jsonify(resenas)
