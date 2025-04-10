# Sistema de Información para Documentos de Proyectos

## Descripción
Sistema de gestión documental para proyectos que permite:
- Almacenamiento seguro y organizado de documentos
- Control de versiones de documentos
- Generación de reportes (completos y Rev 0)
- Gestión de usuarios y permisos

## Características Principales
- 🛡️ Encriptación de documentos sensibles
- 📂 Organización por proyectos, documentos y versiones
- 🔍 Búsqueda y filtrado avanzado
- 📊 Generación de reportes en PDF
- 👥 Sistema de autenticación de usuarios

## Requisitos
- Python 3.10+
- Flet (pip install flet)
- SQLite3
- Bibliotecas adicionales (ver requirements.txt)

## Instalación
1. Clonar el repositorio:
```bash
git clone https://github.com/Kuuhaku07/Gestion-de-Proyectos.git
cd Gestion-de-Proyectos
```

2. Crear entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso
Para iniciar la aplicación:
```bash
python src/main.py
```

### Configuración Inicial
1. Al primer inicio, registrar un usuario administrador
2. Configurar la ruta de descarga en Configuraciones
3. Importar o crear nuevos proyectos

## Mecanismo de Encriptación
El sistema implementa un esquema de seguridad de dos niveles:

1. **Nivel de Autenticación**:
   - Contraseñas almacenadas como hash SHA-256
   - Llave maestra encriptada con XOR usando la contraseña

2. **Nivel de Documentos**:
   - Archivos PDF encriptados con AES-256
   - La llave de encriptación se deriva de la llave maestra
   - Ruta de almacenamiento configurable


### Estructura de Archivos
```
├── src/
│   ├── componentes.py     # Componentes UI principales
│   ├── configuraciones.py # Configuración del sistema
│   ├── database.py        # Operaciones con la base de datos
│   ├── funciones.py       # Funciones auxiliares
│   ├── main.py            # Punto de entrada
│   └── paleta.py          # Configuración de colores
├── docs/                  # Documentación adicional
└── requirements.txt       # Dependencias
```




## Descripción de cada archivo de codigo

### Base de Datos (database.py)
- **Responsabilidad**: Gestiona todas las operaciones con SQLite
- **Funciones clave**:
  - `crear_tablas()`: Inicializa la estructura de la base de datos
  - `login_user()`: Maneja la autenticación de usuarios
  - Operaciones CRUD para proyectos, documentos y versiones
  - Encriptación/desencriptación de la llave maestra

### Componentes UI (componentes.py)
- **Clases principales**:
  - `Proyecto`: Maneja la visualización y acciones de proyectos
  - `Documento`: Gestiona la interfaz de documentos
  - `Version`: Controla el versionado de documentos
  - `ReusableModal`: Componente modal reutilizable

### Funciones Auxiliares (funciones.py)
- **Utilidades clave**:
  - Generación de reportes PDF (completo y Rev 0)
  - Funciones de hashing y encriptación
  - Manipulación de archivos PDF
  - Helpers para la interfaz gráfica

### Configuración (configuraciones.py)
- **Contiene**:
  - Vista de configuración del sistema
  - Gestión de rutas de almacenamiento
  - Preferencias de usuario

### Punto de Entrada (main.py)
- **Responsabilidades**:
  - Configuración inicial de la aplicación
  - Manejo de rutas y vistas
  - Inicialización del sistema

