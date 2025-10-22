import mysql.connector
import psycopg2


SERVER_CREDS_mysql = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "db_name": "empleosDBmysql"
}

SERVER_CREDS_mariaDB = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "db_name": "empleosDBmariaDB"
}

SERVER_CREDS_postgre = {
    "host": "localhost",
    "user": "postgres",
    "password": "admin",
    "db_name": "empleosDB"
}

# Puertos configurados en Docker para cada motor
SERVER_CONFIGS = {
    "PostgreSQL": {"port": 5432, "driver": "psycopg2", "initial_db": "postgres"},
    "MySQL":      {"port": 3306, "driver": "mysql", "initial_db": None}, 
    "MariaDB":    {"port": 3307, "driver": "mariadb", "initial_db": None},
}

SQL_MARIADB = """
CREATE TABLE IF NOT EXISTS Usuarios (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    DNI VARCHAR(20) UNIQUE,
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    Edad INT,
    Email VARCHAR(150) UNIQUE,
    Telefono VARCHAR(20),
    Sexo ENUM('M', 'F', 'Otro'),
    Nacionalidad VARCHAR(100),
    Contrasena VARCHAR(255),
    Domicilio VARCHAR(255),
    Disponibilidad VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Experiencia_Laboral (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,
    Empresa VARCHAR(150),
    Puesto VARCHAR(150),
    Fecha_Inicio DATE,
    Fecha_Fin DATE,
    Descripcion TEXT,
    Sector VARCHAR(100),
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Prota (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(150),
    URL VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Oferta_Empleo (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Portal INT,
    Titulo VARCHAR(150),
    Empresa VARCHAR(150),
    Ubicacion VARCHAR(150),
    Descripcion TEXT,
    Salario DECIMAL(10,2),
    URL_Oferta VARCHAR(255),
    Sector VARCHAR(100),
    Tipo_Contrato VARCHAR(100),
    Duracion VARCHAR(100),
    Jornada VARCHAR(100),
    FOREIGN KEY (ID_Portal) REFERENCES Prota(ID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Habilidades (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100),
    Categoria VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Usuario_Habilidad (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,
    ID_Habilidad INT,
    Nivel VARCHAR(50),
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Habilidad) REFERENCES Habilidades(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Formacion (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(150),
    Tipo VARCHAR(100),
    Institucion VARCHAR(150),
    Area VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Usuario_Formacion (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,
    ID_Formacion INT,
    Anio_Inicio YEAR,
    Anio_Fin YEAR,
    Titulacion VARCHAR(150),
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Formacion) REFERENCES Formacion(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Oferta_Habilidad (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Oferta INT,
    ID_Habilidad INT,
    Nivel VARCHAR(50),
    FOREIGN KEY (ID_Oferta) REFERENCES Oferta_Empleo(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Habilidad) REFERENCES Habilidades(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Oferta_Formacion (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Oferta INT,
    ID_Formacion INT,
    FOREIGN KEY (ID_Oferta) REFERENCES Oferta_Empleo(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Formacion) REFERENCES Formacion(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Recomendaciones (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Oferta INT,
    ID_Usuario INT,
    Afinidad DECIMAL(5,2),
    FOREIGN KEY (ID_Oferta) REFERENCES Oferta_Empleo(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Formacion_Sugerida (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Formacion INT,
    ID_Usuario INT,
    Descripcion TEXT,
    FOREIGN KEY (ID_Formacion) REFERENCES Formacion(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Tendencias_Laborales (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Formacion INT,
    ID_Habilidad INT,
    Sector VARCHAR(100),
    Crecimiento_Demanda VARCHAR(100),
    Periodo VARCHAR(50),
    FOREIGN KEY (ID_Formacion) REFERENCES Formacion(ID) ON DELETE SET NULL,
    FOREIGN KEY (ID_Habilidad) REFERENCES Habilidades(ID) ON DELETE SET NULL
);
"""

SQL_PG = """
CREATE TABLE IF NOT EXISTS Usuarios (
    ID SERIAL PRIMARY KEY,
    DNI VARCHAR(20) UNIQUE,
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    Edad INT,
    Email VARCHAR(150) UNIQUE,
    Telefono VARCHAR(20),
    Sexo VARCHAR(10),
    Nacionalidad VARCHAR(100),
    Contrasena VARCHAR(255),
    Domicilio VARCHAR(255),
    Disponibilidad VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Experiencia_Laboral (
    ID SERIAL PRIMARY KEY,
    ID_Usuario INT REFERENCES Usuarios(ID) ON DELETE CASCADE,
    Empresa VARCHAR(150),
    Puesto VARCHAR(150),
    Fecha_Inicio DATE,
    Fecha_Fin DATE,
    Descripcion TEXT,
    Sector VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Prota (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(150),
    URL VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Oferta_Empleo (
    ID SERIAL PRIMARY KEY,
    ID_Portal INT REFERENCES Prota(ID) ON DELETE SET NULL,
    Titulo VARCHAR(150),
    Empresa VARCHAR(150),
    Ubicacion VARCHAR(150),
    Descripcion TEXT,
    Salario NUMERIC(10,2),
    URL_Oferta VARCHAR(255),
    Sector VARCHAR(100),
    Tipo_Contrato VARCHAR(100),
    Duracion VARCHAR(100),
    Jornada VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Habilidades (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Categoria VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Usuario_Habilidad (
    ID SERIAL PRIMARY KEY,
    ID_Usuario INT REFERENCES Usuarios(ID) ON DELETE CASCADE,
    ID_Habilidad INT REFERENCES Habilidades(ID) ON DELETE CASCADE,
    Nivel VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Formacion (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(150),
    Tipo VARCHAR(100),
    Institucion VARCHAR(150),
    Area VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Usuario_Formacion (
    ID SERIAL PRIMARY KEY,
    ID_Usuario INT REFERENCES Usuarios(ID) ON DELETE CASCADE,
    ID_Formacion INT REFERENCES Formacion(ID) ON DELETE CASCADE,
    Anio_Inicio INT,
    Anio_Fin INT,
    Titulacion VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS Oferta_Habilidad (
    ID SERIAL PRIMARY KEY,
    ID_Oferta INT REFERENCES Oferta_Empleo(ID) ON DELETE CASCADE,
    ID_Habilidad INT REFERENCES Habilidades(ID) ON DELETE CASCADE,
    Nivel VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Oferta_Formacion (
    ID SERIAL PRIMARY KEY,
    ID_Oferta INT REFERENCES Oferta_Empleo(ID) ON DELETE CASCADE,
    ID_Formacion INT REFERENCES Formacion(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Recomendaciones (
    ID SERIAL PRIMARY KEY,
    ID_Oferta INT REFERENCES Oferta_Empleo(ID) ON DELETE CASCADE,
    ID_Usuario INT REFERENCES Usuarios(ID) ON DELETE CASCADE,
    Afinidad NUMERIC(5,2)
);

CREATE TABLE IF NOT EXISTS Formacion_Sugerida (
    ID SERIAL PRIMARY KEY,
    ID_Formacion INT REFERENCES Formacion(ID) ON DELETE CASCADE,
    ID_Usuario INT REFERENCES Usuarios(ID) ON DELETE CASCADE,
    Descripcion TEXT
);

CREATE TABLE IF NOT EXISTS Tendencias_Laborales (
    ID SERIAL PRIMARY KEY,
    ID_Formacion INT REFERENCES Formacion(ID) ON DELETE SET NULL,
    ID_Habilidad INT REFERENCES Habilidades(ID) ON DELETE SET NULL,
    Sector VARCHAR(100),
    Crecimiento_Demanda VARCHAR(100),
    Periodo VARCHAR(50)
);
"""

SQL_MYSQL = """
CREATE TABLE IF NOT EXISTS Usuarios (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    DNI VARCHAR(20) UNIQUE,
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    Edad INT,
    Email VARCHAR(150) UNIQUE,
    Telefono VARCHAR(20),
    Sexo ENUM('M', 'F', 'Otro'),
    Nacionalidad VARCHAR(100),
    Contrasena VARCHAR(255),
    Domicilio VARCHAR(255),
    Disponibilidad VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Experiencia_Laboral (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,
    Empresa VARCHAR(150),
    Puesto VARCHAR(150),
    Fecha_Inicio DATE,
    Fecha_Fin DATE,
    Descripcion TEXT,
    Sector VARCHAR(100),
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Prota (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(150),
    URL VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Oferta_Empleo (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Portal INT,
    Titulo VARCHAR(150),
    Empresa VARCHAR(150),
    Ubicacion VARCHAR(150),
    Descripcion TEXT,
    Salario DECIMAL(10,2),
    URL_Oferta VARCHAR(255),
    Sector VARCHAR(100),
    Tipo_Contrato VARCHAR(100),
    Duracion VARCHAR(100),
    Jornada VARCHAR(100),
    FOREIGN KEY (ID_Portal) REFERENCES Prota(ID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Habilidades (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100),
    Categoria VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Usuario_Habilidad (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,
    ID_Habilidad INT,
    Nivel VARCHAR(50),
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Habilidad) REFERENCES Habilidades(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Formacion (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(150),
    Tipo VARCHAR(100),
    Institucion VARCHAR(150),
    Area VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Usuario_Formacion (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,
    ID_Formacion INT,
    Anio_Inicio YEAR,
    Anio_Fin YEAR,
    Titulacion VARCHAR(150),
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Formacion) REFERENCES Formacion(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Oferta_Habilidad (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Oferta INT,
    ID_Habilidad INT,
    Nivel VARCHAR(50),
    FOREIGN KEY (ID_Oferta) REFERENCES Oferta_Empleo(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Habilidad) REFERENCES Habilidades(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Oferta_Formacion (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Oferta INT,
    ID_Formacion INT,
    FOREIGN KEY (ID_Oferta) REFERENCES Oferta_Empleo(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Formacion) REFERENCES Formacion(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Recomendaciones (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Oferta INT,
    ID_Usuario INT,
    Afinidad DECIMAL(5,2),
    FOREIGN KEY (ID_Oferta) REFERENCES Oferta_Empleo(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Formacion_Sugerida (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Formacion INT,
    ID_Usuario INT,
    Descripcion TEXT,
    FOREIGN KEY (ID_Formacion) REFERENCES Formacion(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Tendencias_Laborales (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Formacion INT,
    ID_Habilidad INT,
    Sector VARCHAR(100),
    Crecimiento_Demanda VARCHAR(100),
    Periodo VARCHAR(50),
    FOREIGN KEY (ID_Formacion) REFERENCES Formacion(ID) ON DELETE SET NULL,
    FOREIGN KEY (ID_Habilidad) REFERENCES Habilidades(ID) ON DELETE SET NULL
);
"""


def create_db_and_schema(db_name, config, creds, sql):
    """Crea la base de datos y su esquema para un motor específico."""
    
    print(f"\n--- Procesando {db_name} (Puerto {config['port']}) ---")
    conn = None
    
    try:
        if config["driver"] == "psycopg2":
            # PostgreSQL
            # Conexión inicial al servidor (usando la DB 'postgres' por defecto)
            conn = psycopg2.connect(
                host=creds["host"], port=config["port"],
                user=creds["user"], password=creds["password"],
                database=config["initial_db"]
            )
            conn.autocommit = True
            cursor = conn.cursor()

            print(f"    1. Eliminando y creando DB '{creds['db_name']}'...")
            try:
                # Intenta forzar la eliminación, ignorando el error si no existe
                cursor.execute(f"DROP DATABASE IF EXISTS {creds['db_name']} WITH (FORCE)") 
            except:
                pass 
            cursor.execute(f"CREATE DATABASE {creds['db_name']}")
            cursor.close()
            conn.close()

            # Reconexión a la nueva base de datos para crear las tablas
            conn = psycopg2.connect(
                host=creds["host"], port=config["port"],
                user=creds["user"], password=creds["password"],
                database=creds["db_name"]
            )
            cursor = conn.cursor()
            
            print("    2. Creando todas las tablas")
            cursor.execute(SQL_PG)
            conn.commit()
            print("Estructura creada correctamente.")
            


        elif config["driver"] in ["mysql", "mariadb"]:
            # MySQL / MariaDB
            if config["driver"] == "mysql":
                conn = mysql.connector.connect(
                    host=creds["host"], port=config["port"],
                    user=creds["user"], password=creds["password"]
                )
            else:
                conn = mysql.connector.connect(
                    host=creds["host"], port=config["port"],
                    user=creds["user"], password=creds["password"]
                )
            cursor = conn.cursor()
            
            print(f"    1. Eliminando y creando DB '{creds['db_name']}'...")
            cursor.execute(f"DROP DATABASE IF EXISTS {creds['db_name']}")
            cursor.execute(f"CREATE DATABASE {creds['db_name']}")
            cursor.execute(f"USE {creds['db_name']}")
            
            print("    2. Creando todas las tablas")
            for statement in sql.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            conn.commit()
            print("Estructura creada correctamente.")

    except Exception as e:
        print(f"ERROR en {db_name} (Puerto {config['port']}): {e}")
    finally:
        if conn: conn.close()



def main():
    print("--- INICIO DE LA CREACIÓN DE ESTRUCTURAS DE BASES DE DATOS ---")

    create_db_and_schema("PostgreSQL", SERVER_CONFIGS["PostgreSQL"], SERVER_CREDS_postgre, SQL_PG)
    create_db_and_schema("MySQL", SERVER_CONFIGS["MySQL"], SERVER_CREDS_mysql, SQL_MYSQL)
    create_db_and_schema("MariaDB", SERVER_CONFIGS["MariaDB"], SERVER_CREDS_mariaDB, SQL_MARIADB)

    print("\n--- PROCESO FINALIZADO ---")

if __name__ == "__main__":
    main()