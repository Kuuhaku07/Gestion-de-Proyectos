import sqlite3
from funciones import hash_text, xor_encrypt_decrypt
def conectar_db():
    conn = sqlite3.connect('../data/documentos.db')

    return conn


def crear_tabla(tabla, columnas):

    # Establece una conexión a la base de datos utilizando la función conectar_db.
    conn = conectar_db()
    
    # Crea un cursor a partir de la conexión. El cursor se utiliza para ejecutar comandos SQL.
    cursor = conn.cursor()
    
    # Construye una cadena que representa las columnas y sus tipos en formato SQL.
    # Se utiliza una comprensión de lista para crear una lista de strings en el formato "nombre_columna tipo_dato".
    # Luego, se unen esos strings en una sola cadena, separándolos por comas.
    columnas_sql = ', '.join([f"{columna} {tipo}" for columna, tipo in columnas.items()])
    
    # Ejecuta la consulta SQL para crear la tabla.
    # La consulta utiliza "CREATE TABLE IF NOT EXISTS" para evitar errores si la tabla ya existe.
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tabla} ({columnas_sql});")
    
    # Confirma los cambios realizados en la base de datos, asegurando que la tabla se cree.
    conn.commit()
    
    # Cierra la conexión a la base de datos para liberar recursos.
    conn.close()

# Al llamar esta funcion se inicializan las tablas de la base de datos
def inicializar_tablas():
    crear_tabla("Usuarios", {
        "id INTEGER PRIMARY KEY": "",
        "username TEXT": "",
        "password TEXT": "",
        "isadmin BOOLEAN": ""
    })
    crear_tabla("Llaves", {
        "id INTEGER PRIMARY KEY": "",
        "llave TEXT": "",
        "hash TEXT": ""
    })
    crear_tabla("Proyectos", {
        "id INTEGER PRIMARY KEY": "",
        "nombre TEXT": "",
        "fecha_inicio DATE": "",
        "fecha_fin DATE": "",
        "cliente TEXT": "",
        "codigo_proyecto TEXT": ""
    })

    crear_tabla("Documentos", {
        "id INTEGER PRIMARY KEY": "",
        "proyecto_id INTEGER REFERENCES Proyectos(id)": "",
        "codigo TEXT": "",
        "nombre TEXT": "",
        "tipo TEXT": "",
        "disciplina TEXT": "",
        "status TEXT": "",
        "observaciones TEXT": ""
    })
    crear_tabla("Versiones", {
        "id INTEGER PRIMARY KEY": "",
        "documento_id INTEGER": "REFERENCES Documentos(id)",
        "nombre_version TEXT": "",
        "status TEXT": "", 
        "archivo TEXT": ""
    })
    crear_tabla("Fechas", {
        "id INTEGER PRIMARY KEY": "",
        "version_id INTEGER": "REFERENCES Versiones(id)",
        "nombre_fecha TEXT": "",
        "fecha DATE": ""
    })

    
#Region Usuario

def crear_usuario(username, password, isadmin):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO Usuarios (username, password, isadmin) VALUES (?, ?, ?)", (username, password, isadmin))
    
    conn.commit()
    conn.close()

def verificar_usuarios_existentes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Usuarios")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def login_user(username, password):
    # Establish a connection to the database
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Query the database to find the user
    cursor.execute("SELECT password FROM Usuarios WHERE username = ?", (username,))
    user_data = cursor.fetchone()  # Fetch the user data

    if user_data:
        stored_hashed_password = user_data[0] 
        conn.close()  # Close the connection
        return hash_text(password) == stored_hashed_password  # Compare the hashed passwords
    
    conn.close()  # Close the connection if user not found
    return False  # User not found

def isadmin(username):
    # Establish a connection to the database
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Query the database to find the user's admin status
    cursor.execute("SELECT isadmin FROM Usuarios WHERE username = ?", (username,))
    user_data = cursor.fetchone()  # Fetch the user data

    conn.close()  # Close the connection
    
    if user_data:
        return user_data[0]  # Return the admin status (True/False)
    
    return False  # User not found or not an admin

def obtener_datos_usuarios():

    conn = conectar_db()  # Update with your actual database path
    cursor = conn.cursor()
    
    # Query to select user data
    cursor.execute("SELECT username, isadmin FROM Usuarios")  # Adjusted to the correct table name

    usuarios = cursor.fetchall()  # Fetch all user records
    
    # Close the connection
    conn.close()
    
    return usuarios


#End Region

#Region Llave
def registrar_llave(llave, hash):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Llaves (llave, hash) VALUES (?, ?)", (llave, hash))
    conn.commit()
    conn.close()

def buscar_llave(hash):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT llave FROM Llaves WHERE hash = ?", (hash,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
#End Region


# Region Proyecto


def obtener_datos_proyecto(proyecto_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Proyectos WHERE id = ?", (proyecto_id,))
    proyecto = cursor.fetchone()
    
    conn.close()
    return proyecto

def crear_proyecto(nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO Proyectos (nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto) VALUES (?, ?, ?, ?, ?)", 
                   (nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto))
    
    conn.commit()
    conn.close()

def modificar_proyecto(proyecto_id, nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE Proyectos SET nombre = ?, fecha_inicio = ?, fecha_fin = ?, cliente = ?, codigo_proyecto = ? WHERE id = ?", 
                   (nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto, proyecto_id))
    
    conn.commit()
    conn.close()

def obtener_proyectos(nombre=None, codigo=None, cliente=None, sort="alfabetico",same=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM Proyectos WHERE 1=1"
    params = []

    if same and nombre and codigo:
        query += " AND (nombre LIKE ? OR codigo_proyecto LIKE ?)"
        params.append(f"%{nombre}%")
        params.append(f"%{codigo}%")
    else:
        if nombre:
            query += " AND nombre LIKE ?"
            params.append(f"%{nombre}%")
        
        if codigo:
            query += " AND codigo_proyecto LIKE ?"
            params.append(f"%{codigo}%")
    
    
    if cliente:
        query += " AND cliente LIKE ?"
        params.append(f"%{cliente}%")
    
    if sort == "creacion":
        query += " ORDER BY fecha_inicio ASC"
    elif sort == "finalizacion":
        query += " ORDER BY fecha_fin ASC, CASE WHEN fecha_fin IS NULL THEN 1 ELSE 0 END"
    elif sort == "alfabetico":
        query += " ORDER BY nombre ASC"
    
    cursor.execute(query, params)
    proyectos = cursor.fetchall()
    
    conn.close()
    return proyectos


# End Region


# Region Documentos

def crear_documento(codigo, nombre, tipo, disciplina, status, observaciones, proyecto_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO Documentos (codigo, nombre, tipo, disciplina, status, observaciones, proyecto_id) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (codigo, nombre, tipo, disciplina, status, observaciones, proyecto_id))
    
    conn.commit()
    conn.close()

def obtener_documentos(proyecto_id=None, status=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM Documentos WHERE 1=1"
    params = []

    if proyecto_id:
        query += " AND proyecto_id = ?"
        params.append(proyecto_id)
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    cursor.execute(query, params)
    documentos = cursor.fetchall()
    
    conn.close()
    return documentos

def modificar_documento(documento_id, codigo, nombre, tipo, disciplina, status, observaciones):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE Documentos SET codigo = ?, nombre = ?, tipo = ?, disciplina = ?, status = ?, observaciones = ? WHERE id = ?", 
                   (codigo, nombre, tipo, disciplina, status, observaciones, documento_id))
    
    conn.commit()
    conn.close()

# End Region


# Region Versiones

def crear_version(documento_id, nombre_version, status, archivo):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO Versiones (documento_id, nombre_version, status, archivo) VALUES (?, ?, ?, ?)", 
                   (documento_id, nombre_version, status, archivo))
    
    conn.commit()
    conn.close()

def obtener_versiones(documento_id=None, status=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM Versiones WHERE 1=1"
    params = []

    if documento_id:
        query += " AND documento_id = ?"
        params.append(documento_id)
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    cursor.execute(query, params)
    versiones = cursor.fetchall()
    
    conn.close()
    return versiones

def modificar_version(version_id, documento_id, nombre_version, status, archivo):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE Versiones SET documento_id = ?, nombre_version = ?, status = ?, archivo = ? WHERE id = ?", 
                   (documento_id, nombre_version, status, archivo, version_id))
    
    conn.commit()
    conn.close()

# End Region


# Region Fechas

def crear_fecha(version_id, nombre_fecha, fecha=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO Fechas (version_id, nombre_fecha, fecha) VALUES (?, ?, ?)", 
                   (version_id, nombre_fecha, fecha))
    
    conn.commit()
    conn.close()

def obtener_fechas(version_id=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM Fechas WHERE 1=1"
    params = []

    if version_id:
        query += " AND version_id = ?"
        params.append(version_id)
    
    cursor.execute(query, params)
    fechas = cursor.fetchall()
    
    conn.close()
    return fechas

def modificar_fecha(fecha_id, version_id, nombre_fecha, fecha):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE Fechas SET version_id = ?, nombre_fecha = ?, fecha = ? WHERE id = ?", 
                   (version_id, nombre_fecha, fecha, fecha_id))
    
    conn.commit()
    conn.close()

def obtener_versiones_con_fechas(version_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Query to get version data and associated dates
    query = """
    SELECT v.id, v.documento_id, v.nombre_version, v.status, v.archivo, 
           f.nombre_fecha, f.fecha 
    FROM Versiones v 
    LEFT JOIN Fechas f ON v.id = f.version_id
    WHERE v.id = ?
    """
    
    cursor.execute(query, (version_id,))
    resultados = cursor.fetchall()
    
    conn.close()
    
    # Organizing the results
    if resultados:
        version_data = resultados[0][:5]  # Version data
        fechas_data = [{"nombre_fecha": row[5], "fecha": row[6]} for row in resultados if row[5] is not None]
        return [version_data, fechas_data]
    
    return None  # Return None if no results found

# End Region


if __name__ == "__main__":
    #pruebas
    

    # Modify the empty date with id = 3 to add a new value
    modificar_fecha(3, 1, "Fecha Ahora no vacia", "2023-10-15")
    print("Fecha modificada para id = 3.")
    # Retrieve versions with their associated dates
     # Test the function to get versions with dates for version_id = 1
    versiones_con_fechas = obtener_versiones_con_fechas(1)
    print("Versiones con fechas para version_id = 1:")
    
    if versiones_con_fechas:
        version_data = versiones_con_fechas[0]  # Version data
        fechas_data = versiones_con_fechas[1]  # Dates data
        
        # Print version details
        print("Datos de la versión:")
        print(f"ID: {version_data[0]}")
        print(f"Documento ID: {version_data[1]}")
        print(f"Nombre de la versión: {version_data[2]}")
        print(f"Status: {version_data[3]}")
        print(f"Archivo: {version_data[4]}")
        
        # Print associated dates
        print("Fechas asociadas:")
        for fecha in fechas_data:
            print(f"Nombre de la fecha: {fecha['nombre_fecha']}, Fecha: {fecha['fecha']}")
    else:
        print("No se encontraron datos para la versión especificada.")
