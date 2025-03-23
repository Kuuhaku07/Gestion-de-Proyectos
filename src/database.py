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
    crear_tabla("Disciplina", {
        "id INTEGER PRIMARY KEY": "",
        "nombre TEXT UNIQUE": ""
    })
    crear_tabla("Status", {
        "id INTEGER PRIMARY KEY": "",
        "nombre TEXT UNIQUE": ""
    })
    crear_tabla("Documentos", {
        "id INTEGER PRIMARY KEY": "",
        "proyecto_id INTEGER REFERENCES Proyectos(id)": "",
        "codigo TEXT": "",
        "nombre TEXT": "",
        "tipo TEXT": "",
        "disciplina_id INTEGER REFERENCES Disciplina(id)": "",
        "status_id INTEGER REFERENCES Status(id)": "",
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

if __name__ == "__main__":
    #pruebas
    

    # Retrieve and print all projects
    proyectos = obtener_proyectos(nombre="Proyecto Al")
    for proyecto in proyectos:
        print(proyecto)

