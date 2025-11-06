import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    user=os.getenv("user"),
    password=os.getenv("password"),
    host=os.getenv("host"),
    port=os.getenv("port"),
    dbname=os.getenv("dbname")
)

cur = conn.cursor()

# Ejecutar una consulta SQL
cur.execute("SELECT * FROM incidencia;")

# Obtener todos los resultados
rows = cur.fetchall()

print("Tabla incidencia:")
for row in rows:
    print(row)

cur.close()
conn.close()
