from flask import Blueprint, jsonify, request
from db import get_connection
import math


busqueda_bp = Blueprint("busqueda", __name__)


@busqueda_bp.get("/materias")
def obtener_materias():
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT codigo, materia AS nombre
            FROM materias
            ORDER BY codigo
            """
        )

        materias = []
        for row in cur:   
            materias.append(row)

    finally:
        cur.close()
        conn.close()

    return jsonify(materias)


@busqueda_bp.get("/publicaciones")
def listar_publicaciones():
    
    
    q = request.args.get("q", "").strip()
    sort = request.args.get("sort", "-fecha").strip()

    try:
        page = max(int(request.args.get("page", 1)), 1)
    except ValueError:
        page = 1

    try:
        page_size = max(int(request.args.get("page_size", 12)), 1)
    except ValueError:
        page_size = 12

    materias_codes = request.args.getlist("materias")
    formatos = request.args.getlist("formato")

    condiciones = []
    params = []

    # Filtro por materias 
    if materias_codes:
        valid_codes = [c for c in materias_codes if c]
        if valid_codes:
            placeholders = ",".join(["%s"] * len(valid_codes))
            condiciones.append(f"p.materia_codigo IN ({placeholders})")
            params.extend(valid_codes)

    # Filtro por formato
    if formatos:
        placeholders = ",".join(["%s"] * len(formatos))
        condiciones.append(f"p.formato IN ({placeholders})")
        params.extend(formatos)

    # Búsqueda de texto libre
    if q:
        condiciones.append("(p.titulo LIKE %s OR p.descripcion LIKE %s)")
        like = f"%{q}%"
        params.extend([like, like])

    where_clause = ""
    if condiciones:
        where_clause = "WHERE " + " AND ".join(condiciones)

    # Campos extra y orden según sort
    extra_fields = ""
    order_by = "ORDER BY p.creado_en DESC"

    if sort == "-comentarios":
        # contar reseñas en resena_publicacion
        extra_fields = """
            , (
                SELECT COUNT(*)
                FROM resena_publicacion r
                WHERE r.id_publicacion = p.id
            ) AS cant_comentarios
        """
        order_by = "ORDER BY cant_comentarios DESC, p.creado_en DESC"

    conn = get_connection()
    try:
        #  Conteo total 
        count_query = f"""
            SELECT COUNT(*)
            FROM publicaciones p
            JOIN materias m ON m.codigo = p.materia_codigo
            {where_clause}
        """
        cur = conn.cursor()
        cur.execute(count_query, params)

        row = next(cur, None)
        total = row[0] if row is not None else 0
        cur.close()

        pages = max(math.ceil(total / page_size), 1) if total > 0 else 1
        if page > pages:
            page = pages

        offset = (page - 1) * page_size

        #  Selección principal  
        main_query = f"""
            SELECT
                p.id,
                p.titulo,
                p.descripcion,
                p.formato,
                p.url,
                p.autor_nombre,
                p.autor_email,
                p.creado_en,
                m.codigo  AS materia_codigo,
                m.materia AS materia_nombre
                {extra_fields}
            FROM publicaciones p
            JOIN materias m ON m.codigo = p.materia_codigo
            {where_clause}
            {order_by}
            LIMIT %s OFFSET %s
        """
        params_main = params + [page_size, offset]

        cur = conn.cursor(dictionary=True)
        cur.execute(main_query, params_main)

        filas = []
        for row in cur:
            filas.append(row)

    finally:
        cur.close()
        conn.close()

    items = []
    for row in filas:
        items.append(
            {
                "id": row["id"],
                "titulo": row["titulo"],
                "descripcion": row["descripcion"],
                "formato": row["formato"],
                "url": row["url"],
                "autor_nombre": row["autor_nombre"],
                "autor_email": row["autor_email"],
                "creado_en": row["creado_en"].isoformat()
                if row["creado_en"]
                else None,
                "materias": [
                    {
                        "codigo": row["materia_codigo"],
                        "nombre": row["materia_nombre"],
                    }
                ],
            }
        )

    return jsonify({"total": total, "page": page, "pages": pages, "items": items})



@busqueda_bp.get("/publicaciones/<int:pub_id>/comentarios")
def listar_comentarios(pub_id: int):
    """
    Devuelve todas las reseñas de una publicación desde la tabla `resena_publicacion`.
    """
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT
                id_resena_publicacion,
                id_usuario,
                calificacion,
                comentario,
                fecha_resena
            FROM resena_publicacion
            WHERE id_publicacion = %s
            ORDER BY fecha_resena ASC
            """,
            (pub_id,),
        )

        reseñas = []
        for row in cur:  
            reseñas.append({
                "id": row["id_resena_publicacion"],
                "id_usuario": row["id_usuario"],
                "calificacion": row["calificacion"],
                "comentario": row["comentario"],
                "fecha_resena": (
                    row["fecha_resena"].isoformat()
                    if row["fecha_resena"] is not None
                    else None
                ),
            })
    finally:
        cur.close()
        conn.close()

    return jsonify(reseñas)


@busqueda_bp.post("/publicaciones/<int:pub_id>/comentarios")
def crear_comentario(pub_id: int):
  
    data = request.get_json(silent=True) or {}

   
    calificacion_raw = data.get("calificacion")
    comentario = (data.get("comentario") or "").strip()

    id_usuario_raw = data.get("id_usuario", None)
    if id_usuario_raw in ("", None):
        id_usuario = None
    else:
        try:
            id_usuario = int(id_usuario_raw)
        except (TypeError, ValueError):
            return jsonify({"error": "id_usuario inválido"}), 400

    try:
        calificacion = int(calificacion_raw)
    except (TypeError, ValueError):
        return jsonify({"error": "Calificación inválida o faltante"}), 400

    if not (1 <= calificacion <= 5):
        return jsonify({"error": "La calificación debe estar entre 1 y 5"}), 400

    conn = get_connection()
    try:
        cur = conn.cursor()

        sql = """
            INSERT INTO resena_publicacion
            (id_usuario, id_publicacion, calificacion, comentario)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (id_usuario, pub_id, calificacion, comentario or None))
        conn.commit()
        nuevo_id = cur.lastrowid

    finally:
        cur.close()
        conn.close()

    return jsonify({
        "id": nuevo_id,
        "mensaje": "Reseña creada correctamente"
    }), 201
