import sqlite3
import os
import sys
from funciones import hash_text, xor_encrypt_decrypt

def conectar_db():
    # Ruta relativa al ejecutable (../data/documentos.db)
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    db_path = os.path.join(base_path, 'data/documentos.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
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
        "revision TEXT": "",
        "observaciones TEXT": "",
        "subproyecto TEXT DEFAULT \"\"": "",
        "Fase TEXT DEFAULT \"\"": ""
    })
    crear_tabla("Versiones", {
        "id INTEGER PRIMARY KEY": "",
        "documento_id INTEGER": "REFERENCES Documentos(id)",
        "nombre_version TEXT": "",
        "status TEXT": "", 
        "archivo TEXT": "",
        "transmitall TEXT": "",
        "transmitall_cliente TEXT DEFAULT \"\"": ""
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

def eliminar_usuario(username):
    """Elimina un usuario de la base de datos"""
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        # Eliminar usuario
        cursor.execute("DELETE FROM Usuarios WHERE username = ?", (username,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

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

def eliminar_proyecto(proyecto_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
        # Primero obtenemos todos los documentos del proyecto
        cursor.execute("SELECT id FROM Documentos WHERE proyecto_id = ?", (proyecto_id,))
        documentos = cursor.fetchall()
        
        # Para cada documento, eliminamos sus versiones y fechas
        for doc in documentos:
            documento_id = doc[0]
            # Eliminar fechas de las versiones del documento
            cursor.execute("""
                DELETE FROM Fechas 
                WHERE version_id IN (
                    SELECT id FROM Versiones WHERE documento_id = ?
                )
            """, (documento_id,))
            
            # Eliminar versiones del documento
            cursor.execute("DELETE FROM Versiones WHERE documento_id = ?", (documento_id,))
        
        # Eliminar todos los documentos del proyecto
        cursor.execute("DELETE FROM Documentos WHERE proyecto_id = ?", (proyecto_id,))
        
        # Finalmente eliminar el proyecto
        cursor.execute("DELETE FROM Proyectos WHERE id = ?", (proyecto_id,))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# End Region


# Region Documentos

def crear_documento(codigo, nombre, tipo, disciplina, status, observaciones, proyecto_id, revision, subproyecto="", Fase=""):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO Documentos (codigo, nombre, tipo, disciplina, status, observaciones, proyecto_id, revision, subproyecto, Fase) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (codigo, nombre, tipo, disciplina, status, observaciones, proyecto_id, revision, subproyecto, Fase))
    
    conn.commit()
    conn.close()

def obtener_documentos(proyecto_id=None, status=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "SELECT id, proyecto_id, codigo, nombre, tipo, disciplina, status, revision, observaciones, subproyecto, Fase FROM Documentos WHERE 1=1"
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

def eliminar_documento(documento_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Primero eliminamos todas las fechas asociadas a las versiones del documento
    cursor.execute("""
        DELETE FROM Fechas 
        WHERE version_id IN (
            SELECT id FROM Versiones WHERE documento_id = ?
        )
    """, (documento_id,))
    
    # Luego eliminamos todas las versiones del documento
    cursor.execute("DELETE FROM Versiones WHERE documento_id = ?", (documento_id,))
    
    # Finalmente eliminamos el documento
    cursor.execute("DELETE FROM Documentos WHERE id = ?", (documento_id,))
    
    conn.commit()
    conn.close()

def modificar_documento(id, codigo, nombre, tipo, disciplina, status, observaciones, revision, subproyecto=None, Fase=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    if subproyecto is not None and Fase is not None:
        cursor.execute("UPDATE Documentos SET codigo = ?, nombre = ?, tipo = ?, disciplina = ?, status = ?, observaciones = ?, revision = ?, subproyecto = ?, Fase = ? WHERE id = ?", 
                       (codigo, nombre, tipo, disciplina, status, observaciones, revision, subproyecto, Fase, id))
    elif subproyecto is not None:
        cursor.execute("UPDATE Documentos SET codigo = ?, nombre = ?, tipo = ?, disciplina = ?, status = ?, observaciones = ?, revision = ?, subproyecto = ? WHERE id = ?", 
                       (codigo, nombre, tipo, disciplina, status, observaciones, revision, subproyecto, id))
    elif Fase is not None:
        cursor.execute("UPDATE Documentos SET codigo = ?, nombre = ?, tipo = ?, disciplina = ?, status = ?, observaciones = ?, revision = ?, Fase = ? WHERE id = ?", 
                       (codigo, nombre, tipo, disciplina, status, observaciones, revision, Fase, id))
    else:
        cursor.execute("UPDATE Documentos SET codigo = ?, nombre = ?, tipo = ?, disciplina = ?, status = ?, observaciones = ?, revision = ? WHERE id = ?", 
                       (codigo, nombre, tipo, disciplina, status, observaciones, revision, id))
    
    conn.commit()
    conn.close()

# End Region


# Region Versiones

def crear_version(documento_id, nombre_version, status, archivo, transmitall="", transmitall_cliente=""):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Crear la versión
    cursor.execute("INSERT INTO Versiones (documento_id, nombre_version, status, archivo, transmitall, transmitall_cliente) VALUES (?, ?, ?, ?, ?, ?)", 
                   (documento_id, nombre_version, status, archivo, transmitall, transmitall_cliente))
    version_id = cursor.lastrowid
    
    # Crear fechas predeterminadas
    cursor.execute("INSERT INTO Fechas (version_id, nombre_fecha) VALUES (?, ?)", 
                   (version_id, "Fecha de Emisión"))
    cursor.execute("INSERT INTO Fechas (version_id, nombre_fecha) VALUES (?, ?)", 
                   (version_id, "Fecha de Recepción"))
    cursor.execute("INSERT INTO Fechas (version_id, nombre_fecha) VALUES (?, ?)", 
                   (version_id, "Fecha Emisión Cliente"))
    cursor.execute("INSERT INTO Fechas (version_id, nombre_fecha) VALUES (?, ?)", 
                   (version_id, "Fecha Recepción Cliente"))
    
    conn.commit()
    conn.close()

def obtener_versiones(documento_id=None, status=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "SELECT id, documento_id, nombre_version, status, archivo, transmitall, transmitall_cliente FROM Versiones WHERE 1=1"
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

def modificar_version(version_id, documento_id, nombre_version, status, archivo, transmitall=None, transmitall_cliente=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    if transmitall is not None and transmitall_cliente is not None:
        cursor.execute("UPDATE Versiones SET documento_id = ?, nombre_version = ?, status = ?, archivo = ?, transmitall = ?, transmitall_cliente = ? WHERE id = ?", 
                       (documento_id, nombre_version, status, archivo, transmitall, transmitall_cliente, version_id))
    elif transmitall is not None:
        cursor.execute("UPDATE Versiones SET documento_id = ?, nombre_version = ?, status = ?, archivo = ?, transmitall = ? WHERE id = ?", 
                       (documento_id, nombre_version, status, archivo, transmitall, version_id))
    elif transmitall_cliente is not None:
        cursor.execute("UPDATE Versiones SET documento_id = ?, nombre_version = ?, status = ?, archivo = ?, transmitall_cliente = ? WHERE id = ?", 
                       (documento_id, nombre_version, status, archivo, transmitall_cliente, version_id))
    else:
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

def eliminar_fecha(fecha_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Fechas WHERE id = ?", (fecha_id,))
    
    conn.commit()
    conn.close()

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
    SELECT v.id, v.documento_id, v.nombre_version, v.status, v.archivo, v.transmitall,
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
        version_data = resultados[0][:6]  # Version data including transmitall
        fechas_data = [{"nombre_fecha": row[5], "fecha": row[6]} for row in resultados if row[5] is not None]
        return [version_data, fechas_data]
    
    return None  # Return None if no results found

# End Region

def obtener_proyecto_completo(proyecto_id):
    """Obtiene todos los datos de un proyecto incluyendo documentos, versiones y fechas"""
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Obtener datos del proyecto
    cursor.execute("SELECT * FROM Proyectos WHERE id = ?", (proyecto_id,))
    proyecto = cursor.fetchone()
    
    if not proyecto:
        conn.close()
        return None
    
    # Obtener documentos del proyecto
    cursor.execute("SELECT * FROM Documentos WHERE proyecto_id = ?", (proyecto_id,))
    documentos = cursor.fetchall()
    
    resultado = {
        'proyecto': proyecto,
        'documentos': []
    }
    
    # Para cada documento, obtener sus versiones y fechas
    for doc in documentos:
        documento_id = doc[0]
        
        # Obtener versiones del documento
        cursor.execute("SELECT * FROM Versiones WHERE documento_id = ?", (documento_id,))
        versiones = cursor.fetchall()
        
        doc_data = {
            'documento': doc,
            'versiones': []
        }
        
        for version in versiones:
            version_id = version[0]
            
            # Obtener fechas de la versión
            cursor.execute("SELECT * FROM Fechas WHERE version_id = ?", (version_id,))
            fechas = cursor.fetchall()
            
            doc_data['versiones'].append({
                'version': version,
                'fechas': fechas
            })
        
        resultado['documentos'].append(doc_data)
    
    conn.close()
    return resultado


if __name__ == "__main__":
    # Prueba detallada de la función obtener_proyecto_completo
    print("\n=== PRUEBA DETALLADA DE OBTENER_PROYECTO_COMPLETO ===")
    
    # Probar con proyecto_id = 1
    proyecto_id = 1
    datos = obtener_proyecto_completo(proyecto_id)
    
    if datos:
        # Mostrar todos los campos del proyecto
        print("\n=== DATOS DEL PROYECTO ===")
        print(f"ID: {datos['proyecto'][0]}")
        print(f"Nombre: {datos['proyecto'][1]}")
        print(f"Fecha inicio: {datos['proyecto'][2]}")
        print(f"Fecha fin: {datos['proyecto'][3]}")
        print(f"Cliente: {datos['proyecto'][4]}")
        print(f"Código: {datos['proyecto'][5]}")
        
        # Mostrar todos los documentos con todos sus campos
        print("\n=== DOCUMENTOS ===")
        for i, doc in enumerate(datos['documentos']):
            print(f"\nDocumento {i+1}:")
            print(f"ID: {doc['documento'][0]}")
            print(f"Proyecto ID: {doc['documento'][1]}")
            print(f"Código: {doc['documento'][2]}")
            print(f"Nombre: {doc['documento'][3]}")
            print(f"Tipo: {doc['documento'][4]}")
            print(f"Disciplina: {doc['documento'][5]}")
            print(f"Status: {doc['documento'][6]}")
            print(f"Revisión: {doc['documento'][7]}")
            print(f"Observaciones: {doc['documento'][8]}")
            
            # Mostrar todas las versiones
            print(f"\n  Versiones ({len(doc['versiones'])}):")
            for j, version in enumerate(doc['versiones']):
                print(f"\n  Versión {j+1}:")
                print(f"  ID: {version['version'][0]}")
                print(f"  Documento ID: {version['version'][1]}")
                print(f"  Nombre: {version['version'][2]}")
                print(f"  Status: {version['version'][3]}")
                print(f"  Archivo: {version['version'][4]}")
                print(f"  Transmittal: {version['version'][5]}")
                
                # Mostrar todas las fechas
                print("\n    Fechas:")
                for fecha in version['fechas']:
                    print(f"    ID: {fecha[0]}")
                    print(f"    Versión ID: {fecha[1]}")
                    print(f"    Nombre: {fecha[2]}")
                    print(f"    Fecha: {fecha[3]}")
                    print("    ---")
    else:
        print(f"No se encontró el proyecto con ID {proyecto_id}")
        
    print("\nPrueba completada. Todos los campos mostrados.")
