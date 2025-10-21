
#Estos son los providers usados:
#1. faker.providers.person          → Nombres, apellidos, sexo
#2. faker.providers.address         → Domicilios, nacionalidades, ubicaciones
#3. faker.providers.internet        → Emails, URLs, contraseñas
#4. faker.providers.phone_number    → Teléfonos
#5. faker.providers.job             → Puestos, sectores
#6. faker.providers.company         → Empresas
#7. faker.providers.date_time       → Fechas de inicio/fin
#8. faker.providers.education       → Instituciones, titulaciones
#9. faker.providers.misc            → Elementos aleatorios (niveles, categorías, tipos)
#10. faker.providers.lorem          → Descripciones de texto

import random
from faker import Faker
import mysql.connector
import psycopg2
import mariadb

# Inicializar Faker
fake = Faker('es_ES')

# CONEXIONES A LAS BASES DE DATOS

mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="empleosDBmysql"
)

mariadb_conn = mariadb.connect(
    host="localhost",
    user="root",
    port=3307,
    password="admin",
    database="empleosDBmariaDB"
)

postgres_conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="admin",
    dbname="empleosDB"
)

# Crear cursores
mysql_cursor = mysql_conn.cursor()
mariadb_cursor = mariadb_conn.cursor()
postgres_cursor = postgres_conn.cursor()

# FUNCIÓN GENÉRICA DE INSERCIÓN
def ejecutar_en_todas(query, valores=None):
    try:
        if valores:
            mysql_cursor.execute(query, valores)
            mariadb_cursor.execute(query, valores)
            postgres_cursor.execute(query, valores)
        else:
            mysql_cursor.execute(query)
            mariadb_cursor.execute(query)
            postgres_cursor.execute(query)
    except Exception as e:
        print("Error:", e)

# FUNCIONES DE INSERCIÓN DE DATOS BASE
def insertar_usuarios(n=30):
    for _ in range(n):
        dni = fake.unique.random_int(10000000, 99999999)
        nombre = fake.first_name()
        apellido = fake.last_name()
        edad = random.randint(18, 65)
        email = fake.unique.email()
        telefono = fake.phone_number()
        sexo = random.choice(['M', 'F', 'Otro'])
        nacionalidad = fake.country()
        contrasena = fake.password()
        domicilio = fake.address().replace('\n', ', ')
        disponibilidad = random.choice(['Tiempo completo', 'Medio tiempo', 'Remoto', 'Freelance'])

        query = """
            INSERT INTO Usuarios (DNI, Nombre, Apellido, Edad, Email, Telefono, Sexo, Nacionalidad, Contrasena, Domicilio, Disponibilidad)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        ejecutar_en_todas(query, (dni, nombre, apellido, edad, email, telefono, sexo, nacionalidad, contrasena, domicilio, disponibilidad))

def insertar_portales(n=5):
    for _ in range(n):
        nombre = fake.company()
        url = fake.url()
        query = "INSERT INTO Prota (Nombre, URL) VALUES (%s, %s)"
        ejecutar_en_todas(query, (nombre, url))

def insertar_habilidades(n=15):
    for _ in range(n):
        nombre = fake.word().capitalize()
        categoria = random.choice(['Técnica', 'Blanda', 'Gestión', 'Idioma'])
        query = "INSERT INTO Habilidades (Nombre, Categoria) VALUES (%s,%s)"
        ejecutar_en_todas(query, (nombre, categoria))

def insertar_formaciones(n=15):
    for _ in range(n):
        nombre = fake.job()
        tipo = random.choice(['Grado', 'Máster', 'Curso', 'Diplomado'])
        institucion = fake.company()
        area = random.choice(['Informática', 'Administración', 'Educación', 'Salud'])
        query = "INSERT INTO Formacion (Nombre, Tipo, Institucion, Area) VALUES (%s,%s,%s,%s)"
        ejecutar_en_todas(query, (nombre, tipo, institucion, area))

def insertar_ofertas(n=20):
    for _ in range(n):
        titulo = fake.job()
        empresa = fake.company()
        ubicacion = fake.city()
        descripcion = fake.text(200)
        salario = round(random.uniform(1000, 8000), 2)
        url = fake.url()
        sector = random.choice(['Tecnología', 'Salud', 'Educación', 'Marketing', 'Finanzas'])
        tipo_contrato = random.choice(['Indefinido', 'Temporal', 'Prácticas', 'Freelance'])
        duracion = random.choice(['6 meses', '1 año', 'Indefinido'])
        jornada = random.choice(['Completa', 'Parcial', 'Remota'])
        id_portal = random.randint(1, 5)

        query = """
            INSERT INTO Oferta_Empleo (ID_Portal, Titulo, Empresa, Ubicacion, Descripcion, Salario, URL_Oferta, Sector, Tipo_Contrato, Duracion, Jornada)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        ejecutar_en_todas(query, (id_portal, titulo, empresa, ubicacion, descripcion, salario, url, sector, tipo_contrato, duracion, jornada))

def insertar_experiencia(n=40):
    for _ in range(n):
        id_usuario = random.randint(1, 30)
        empresa = fake.company()
        puesto = fake.job()
        fecha_inicio = fake.date_between(start_date='-10y', end_date='-2y')
        fecha_fin = fake.date_between(start_date=fecha_inicio, end_date='today')
        descripcion = fake.text(200)
        sector = random.choice(['Tecnología', 'Educación', 'Salud', 'Finanzas'])
        query = """
            INSERT INTO Experiencia_Laboral (ID_Usuario, Empresa, Puesto, Fecha_Inicio, Fecha_Fin, Descripcion, Sector)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        ejecutar_en_todas(query, (id_usuario, empresa, puesto, fecha_inicio, fecha_fin, descripcion, sector))

def insertar_usuario_habilidad(n=60):
    for _ in range(n):
        id_usuario = random.randint(1, 30)
        id_habilidad = random.randint(1, 15)
        nivel = random.choice(['Básico', 'Intermedio', 'Avanzado', 'Experto'])
        query = "INSERT INTO Usuario_Habilidad (ID_Usuario, ID_Habilidad, Nivel) VALUES (%s,%s,%s)"
        ejecutar_en_todas(query, (id_usuario, id_habilidad, nivel))

def insertar_usuario_formacion(n=50):
    for _ in range(n):
        id_usuario = random.randint(1, 30)
        id_formacion = random.randint(1, 15)
        anio_inicio = random.randint(2005, 2020)
        anio_fin = anio_inicio + random.randint(1, 3)
        titulacion = fake.job()
        query = """
            INSERT INTO Usuario_Formacion (ID_Usuario, ID_Formacion, Anio_Inicio, Anio_Fin, Titulacion)
            VALUES (%s,%s,%s,%s,%s)
        """
        ejecutar_en_todas(query, (id_usuario, id_formacion, anio_inicio, anio_fin, titulacion))

def insertar_oferta_habilidad(n=40):
    for _ in range(n):
        id_oferta = random.randint(1, 20)
        id_habilidad = random.randint(1, 15)
        nivel = random.choice(['Básico', 'Intermedio', 'Avanzado'])
        query = "INSERT INTO Oferta_Habilidad (ID_Oferta, ID_Habilidad, Nivel) VALUES (%s,%s,%s)"
        ejecutar_en_todas(query, (id_oferta, id_habilidad, nivel))

def insertar_oferta_formacion(n=30):
    for _ in range(n):
        id_oferta = random.randint(1, 20)
        id_formacion = random.randint(1, 15)
        query = "INSERT INTO Oferta_Formacion (ID_Oferta, ID_Formacion) VALUES (%s,%s)"
        ejecutar_en_todas(query, (id_oferta, id_formacion))

def insertar_recomendaciones(n=50):
    for _ in range(n):
        id_oferta = random.randint(1, 20)
        id_usuario = random.randint(1, 30)
        afinidad = round(random.uniform(50, 100), 2)
        query = "INSERT INTO Recomendaciones (ID_Oferta, ID_Usuario, Afinidad) VALUES (%s,%s,%s)"
        ejecutar_en_todas(query, (id_oferta, id_usuario, afinidad))

def insertar_formacion_sugerida(n=20):
    for _ in range(n):
        id_formacion = random.randint(1, 15)
        id_usuario = random.randint(1, 30)
        descripcion = fake.text(150)
        query = "INSERT INTO Formacion_Sugerida (ID_Formacion, ID_Usuario, Descripcion) VALUES (%s,%s,%s)"
        ejecutar_en_todas(query, (id_formacion, id_usuario, descripcion))

def insertar_tendencias_laborales(n=20):
    for _ in range(n):
        id_formacion = random.randint(1, 15)
        id_habilidad = random.randint(1, 15)
        sector = random.choice(['Tecnología', 'Educación', 'Salud', 'Finanzas'])
        crecimiento = random.choice(['Alta', 'Media', 'Baja'])
        periodo = random.choice(['2023', '2024', '2025'])
        query = """
            INSERT INTO Tendencias_Laborales (ID_Formacion, ID_Habilidad, Sector, Crecimiento_Demanda, Periodo)
            VALUES (%s,%s,%s,%s,%s)
        """
        ejecutar_en_todas(query, (id_formacion, id_habilidad, sector, crecimiento, periodo))

# EJECUCIÓN PRINCIPAL

print("Insertando datos falsos en MySQL, MariaDB y PostgreSQL")

insertar_usuarios()
insertar_portales()
insertar_habilidades()
insertar_formaciones()
insertar_ofertas()
insertar_experiencia()
insertar_usuario_habilidad()
insertar_usuario_formacion()
insertar_oferta_habilidad()
insertar_oferta_formacion()
insertar_recomendaciones()
insertar_formacion_sugerida()
insertar_tendencias_laborales()

# Confirmar transacciones
mysql_conn.commit()
mariadb_conn.commit()
postgres_conn.commit()

# Cerrar cursores y conexiones
mysql_cursor.close()
mariadb_cursor.close()
postgres_cursor.close()
mysql_conn.close()
mariadb_conn.close()
postgres_conn.close()

print("Tarea Realizada")
