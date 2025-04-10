# Módulo 1: Base de Datos con SQLite - Para Principiantes

## 🎯 Conceptos Básicos
SQLite es como un cuaderno digital donde guardamos información:
- Todo se guarda en **un solo archivo** (.db)
- No necesita internet ni servidores
- Usa comandos SQL (lenguaje universal para bases de datos)

## 📚 Funciones Principales (database.py)

### 1. `crear_tablas()`
```python
def crear_tablas():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    # Crea las tablas principales
    cursor.execute('CREATE TABLE IF NOT EXISTS proyectos(...)')
    conn.commit()
    conn.close()
```

**Propósito**: Prepara la estructura inicial de la base de datos  
**Detalles**:
- Crea/abre el archivo `user_data.db`
- Define 6 tablas principales:
  - `usuarios` (credenciales)
  - `Llaves` (Llaves de encriptamiento)
  - `documentos` (registro de archivos)
  - `proyectos` (datos de proyectos)
  - `Versiones` (Versiones de los documentos)
  - `Fechas` (Fechas de de las versiones)

### 2. `login_user(usuario, password)`
```python 
def login_user(usuario, password):
    hash_input = hash_text(password)
    # Compara con hash guardado
    return hash_guardado == hash_input
```
**Propósito**: Verifica credenciales de acceso  
**Proceso**:
1. Convierte la contraseña a hash SHA-256
2. Busca el usuario en la tabla `usuarios`
3. Compara los hashes de las contraseñas
4. Devuelve True/False dependiendo si coinciden

### 3. Operaciones Básicas

#### 🔄 CRUD por Entidad

Cada entidad en el sistema tiene operaciones básicas para:
- **Crear** (C): Añadir nuevos registros
- **Leer** (R): Obtener información existente  
- **Actualizar** (U): Modificar registros
- **Eliminar** (D): Remover registros

**📌 Proyectos** (La entidad principal):
- **Crear**: `crear_proyecto()`, `inicializar_tablas()`
- **Leer**: `obtener_proyectos()`, `obtener_datos_proyecto()`, `obtener_proyecto_completo()`
- **Actualizar**: `modificar_proyecto()`
- **Eliminar**: `eliminar_proyecto()`

**📄 Documentos** (Pertenecen a un proyecto):
- **Crear**: `crear_documento()`
- **Leer**: `obtener_documentos()`
- **Actualizar**: `modificar_documento()`
- **Eliminar**: `eliminar_documento()`

**🔄 Versiones** (Historial de documentos):
- **Crear**: `crear_version()`
- **Leer**: `obtener_versiones()`, `obtener_versiones_con_fechas()`
- **Actualizar**: `modificar_version()`

**📅 Fechas** (Asociadas a versiones):
- **Crear**: `crear_fecha()`
- **Leer**: `obtener_fechas()`
- **Actualizar**: `modificar_fecha()`
- **Eliminar**: `eliminar_fecha()`

**👤 Usuarios** (Acceso al sistema):
- **Crear**: `crear_usuario()`
- **Leer**: `login_user()`, `isadmin()`, `obtener_datos_usuarios()`
- **Eliminar**: `eliminar_usuario()`

**🔑 Llaves** (Encriptamiento de PDFs):
- **Crear**: `registrar_llave()` (Genera nuevas llaves de encriptamiento)
- **Leer**: `buscar_llave()` (Obtiene llaves para desencriptar)
*Nota: El proceso completo de encriptación/desencriptación se detallará en el Módulo 2*

**🔗 Relaciones entre entidades**:
- Cada **Proyecto** contiene múltiples **Documentos**
- Cada **Documento** tiene varias **Versiones**
- Cada **Versión** registra sus **Fechas** importantes
- Los **Usuarios** interactúan con todas las entidades
- Las **Llaves** protegen los datos sensibles

**Ejemplo Práctico**:
1. Un **Usuario** crea un **Proyecto**
2. Dentro del proyecto, se crean varios **Documentos**
3. Cada documento tiene múltiples **Versiones** con sus **Fechas**
4. Las **Llaves** aseguran que solo usuarios autorizados puedan acceder a los archivos
