
from flask import Blueprint, jsonify
from db import get_connection

home_bp = Blueprint("home", __name__)

@home_bp.get("/home/resenas")
def ultimas_resenas():
    
    conn = get_connection()
    try:
        cur = conn.cursor()

        sql = """
            SELECT 
                r.id_resena,
                r.id_materia,
                m.materia AS nombre_materia,
                r.comentario,
                r.puntuacion,
                u.nombre AS autor
            FROM Resenas_cursos r
            JOIN materias m ON r.id_materia = m.codigo
            LEFT JOIN USERS u ON r.id_usuario = u.legajo
            ORDER BY r.fecha_resena DESC
            LIMIT 3
        """
        cur.execute(sql)

        reseñas = []

        for (
            id_resena,
            id_materia,
            nombre_materia,
            comentario,
            puntuacion,
            autor,
        ) in cur:
            comentario = comentario or ""

            lineas = [ln.strip() for ln in comentario.splitlines() if ln.strip()]

            titulo = lineas[0] if lineas else ""
            cuerpo_lineas = lineas[1:]

            if cuerpo_lineas and cuerpo_lineas[0].lower().startswith("autor:"):
                cuerpo_lineas = cuerpo_lineas[1:]

            texto = " ".join(cuerpo_lineas)

            reseñas.append(
                {
                    "id_resena": id_resena,
                    "id_materia": id_materia,
                    "nombre_materia": nombre_materia,
                    "puntuacion": int(puntuacion) if puntuacion is not None else None,
                    "autor": autor,
                    "titulo_resena": titulo,
                    "texto_resena": texto,
                }
            )

    finally:
        cur.close()
        conn.close()

    return jsonify(reseñas)

@home_bp.get("/home/stats")
def estadisticas_home():
    """
    Devuelve estadísticas simples de la plataforma:
    - total_publicaciones
    - total_usuarios
    - total_resenas
    """
    conn = get_connection()
    try:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM publicaciones;")
        try:
            row_pub = next(cur)
            total_publicaciones = int(row_pub[0])
        except StopIteration:
            total_publicaciones = 0

        cur.execute("SELECT COUNT(*) FROM USERS;")
        try:
            row_usr = next(cur)
            total_usuarios = int(row_usr[0])
        except StopIteration:
            total_usuarios = 0

        cur.execute("SELECT COUNT(*) FROM Resenas_cursos;")
        try:
            row_res = next(cur)
            total_resenas = int(row_res[0])
        except StopIteration:
            total_resenas = 0

    finally:
        cur.close()
        conn.close()

    stats = [
        {"valor": f"+{total_publicaciones}", "descripcion": "Ofertas publicadas"},
        {"valor": f"+{total_usuarios}", "descripcion": "Estudiantes registrados"},
        {"valor": f"+{total_resenas}", "descripcion": "Reseñas de materias"},
    ]

    return jsonify(stats)

