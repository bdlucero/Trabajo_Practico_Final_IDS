import pathlib
from db import get_connection   

def init_db() -> None:
    BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

    sql_path = BASE_DIR / "SQL" / "skillmatch_uba.sql"
    sql_text = sql_path.read_text(encoding="utf-8")

    conn = get_connection()
    try:
        cur = conn.cursor()
        for _ in cur.execute(sql_text, multi=True):
            pass
        conn.commit()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    init_db()
