# 🖥️ Módulo 3: Interfaz de Usuario con Flet

## � Introducción a Flet
Flet es un framework para construir interfaces multiplataforma con Python. Permite crear aplicaciones web, móviles y de escritorio con una API simple.

Principales características:
- 🧩 Basado en componentes (widgets)
- 🎨 Diseño responsive automático
- ⚡ Fácil manejo de eventos
- 🎨 Temas y estilos personalizables


### Ejemplo Rápido:
```python
import flet as ft

def main(page):
    btn = ft.ElevatedButton("¡Haz clic!")
    def click(e):
        page.add(ft.Text("¡Funciona!"))
    btn.on_click = click
    page.add(btn)

ft.app(target=main)
```
Este código crea una ventana con un botón que, al hacer clic, muestra un mensaje de texto


## Ejemplo Básico de Flet
```python
import flet as ft

def main(page: ft.Page):
    # Configuración básica de la página
    page.title = "Mi App Flet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Crear controles
    txt_nombre = ft.TextField(label="Nombre")
    btn_saludar = ft.ElevatedButton("Saludar")
    
    def saludar_click(e):
        # Manejo de eventos
        page.add(ft.Text(f"¡Hola, {txt_nombre.value}!"))
        txt_nombre.value = ""
        page.update()
    
    btn_saludar.on_click = saludar_click
    
    # Agregar controles a la página
    page.add(
        ft.Column([
            txt_nombre,
            btn_saludar
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)
```

Explicación del ejemplo:
1. `ft.Page` representa la ventana/ventana principal
2. Los controles (TextField, Button) se crean como objetos
3. Los eventos se manejan con funciones callback  
4. `page.add()` agrega controles a la interfaz
5. `page.update()` actualiza la UI después de cambios

Este ejemplo muestra el flujo básico:
- Crear controles → Configurar eventos → Agregar a página → Manejar interacciones

## Estructura de Componentes

### 1. Componentes Principales

#### Proyecto
```python
class Proyecto(ft.Column):
    """
    Representa un proyecto con sus atributos y controles asociados.
    Incluye funcionalidad para:
    - Mostrar información
    - Descargar reportes  
    - Eliminar proyectos
    - Seleccionar para ver detalles
    """
```

#### Documento  
```python
class Documento(ft.Column):
    """
    Representa un documento con sus versiones.
    Funcionalidades:
    - Mostrar información básica
    - Agregar nuevas versiones
    - Eliminar documentos
    - Ver detalles
    """
```
#### Version
```python
class Version(ft.Column):
    """
    Representa una versión específica de un documento:
    - Nombre de versión (Rev A, B, 0)
    - Estado (Aprobado, Pendiente)
    - Archivo PDF asociado
    - Transmitall correspondiente
    - Se integra con VersionDetalle para mostrar información extendida
    """
```

### 2. Componentes de Listado

#### ProyectoApp
```python
class ProyectoApp(ft.Column):
    """
    Listado principal de proyectos con:
    - Búsqueda
    - Creación de nuevos proyectos
    - Visualización de cantidad
    """
```

#### DocumentosApp
```python
class DocumentosApp(ft.Column): 
    """
    Listado de documentos de un proyecto con:
    - Filtrado por proyecto
    - Creación de nuevos documentos
    """
```

### 3. Componentes de Detalle

#### ProyectoDetalle
```python
class ProyectoDetalle(ft.Container):
    """
    Muestra detalles completos de un proyecto:
    - Nombre, fechas, cliente  
    - Permite edición
    """
```

#### DocumentoDetalle
```python
class DocumentoDetalle(ft.Container):
    """
    Muestra detalles completos de un documento:
    - Código y nombre
    - Tipo y disciplina  
    - Estado y revisión
    - Observaciones
    - Permite edición
    """
```

#### VersionDetalle
```python
class VersionDetalle(ft.Container):
    """
    Muestra detalles extendidos de una versión:
    - Información básica (nombre, estado)
    - Gestión de fechas (emisión, recepción, personalizadas)
    - Manejo de archivos PDF (subir/descargar)
    - Transmitall asociado
    - Relación con el documento padre
    """
```

## Vistas de la Aplicación


### 1. BienvenidaView
```python
class BienvenidaView(ft.View):
    """
    Vista inicial de la aplicación con:
    - Pantalla de bienvenida
    - Botón para registro/login
    - Redirección según estado de usuarios
    """
```

### 2. RegistroView  
```python
class RegistroView(ft.View):
    """
    Vista de registro de usuario con:
    - Campos para usuario y contraseña
    - Validación de campos
    - Creación de usuario administrador inicial
    - Generación de llave maestra
    """
```

### 3. LoginView
```python
class LoginView(ft.View):
    """
    Vista de autenticación con:
    - Validación de credenciales
    - Manejo de sesiones
    - Desencriptación de llave maestra
    - Redirección a Home
    """
```

### 4. HomeView
```python
class HomeView(ft.View):
    """
    Vista principal de la aplicación que contiene:
    - Listado de proyectos (ProyectoApp)
    - Detalles de proyectos (ProyectoDetalle)
    - Listado de documentos (DocumentosApp)
    - Detalles de documentos y versiones
    - Acceso a configuraciones
    """
```

### 5. ConfiguracionesView
```python
class ConfiguracionesView(ft.View):
    """
    Vista de configuración del sistema con:
    - Ajustes de usuario
    - Configuración de rutas
    - Preferencias de la aplicación
    """
```



## Patrones de Diseño

### 1. Componentes Reutilizables

#### ReusableModal
```python
class ReusableModal:
    """
    Diálogo modal reutilizable para:
    - Confirmaciones
    - Formularios
    - Mensajes
    """
```
### 2. CustomDatePicker
```python
class CustomDatePicker:
    """
    Componente reutilizable para selección de fechas.
    Se integra con campos de texto para mostrar la fecha seleccionada.
    """
```

### 2. Comunicación entre Componentes

Los componentes se comunican mediante:
- Referencias directas (inyección de dependencias)
- Eventos y callbacks
- Actualización de estado compartido

Ejemplo:
```python
# ProyectoApp recibe referencia a DetalleComponent
def __init__(self, detalle_component):
    self.detalle_component = detalle_component
```

## Consejos de Diseño

1. **Organización por Temas**:
   - Agrupar componentes relacionados
   - Separar lógica de presentación

2. **Estilos Centralizados**:
```python
# paleta.py
COLOR_PRIMARIO = "#4a6baf"
COLOR_TEXTO = "#333333" 
ESPACIADO_NORMAL = 10
```

3. **Patrón de Diseño**:
   - Usar composición sobre herencia
   - Mantener componentes pequeños y enfocados

4. **Manejo de Estado**:
   - Actualizar UI cuando cambian datos
   - Usar referencias para comunicación entre componentes

## Ejemplo de Uso

Creación de un nuevo proyecto:
```python
proyectos = ProyectoApp(detalle_component)
detalle = ProyectoDetalle(documentos_app)

page.add(
    ft.Row([proyectos, detalle])
)
```

## Extensión del Sistema

Para agregar nuevos componentes:
1. Crear nueva clase heredando de ft.Control
2. Implementar métodos requeridos
3. Integrar con componentes existentes

Ejemplo componente de gráficos:
```python
class GraficosProyecto(ft.Column):
    def __init__(self, proyecto_id):
        super().__init__()
        # Lógica para mostrar gráficos
```

