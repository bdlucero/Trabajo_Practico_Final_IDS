import os
import mysql.connector

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER")         
DB_PASSWORD = os.getenv("DB_PASSWORD")  
DB_NAME = os.getenv("DB_NAME", "skillmatch_uba")


def get_connection():
    if not DB_USER or not DB_PASSWORD:
        raise RuntimeError(
            "Faltan variables de entorno "
        )

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
