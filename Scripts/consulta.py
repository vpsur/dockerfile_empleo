#!/usr/bin/env python3


import json
import mysql.connector
import mariadb
import psycopg2
from decimal import Decimal
from datetime import date, datetime
# CONFIGURACIÓN DE CONEXIONES
MYSQL = dict(host="localhost", user="root", password="admin", database="empleosDBmysql")
MARIADB = dict(host="localhost", user="root", password="admin", port=3307, database="empleosDBmariaDB")
POSTGRES = dict(host="localhost", user="postgres", password="admin", dbname="empleosDB")

# FUNCIONES GENÉRICAS

def fetch_all(cursor, query):
    cursor.execute(query)
    cols = [desc[0] for desc in cursor.description]
    result = []
    for row in cursor.fetchall():
        row_dict = {}
        for col, val in zip(cols, row):
            # Convertir Decimal a float
            if isinstance(val, Decimal):
                val = float(val)
            row_dict[col] = val
            if isinstance(val, date):
                val = val.isoformat()
        result.append(row_dict)
    return result

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Archivo generado: {filename}")

# CONSULTAS ANALÍTICAS POR BASE DE DATOS

def analizar_mysql():
    conn = mysql.connector.connect(**MYSQL)
    cur = conn.cursor()

    # 1️ Habilidades más demandadas para conocer sobre las tendencias actuales
    q1 = """
        SELECT h.Nombre AS Habilidad, COUNT(oh.ID_Oferta) AS Veces_Demandada
        FROM Oferta_Habilidad oh
        JOIN Habilidades h ON h.ID = oh.ID_Habilidad
        GROUP BY h.Nombre
        ORDER BY Veces_Demandada DESC
        LIMIT 5;
    """

    # 2️ Promedio de edad por disponibilidad para analizar el perfil de usuarios que están disponibles en los distintos momentos
    q2 = """
        SELECT Disponibilidad, AVG(Edad) AS Edad_Promedio, COUNT(*) AS Num_Usuarios
        FROM Usuarios
        GROUP BY Disponibilidad;
    """

    # 3️ Formaciones más pedidas para ver las áreas de conocimiento más valoradas y demandadas
    q3 = """
        SELECT f.Nombre AS Formacion, COUNT(ofor.ID_Oferta) AS Num_Ofertas
        FROM Oferta_Formacion ofor
        JOIN Formacion f ON f.ID = ofor.ID_Formacion
        GROUP BY f.Nombre
        ORDER BY Num_Ofertas DESC
        LIMIT 5;
    """

    data = {
        "Habilidades_Mas_Demandadas": fetch_all(cur, q1),
        "Edad_Promedio_Por_Disponibilidad": fetch_all(cur, q2),
        "Formaciones_Mas_Pedidas": fetch_all(cur, q3),
        "Descripcion": "Análisis de tendencias laborales y perfil de usuarios en MySQL"
    }

    cur.close()
    conn.close()
    save_json("analisis_mysql.json", data)

def analizar_mariadb():
    conn = mariadb.connect(**MARIADB)
    cur = conn.cursor()

    # 1️ Recomendaciones con mayor afinidad por usurios. Esto nos permite que oferta encaja mejor con cada usuario
    q1 = """
        SELECT u.Nombre AS Usuario, o.Titulo AS Oferta, r.Afinidad
        FROM Recomendaciones r
        JOIN Usuarios u ON r.ID_Usuario = u.ID
        JOIN Oferta_Empleo o ON r.ID_Oferta = o.ID
        ORDER BY r.Afinidad DESC
        LIMIT 10;
    """

    # 2️ Promedio de afinidad por sector que permita identificar qué sectores tienen mejor afinidad con los usuarios
    q2 = """
        SELECT o.Sector, AVG(r.Afinidad) AS Afinidad_Promedio
        FROM Recomendaciones r
        JOIN Oferta_Empleo o ON r.ID_Oferta = o.ID
        GROUP BY o.Sector;
    """

    data = {
        "Top10_Recomendaciones": fetch_all(cur, q1),
        "Afinidad_Promedio_Por_Sector": fetch_all(cur, q2),
        "Descripcion": "Análisis de afinidad entre usuarios y ofertas en MariaDB"
    }

    cur.close()
    conn.close()
    save_json("analisis_mariadb.json", data)

def analizar_postgres():
    conn = psycopg2.connect(**POSTGRES)
    cur = conn.cursor()

    # 1️ Tendencias laborales por sector que muestre el crecimiento de ciertos empleos
    q1 = """
        SELECT Sector, COUNT(*) AS Num_Tendencias, 
               STRING_AGG(DISTINCT Crecimiento_Demanda, ', ') AS Tipos_Crecimiento
        FROM Tendencias_Laborales
        GROUP BY Sector;
    """

    # 2️ Formaciones sugeridas más comunes para ver que formaciones son las más sugeridas a los usuarios
    q2 = """
        SELECT f.Nombre AS Formacion, COUNT(fs.ID) AS Num_Sugerencias
        FROM Formacion_Sugerida fs
        JOIN Formacion f ON f.ID = fs.ID_Formacion
        GROUP BY f.Nombre
        ORDER BY Num_Sugerencias DESC
        LIMIT 5;
    """

    data = {
        "Tendencias_Por_Sector": fetch_all(cur, q1),
        "Formaciones_Sugeridas_Mas_Comunes": fetch_all(cur, q2),
        "Descripcion": "Análisis de tendencias y formaciones recomendadas en PostgreSQL"
    }

    cur.close()
    conn.close()
    save_json("analisis_postgres.json", data)

# EJECUCIÓN PRINCIPAL

if __name__ == "__main__":
    print("Generando análisis y JSONs para MySQL, MariaDB y PostgreSQL...")
    analizar_mysql()
    analizar_mariadb()
    analizar_postgres()
    print("Todos los archivos JSON fueron creados correctamente.")
