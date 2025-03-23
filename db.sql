CREATE TABLE IF NOT EXISTS Usuarios (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    isadmin BOOLEAN
);

CREATE TABLE IF NOT EXISTS Llaves (
    id INTEGER PRIMARY KEY,
    llave TEXT,
    hash TEXT
);

CREATE TABLE IF NOT EXISTS Proyectos (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    cliente TEXT,
    codigo_proyecto TEXT
);

CREATE TABLE IF NOT EXISTS Documentos (
    id INTEGER PRIMARY KEY,
    proyecto_id INTEGER REFERENCES Proyectos(id),
    codigo TEXT,
    nombre TEXT,
    tipo TEXT,
    disciplina TEXT,
    status TEXT,
    observaciones TEXT
);

CREATE TABLE IF NOT EXISTS Versiones (
    id INTEGER PRIMARY KEY,
    documento_id INTEGER REFERENCES Documentos(id),
    nombre_version TEXT,
    archivo TEXT
);

CREATE TABLE IF NOT EXISTS Fechas (
    id INTEGER PRIMARY KEY,
    version_id INTEGER REFERENCES Versiones(id),
    nombre_fecha TEXT,
    fecha DATE
);