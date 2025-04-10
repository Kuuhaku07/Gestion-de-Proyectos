# 🚀 Introducción al Sistema de Gestión Documental

## 🎯 ¿Qué es este sistema?
Herramienta completa para:
- Organizar proyectos y documentos
- Proteger información confidencial
- Mantener historial de versiones
- Colaborar entre usuarios

## 🔧 Configuración Inicial
- **Requisitos**: Python 3.10+, pip
- **Instalación**:
  ```bash
  pip install -r requirements.txt
  ```
- **Primer inicio**:
  - La aplicación creará automáticamente:
    - Base de datos en `user_data.db`
    - Directorio para documentos

## 🏗️ Estructura Clave
- **Persistencia**:
  - SQLite para metadatos
  - Sistema de archivos para documentos
- **Seguridad**:
  - Autenticación con hash SHA-256
  - Llave maestra cifrada
  - Documentos con AES-256

## 🔄 Flujo Principal
1. 🔑 Autenticación → 
2. 📂 Gestión Proyectos → 
3. 📄 Administración Documentos → 
4. ⏱️ Control Versiones

## 🎨 Personalización
- **UI**: Modificar `paleta.py` para colores
- **Reportes**: Ajustar plantillas en `funciones.py`
- **DB**: Esquema en `database.py`

