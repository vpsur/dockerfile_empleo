-- =======================
-- Tabla: Usuarios
-- =======================
CREATE TABLE Usuarios (
    ID SERIAL PRIMARY KEY,
    DNI VARCHAR(20) UNIQUE,
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    Edad INT,
    Email VARCHAR(150) UNIQUE,
    Telefono VARCHAR(20),
    Sexo VARCHAR(10), -- PostgreSQL no soporta ENUM directamente
    Nacionalidad VARCHAR(100),
    Contrasena VARCHAR(255),
    Domicilio VARCHAR(255),
    Disponibilidad VARCHAR(100)
);

-- =======================
-- Tabla: Experiencia_Laboral
-- =======================
CREATE TABLE Experiencia_Laboral (
    ID SERIAL PRIMARY KEY,
    ID_Usuario INT REFERENCES Usuarios(ID) ON DELETE CASCADE,
    Empresa VARCHAR(150),
    Puesto VARCHAR(150),
    Fecha_Inicio DATE,
    Fecha_Fin DATE,
    Descripcion TEXT,
    Sector VARCHAR(100)
);

-- =======================
-- Tabla: Prota (Portal)
-- =======================
CREATE TABLE Prota (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(150),
    URL VARCHAR(255)
);

-- =======================
-- Tabla: Oferta_Empleo
-- =======================
CREATE TABLE Oferta_Empleo (
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

-- =======================
-- Tabla: Habilidades
-- =======================
CREATE TABLE Habilidades (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Categoria VARCHAR(100)
);

-- =======================
-- Tabla: Usuario_Habilidad
-- =======================
CREATE TABLE Usuario_Habilidad (
    ID SERIAL PRIMARY KEY,
    ID_Usuario INT REFERENCES Usuarios(ID) ON DELETE CASCADE,
    ID_Habilidad INT REFERENCES Habilidades(ID) ON DELETE CASCADE,
    Nivel VARCHAR(50)
);

-- =======================
-- Tabla: Formacion
-- =======================
CREATE TABLE Formacion (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(150),
    Tipo VARCHAR(100),
    Institucion VARCHAR(150),
    Area VARCHAR(100)
);

-- =======================
-- Tabla: Usuario_Formacion
-- =======================
CREATE TABLE Usuario_Formacion (
    ID SERIAL PRIMARY KEY,
    ID_Usuario INT REFERENCES Usuarios(ID) ON DELETE CASCADE,
    ID_Formacion INT REFERENCES Formacion(ID) ON DELETE CASCADE,
    Anio_Inicio INT,
    Anio_Fin INT,
    Titulacion VARCHAR(150)
);

-- =======================
-- Tabla: Oferta_Habilidad
-- =======================
CREATE TABLE Oferta_Habilidad (
    ID SERIAL PRIMARY KEY,
    ID_Oferta INT REFERENCES Oferta_Empleo(ID) ON DELETE CASCADE,
    ID_Habilidad INT REFERENCES Habilidades(ID) ON DELETE CASCADE,
    Nivel VARCHAR(50)
);

-- =======================
-- Tabla: Oferta_Formacion
-- =======================
CREATE TABLE Oferta_Formacion (
    ID SERIAL PRIMARY KEY,
    ID_Oferta INT REFERENCES Oferta_Empleo(ID) ON DELETE CASCADE,
    ID_Formacion INT REFERENCES Formacion(ID) ON DELETE CASCADE
);

-- =======================
-- Tabla: Recomendaciones
-- =======================
CREATE TABLE Recomendaciones (
    ID SERIAL PRIMARY KEY,
    ID_Oferta INT REFERENCES Oferta_Empleo(ID) ON DELETE CASCADE,
    ID_Usuario INT REFERENCES Usuarios(ID) ON DELETE CASCADE,
    Afinidad NUMERIC(5,2)
);

-- =======================
-- Tabla: Formacion_Sugerida
-- =======================
CREATE TABLE Formacion_Sugerida (
    ID SERIAL PRIMARY KEY,
    ID_Formacion INT REFERENCES Formacion(ID) ON DELETE CASCADE,
    ID_Usuario INT REFERENCES Usuarios(ID) ON DELETE CASCADE,
    Descripcion TEXT
);

-- =======================
-- Tabla: Tendencias_Laborales
-- =======================
CREATE TABLE Tendencias_Laborales (
    ID SERIAL PRIMARY KEY,
    ID_Formacion INT REFERENCES Formacion(ID) ON DELETE SET NULL,
    ID_Habilidad INT REFERENCES Habilidades(ID) ON DELETE SET NULL,
    Sector VARCHAR(100),
    Crecimiento_Demanda VARCHAR(100),
    Periodo VARCHAR(50)
);
