import datetime
import flet as ft
from database import *
from funciones import *
from flet import View,Icons, Page, AppBar, ElevatedButton,TextField, Text, RouteChangeEvent, ViewPopEvent,CrossAxisAlignment,MainAxisAlignment
from paleta import *

class Proyecto(ft.Column):
    def __init__(self, id, nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto, detalle_component):
        super().__init__()  # Llama al constructor de ft.Column
        self.id = id
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.cliente = cliente
        self.codigo_proyecto = codigo_proyecto
        self.detalle_component = detalle_component 

        self.edit_name = ft.TextField(expand=1, value=self.mostrar_info())
        
        self.display_task = ft.Container(
            content=ft.Text(
                value=self.mostrar_info(),
                color=COLOR_TEXTO,
                size=TEXTO_NORMAL
            ),
            on_click=self.select_clicked,  
            padding=ESPACIADO_NORMAL,
            border_radius=BORDE_RADIO,
            bgcolor=COLOR_ITEM,
            width=300,
            shadow=SOMBRA_NORMAL,
            ink=True,  # Efecto de ripple al hacer clic
            on_hover=self.on_hover
        )
        
        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.DOWNLOAD,
                            tooltip="Descargar Proyecto",
                            on_click=self.download_clicked,
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            tooltip="Delete Project",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.controls = [self.display_view]

    def mostrar_info(self):
        # Devuelve la información del proyecto como una cadena
        return f"{self.codigo_proyecto} - {self.nombre}"

    def download_clicked(self, e):
        dlg = ReusableModal(
            title="Descargando",
            content=f"Descargando: {self.nombre}",
            actions=[ft.TextButton("Close", on_click=lambda e: dlg.close(self.page))],
            modal=False
        )
        dlg.open(self.page)

    def delete_clicked(self, e):
        # Crear el modal de confirmación
        accept_button = ft.TextButton(
            "Eliminar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_ERROR
            ),
            on_click=lambda e: self.confirmar_eliminacion(dlg)
        )
        cancel_button = ft.TextButton(
            "Cancelar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: dlg.close(self.page)
        )

        dlg = ReusableModal(
            title="Confirmar Eliminación",
            content=f"¿Está seguro que desea eliminar el proyecto '{self.nombre}'? Esta acción también eliminará todos sus documentos, versiones y fechas asociadas.",
            actions=[
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def confirmar_eliminacion(self, dlg):
        try:
            # Eliminar el proyecto de la base de datos
            eliminar_proyecto(self.id)
            
            # Cerrar el modal
            dlg.close(self.page)
            
            # Limpiar detalles del proyecto
            self.detalle_component.details_column.controls.clear()
            self.detalle_component.initial_message.visible = True
            self.detalle_component.details_column.controls.append(
                self.detalle_component.initial_message
            )
            self.detalle_component.update()
            
            # Limpiar lista de documentos
            self.detalle_component.documentos_app.documents.controls.clear()
            self.detalle_component.documentos_app.items_left.value = "0 Documentos Encontrados"
            self.detalle_component.documentos_app.update()
            
            # Recargar la lista de proyectos
            self.detalle_component.proyecto_app.search_projects(None)
            
        except Exception as e:
            # Mostrar mensaje de error
            error_dlg = ReusableModal(
                title="Error",
                content=f"Error al eliminar el proyecto: {str(e)}",
                actions=[
                    ft.TextButton(
                        "Aceptar",
                        style=ft.ButtonStyle(
                            color=COLOR_TEXTO_BOTON,
                            bgcolor=COLOR_BOTON
                        ),
                        on_click=lambda e: error_dlg.close(self.page)
                    )
                ],
                modal=True
            )
            error_dlg.open(self.page)

    def select_clicked(self, e):
        # Lógica para seleccionar el proyecto
        self.detalle_component.mostrar_detalles(
            self.id,
            self.nombre,
            self.fecha_inicio,
            self.fecha_fin,
            self.cliente,
            self.codigo_proyecto
        )
        self.detalle_component.documentos_app.mostrar_documentos(self.id)  
        
        # Limpiar detalles del documento y versiones
        doc_detalle = self.detalle_component.documentos_app.documento_detalle
        ver_detalle = self.detalle_component.documentos_app.version_detalle
        
        # Limpiar y actualizar detalles del documento
        doc_detalle.details_column.controls.clear()
        doc_detalle.initial_message.visible = True
        doc_detalle.details_column.controls.append(doc_detalle.initial_message)
        
        # Limpiar y actualizar detalles de la versión
        ver_detalle.details_column.controls.clear()
        ver_detalle.initial_message.visible = True
        ver_detalle.details_column.controls.append(ver_detalle.initial_message)
        
        # Actualizar la interfaz
        doc_detalle.update()
        ver_detalle.update()

    def on_hover(self, e):
        self.display_task.bgcolor = COLOR_ITEM_HOVER if e.data == "true" else COLOR_ITEM
        self.display_task.update()

class ReusableModal:
    def __init__(self, title, content, actions, modal=True):
        self.title = title
        self.content = content
        self.actions = actions
        self.modal = modal
        self.dialog = ft.AlertDialog(
            title=ft.Text(
                self.title,
                size=TEXTO_GRANDE,
                color=COLOR_TEXTO,
                weight=ft.FontWeight.BOLD
            ),
            content=ft.Text(
                self.content,
                size=TEXTO_NORMAL,
                color=COLOR_TEXTO_SECUNDARIO
            ) if self.content else None,
            actions=self.actions,
            actions_alignment=ft.MainAxisAlignment.END,
            modal=self.modal,
            on_dismiss=self.on_dismiss,
            bgcolor=COLOR_FONDO,
            shape=ft.RoundedRectangleBorder(radius=BORDE_RADIO)
        )

    def on_dismiss(self, e):
        pass

    def open(self, page):
        page.open(self.dialog)
    def close(self, page):
        page.close(self.dialog)


        
class ProyectoApp(ft.Column):
    def __init__(self,detalle_component):
        super().__init__()
        self.detalle_component=detalle_component
        self.search_name = ft.TextField(
            hint_text="Nombre del proyecto",
            expand=True,
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        
        self.projects = ft.ListView(
            spacing=ESPACIADO_NORMAL,
            width=400,
            height=500,  # Aumentamos la altura ya que quitamos el texto redundante
        )
            
        self.items_left = ft.Text(
            "0 proyectos",
            color=COLOR_TEXTO_SECUNDARIO,
            size=TEXTO_NORMAL
        )

        self.width = 400
        self.controls = [
            ft.Row(
                [ft.Text(
                    value="Proyectos",
                    color=COLOR_TEXTO,
                    size=TEXTO_GRANDE,
                    weight=ft.FontWeight.BOLD
                )],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.search_name,
                    ft.FloatingActionButton(
                        icon=ft.icons.SEARCH,
                        bgcolor=COLOR_BOTON,
                        foreground_color=COLOR_TEXTO_BOTON,
                        on_click=self.search_projects,
                        tooltip="Buscar proyecto"
                    ),
                ],
            ),
            ft.Row(
                controls=[
                    self.items_left,
                    ft.FloatingActionButton(
                        text="Nuevo",
                        height=20,
                        bgcolor=COLOR_BOTON,
                        foreground_color=COLOR_TEXTO_BOTON,
                        on_click=self.open_project_modal,
                        tooltip="Crear nuevo proyecto"
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            self.projects,
        ]

    def open_project_modal(self, e):
        # Create a modal for project data entry
        project_name = ft.TextField(
            hint_text="Nombre del proyecto",
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        
        start_date = ft.TextField(
            hint_text="Fecha de inicio",
            disabled=True,
            border_color=COLOR_BORDE,
            text_size=TEXTO_NORMAL
        )
        start_date_button = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            icon_color=COLOR_BOTON,
            on_click=lambda e: CustomDatePicker(self.page, start_date).open()
        )
        end_date = ft.TextField(
            hint_text="Fecha de fin",
            disabled=True,
            border_color=COLOR_BORDE,
            text_size=TEXTO_NORMAL
        )
        end_date_button = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            icon_color=COLOR_BOTON,
            on_click=lambda e: CustomDatePicker(self.page, end_date).open()
        )
        
        client = ft.TextField(
            hint_text="Cliente",
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        project_code = ft.TextField(
            hint_text="Código del proyecto",
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        warning_signal = ft.Container(
            content=ft.Column(
                controls=[
                    create_info_box(
                        text_color=COLOR_TEXTO_ERROR,
                        background_color=COLOR_ERROR,
                        message="Por favor, complete todos los campos."
                    ),
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=350,
            visible=False
        )
        accept_button = ft.TextButton(
            "Aceptar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: self.submit_project_data(
                project_name.value,
                start_date.value,
                end_date.value,
                client.value,
                project_code.value,
                warning_signal,
                dlg
            )
        )
        cancel_button = ft.TextButton(
            "Cancelar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_ERROR
            ),
            on_click=lambda e: dlg.close(self.page)
        )

        dlg = ReusableModal(
            title="Nuevo Proyecto",
            content="",
            actions=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                warning_signal,
                                      project_name,
                                ft.Row(
                                    controls=[start_date, start_date_button],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Row(
                                    controls=[end_date, end_date_button],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                      client,
                                project_code
                            ],
                            spacing=ESPACIADO_NORMAL,
                    alignment=ft.MainAxisAlignment.CENTER,
                            width=350
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(height=ESPACIADO_GRANDE),
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def submit_project_data(self, nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto,warning_signal,dlg):
        if not nombre or not fecha_inicio or not fecha_fin or not cliente or not codigo_proyecto:
            warning_signal.visible = True  # Mostrar el mensaje de advertencia
            self.page.update()
        else:
            warning_signal.visible = False  # Ocultar el mensaje de advertencia
            # Si todos los campos están completos, proceder con el envío de datos
            crear_proyecto(nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto)
            dlg.close(self.page)
            self.search_projects(None)  # Llamar a search_projects con None como evento


    def search_projects(self, e):
        search_term = self.search_name.value
        proyectos = obtener_proyectos(nombre=search_term, codigo=search_term, same=True)  # Call the database function with the search term
        self.projects.controls.clear()  # Clear the current project list
        for proyecto_data in proyectos:
            project = Proyecto(
                id=proyecto_data[0],
                nombre=proyecto_data[1],
                fecha_inicio=proyecto_data[2],
                fecha_fin=proyecto_data[3],
                cliente=proyecto_data[4],
                codigo_proyecto=proyecto_data[5],
                detalle_component=self.detalle_component
            )
            self.projects.controls.append(project)
        self.items_left.value = f"{len(proyectos)} Proyecto(s) Encontrados"
        self.update()  # Update the interface to reflect the loaded projects
    
    def cargar_proyectos(self):
        proyectos = obtener_proyectos()  # Fetch all projects from the database
        for proyecto_data in proyectos:
            project = Proyecto(
                id=proyecto_data[0],
                nombre=proyecto_data[1],
                fecha_inicio=proyecto_data[2],
                fecha_fin=proyecto_data[3],
                cliente=proyecto_data[4],
                codigo_proyecto=proyecto_data[5],
                detalle_component=self.detalle_component
            )
            self.projects.controls.append(project)
            count = len(proyectos)
            self.items_left.value = f"{count} proyecto(s)"
        self.update()  # Update the interface to reflect the loaded projects

def create_info_box(text_color, background_color, icon=Icons.INFO, message=""):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, color=text_color, size=TEXTO_NORMAL),
                Text(
                    message,
                    color=text_color,
                    size=TEXTO_NORMAL,
                    weight=ft.FontWeight.W_500
                )
            ],
            spacing=ESPACIADO_PEQUENO
        ),
        bgcolor=background_color,
        padding=ESPACIADO_NORMAL,
        margin=ESPACIADO_NORMAL,
        border_radius=BORDE_RADIO,
        shadow=SOMBRA_NORMAL
    )


class Documento(ft.Column):
    def __init__(self, id, codigo, nombre, tipo, disciplina, status, observaciones, revision, documentos_app, documento_detalle, version_detalle):
        super().__init__()
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.disciplina = disciplina
        self.status = status
        self.observaciones = observaciones
        self.revision = revision
        self.documentos_app = documentos_app  # Referencia a DocumentosApp
        self.documento_detalle = documento_detalle  # Referencia a DocumentoDetalle
        self.version_detalle = version_detalle  # Referencia a VersionDetalle

        self.versions_container = ft.Column(controls=[], visible=False)  # Contenedor para las versiones

        self.display_document = ft.Container(
            content=ft.Text(
                value=self.mostrar_info(),
                color=COLOR_TEXTO,
                size=TEXTO_NORMAL
            ),
            on_click=self.select_clicked,
            padding=ESPACIADO_NORMAL,
            border_radius=BORDE_RADIO,
            bgcolor=COLOR_ITEM,
            width=300,
            shadow=SOMBRA_NORMAL,
            ink=True,
            on_hover=self.on_hover
        )
        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_document,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ADD,
                            tooltip="Nueva Versión",
                            icon_color=COLOR_BOTON,
                            icon_size=24,
                            on_click=self.open_version_modal
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            tooltip="Eliminar Documento",
                            icon_color=COLOR_ERROR,
                            icon_size=24,
                            on_click=self.delete_clicked
                        ),
                    ],
                ),
            ],
        )
        self.controls = [self.display_view, self.versions_container]  # Agregar el contenedor de versiones

    def mostrar_info(self):
        return f"{self.nombre} - {self.tipo}"

    def select_clicked(self, e):
        # Mostrar detalles del documento seleccionado
        self.documento_detalle.mostrar_detalles(
            self.id,  # id
            self.codigo,  # codigo
            self.nombre,  # nombre
            self.tipo,  # tipo
            self.disciplina,  # disciplina
            self.status,  # status
            self.observaciones,  # observaciones
            self.revision  # revision
        )
        
        # Limpiar detalles de las versiones
        self.version_detalle.details_column.controls.clear()
        self.version_detalle.initial_message.visible = True
        self.version_detalle.details_column.controls.append(
            self.version_detalle.initial_message
        )
        self.version_detalle.update()
        
        # Obtener las versiones del documento seleccionado
        versiones = obtener_versiones(documento_id=self.id)
        self.mostrar_versiones(versiones)  # Mostrar versiones en el contenedor

    def mostrar_versiones(self, versiones):
        self.versions_container.controls.clear()  # Limpiar versiones anteriores
        for version_data in versiones:
            version = Version(
                id=version_data[0],
                nombre_version=version_data[2],
                status=version_data[3],
                archivo=version_data[4],
                version_detalle=self.version_detalle,  # Pasar la referencia a VersionDetalle
                documento_id=version_data[1]  # Pasar el documento_id de la versión
            )
            self.versions_container.controls.append(version)
        self.versions_container.visible = not self.versions_container.visible  # Alternar visibilidad
        self.update()  # Actualizar la interfaz

    def on_hover(self, e):
        self.display_document.bgcolor = COLOR_ITEM_HOVER if e.data == "true" else COLOR_ITEM
        self.display_document.update()

    def open_version_modal(self, e):
        # Crear campos para la nueva versión
        nombre_version_field = ft.Dropdown(
            label="Nombre de la versión",
            options=[
                ft.dropdown.Option("Versión A"),
                ft.dropdown.Option("Versión B"),
                ft.dropdown.Option("Versión 0"),
            ],
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )
        
        status_field = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option("Aprobado"),
                ft.dropdown.Option("Aprobado con comentarios"),
                ft.dropdown.Option("Pendiente"),
            ],
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )

        warning_signal = ft.Container(
            content=ft.Column(
                controls=[
                    create_info_box(
                        text_color=COLOR_TEXTO_ERROR,
                        background_color=COLOR_ERROR,
                        message="Por favor, complete todos los campos obligatorios."
                    ),
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=350,
            visible=False
        )

        accept_button = ft.TextButton(
            "Aceptar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: self.submit_version_data(
                nombre_version_field.value,
                status_field.value,
                warning_signal,
                dlg
            )
        )
        cancel_button = ft.TextButton(
            "Cancelar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_ERROR
            ),
            on_click=lambda e: dlg.close(self.page)
        )

        dlg = ReusableModal(
            title="Nueva Versión",
            content="",
            actions=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                warning_signal,
                                nombre_version_field,
                                status_field
                            ],
                            spacing=ESPACIADO_NORMAL,
                            alignment=ft.MainAxisAlignment.CENTER,
                            width=350
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(height=ESPACIADO_GRANDE),
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def submit_version_data(self, nombre_version, status, warning_signal, dlg):
        if not nombre_version or not status:
            warning_signal.visible = True
            self.page.update()
        else:
            warning_signal.visible = False
            crear_version(
                documento_id=self.id,
                nombre_version=nombre_version,
                status=status,
                archivo=""  # Por ahora dejamos el archivo vacío
            )
            dlg.close(self.page)
            # Recargar las versiones
            versiones = obtener_versiones(documento_id=self.id)
            self.mostrar_versiones(versiones)

    def delete_clicked(self, e):
        # Crear el modal de confirmación
        accept_button = ft.TextButton(
            "Eliminar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_ERROR
            ),
            on_click=lambda e: self.confirmar_eliminacion(dlg)
        )
        cancel_button = ft.TextButton(
            "Cancelar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: dlg.close(self.page)
        )

        dlg = ReusableModal(
            title="Confirmar Eliminación",
            content=f"¿Está seguro que desea eliminar el documento '{self.nombre}'? Esta acción también eliminará todas sus versiones y fechas asociadas.",
            actions=[
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def confirmar_eliminacion(self, dlg):
        # Eliminar el documento de la base de datos
        eliminar_documento(self.id)
        
        # Cerrar el modal
        dlg.close(self.page)
        
        # Limpiar detalles del documento
        self.documento_detalle.details_column.controls.clear()
        self.documento_detalle.initial_message.visible = True
        self.documento_detalle.details_column.controls.append(
            self.documento_detalle.initial_message
        )
        self.documento_detalle.update()
        
        # Limpiar detalles de la versión
        self.version_detalle.details_column.controls.clear()
        self.version_detalle.initial_message.visible = True
        self.version_detalle.details_column.controls.append(
            self.version_detalle.initial_message
        )
        self.version_detalle.update()
        
        # Recargar la lista de documentos
        self.documentos_app.mostrar_documentos(self.documentos_app.current_proyecto_id)

class DocumentosApp(ft.Column):
    def __init__(self, documento_detalle, version_detalle):
        super().__init__()
        self.documents = ft.ListView(
            spacing=ESPACIADO_NORMAL,
            width=400,
            height=300,
        )
        self.items_left = ft.Text(
            "0 Documentos",
            color=COLOR_TEXTO_SECUNDARIO,
            size=TEXTO_NORMAL
        )
        self.width = 400
        self.controls = [
            ft.Row(
                [ft.Text(
                    value="Documentos",
                    color=COLOR_TEXTO,
                    size=TEXTO_GRANDE,
                    weight=ft.FontWeight.BOLD
                )],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.items_left,
                    ft.FloatingActionButton(
                        text="Nuevo",
                        height=20,
                        bgcolor=COLOR_BOTON,
                        foreground_color=COLOR_TEXTO_BOTON,
                        on_click=self.open_document_modal,
                        tooltip="Crear nuevo documento"
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            self.documents,
        ]
        self.documento_detalle = documento_detalle
        self.version_detalle = version_detalle
        self.current_proyecto_id = None

    def set_proyecto_id(self, proyecto_id):
        self.current_proyecto_id = proyecto_id

    def open_document_modal(self, e):
        if not self.current_proyecto_id:
            dlg = ReusableModal(
                title="Error",
                content="Debe seleccionar un proyecto primero",
                actions=[ft.TextButton("Aceptar", on_click=lambda e: dlg.close(self.page))],
                modal=True
            )
            dlg.open(self.page)
            return

        # Crear campos para el nuevo documento
        codigo_field = ft.TextField(
            label="Código",
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )
        nombre_field = ft.TextField(
            label="Nombre",
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )
        tipo_field = ft.Dropdown(
            label="Tipo",
            options=[
                ft.dropdown.Option("Documento"),
                ft.dropdown.Option("Plano"),
            ],
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )
        disciplina_field = ft.TextField(
            label="Disciplina",
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )
        status_field = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option("Aprobado"),
                ft.dropdown.Option("Aprobado con comentarios"),
                ft.dropdown.Option("Pendiente"),
            ],
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )
        revision_field = ft.Dropdown(
            label="Revisión",
            options=[
                ft.dropdown.Option("Rev A"),
                ft.dropdown.Option("Rev B"),
                ft.dropdown.Option("Rev 0"),
            ],
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )
        observaciones_field = ft.TextField(
            label="Observaciones",
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350,
            multiline=True,
            min_lines=3
        )

        warning_signal = ft.Container(
            content=ft.Column(
                controls=[
                    create_info_box(
                        text_color=COLOR_TEXTO_ERROR,
                        background_color=COLOR_ERROR,
                        message="Por favor, complete todos los campos obligatorios."
                    ),
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=350,
            visible=False
        )

        accept_button = ft.TextButton(
            "Aceptar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: self.submit_document_data(
                codigo_field.value,
                nombre_field.value,
                tipo_field.value,
                disciplina_field.value,
                status_field.value,
                observaciones_field.value,
                revision_field.value,
                warning_signal,
                dlg
            )
        )
        cancel_button = ft.TextButton(
            "Cancelar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_ERROR
            ),
            on_click=lambda e: dlg.close(self.page)
        )

        dlg = ReusableModal(
            title="Nuevo Documento",
            content="",
            actions=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                warning_signal,
                                codigo_field,
                                nombre_field,
                                tipo_field,
                                disciplina_field,
                                status_field,
                                revision_field,
                                observaciones_field
                            ],
                            spacing=ESPACIADO_NORMAL,
                            alignment=ft.MainAxisAlignment.CENTER,
                            width=350,
                            scroll=ft.ScrollMode.AUTO
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(height=ESPACIADO_GRANDE),
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def submit_document_data(self, codigo, nombre, tipo, disciplina, status, observaciones, revision, warning_signal, dlg):
        if not codigo or not nombre or not tipo or not disciplina or not status or not revision:
            warning_signal.visible = True
            self.page.update()
        else:
            warning_signal.visible = False
            crear_documento(
                codigo=codigo,
                nombre=nombre,
                tipo=tipo,
                disciplina=disciplina,
                status=status,
                observaciones=observaciones,
                proyecto_id=self.current_proyecto_id,
                revision=revision
            )
            dlg.close(self.page)
            self.mostrar_documentos(self.current_proyecto_id)  # Recargar la lista de documentos

    def mostrar_documentos(self, proyecto_id):
        self.current_proyecto_id = proyecto_id
        documentos = obtener_documentos(proyecto_id=proyecto_id)
        self.documents.controls.clear()
        
        for doc_data in documentos:
            # Los índices coinciden con la estructura de la tabla Documentos:
            # 0: id
            # 1: proyecto_id
            # 2: codigo
            # 3: nombre
            # 4: tipo
            # 5: disciplina
            # 6: status
            # 7: revision
            # 8: observaciones
            documento = Documento(
                id=doc_data[0],
                codigo=doc_data[2],
                nombre=doc_data[3],
                tipo=doc_data[4],
                disciplina=doc_data[5],
                status=doc_data[6],
                observaciones=doc_data[8],
                revision=doc_data[7],
                documentos_app=self,
                documento_detalle=self.documento_detalle,
                version_detalle=self.version_detalle
            )
            self.documents.controls.append(documento)
        
        self.items_left.value = f"{len(documentos)} documentos"
        self.update()

class Version(ft.Column):
    def __init__(self, id, nombre_version, status, archivo, version_detalle, documento_id):
        super().__init__()
        self.id = id
        self.nombre_version = nombre_version
        self.status = status
        self.archivo = archivo
        self.version_detalle = version_detalle  # Referencia a VersionDetalle
        self.documento_id = documento_id  # Guardar el ID del documento

        self.display_version = ft.Container(
            content=ft.Text(
                value=self.mostrar_info(),
                color=COLOR_TEXTO,
                size=TEXTO_NORMAL
            ),
            on_click=self.select_clicked,  # Agregar evento de clic
            padding=ESPACIADO_NORMAL,
            border_radius=BORDE_RADIO,
            bgcolor=COLOR_VERSION,
            width=300,
            shadow=SOMBRA_NORMAL,
            ink=True,
            on_hover=self.on_hover
        )
        self.controls = [self.display_version]

    def mostrar_info(self):
        return f"{self.nombre_version} - {self.status}"

    def select_clicked(self, e):
        # Establecer el documento_id en VersionDetalle antes de mostrar los detalles
        self.version_detalle.current_document_id = self.documento_id
        # Mostrar detalles de la versión seleccionada
        self.version_detalle.mostrar_detalles(self.id, self.nombre_version, self.status, self.archivo)

    def on_hover(self, e):
        self.display_version.bgcolor = COLOR_VERSION_HOVER if e.data == "true" else COLOR_VERSION
        self.display_version.update()


class ProyectoDetalle(ft.Container):
    def __init__(self,documentos_app):
        super().__init__()
        self.scroll = ft.ScrollMode.AUTO
        self.width = 400
        self.height = 300
        self.border = ft.border.all(1, COLOR_BORDE)
        self.border_radius = ft.border_radius.all(BORDE_RADIO_GRANDE)
        self.padding = ESPACIADO_NORMAL
        self.bgcolor = COLOR_FONDO
        
        # Título del componente
        self.title = ft.Text(
            "Detalles del Proyecto",
            size=TEXTO_GRANDE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXTO,
            text_align=ft.TextAlign.CENTER
        )
        
        self.documentos_app = documentos_app
        self.details_column = ft.Column(
            controls=[],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=ESPACIADO_NORMAL,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        # Mensaje inicial
        self.initial_message = ft.Text(
            "Seleccione un proyecto para ver los detalles",
            size=TEXTO_GRANDE,
            color=COLOR_TEXTO_SECUNDARIO,
            text_align=ft.TextAlign.CENTER
        )
        self.details_column.controls.append(self.initial_message)

        # Botón de editar
        self.edit_button = ft.TextButton(
            "Editar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON,
            ),
            on_click=self.edit_clicked,
            tooltip="Editar proyecto"
        )
        
        self.current_project = {}
        self.proyecto_app = None
        
        # Contenedor principal que incluye título y detalles
        self.main_column = ft.Column(
            controls=[
                self.title,
                ft.Divider(color=COLOR_BORDE),
                self.details_column
            ],
            spacing=ESPACIADO_NORMAL,
            expand=True
        )
        
        self.content = self.main_column

    def set_proyecto_app(self, proyecto_app):
        """Método para establecer la referencia a ProyectoApp."""
        self.proyecto_app = proyecto_app
    
    def mostrar_detalles(self, id_proyecto, nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto):
        self.details_column.controls.clear()  # Limpiar controles anteriores
        self.initial_message.visible = False
        self.current_project = {
            "id": id_proyecto,
            "nombre": nombre,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "cliente": cliente,
            "codigo_proyecto": codigo_proyecto
        }
        
        # Sección de detalles
        details_section = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Detalles", size=TEXTO_NORMAL, weight=ft.FontWeight.BOLD, color=COLOR_TEXTO),
                        self.edit_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Text(f"Nombre: {nombre}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ft.Text(f"Fecha de Inicio: {fecha_inicio}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ft.Text(f"Fecha de Fin: {fecha_fin}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ft.Text(f"Cliente: {cliente}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ft.Text(f"Código del Proyecto: {codigo_proyecto}", size=TEXTO_NORMAL, color=COLOR_TEXTO)
            ],
            spacing=ESPACIADO_NORMAL,
            scroll=ft.ScrollMode.AUTO
        )

        # Agregar sección a la columna principal
        self.details_column.controls.append(details_section)
        self.update()
    
    def edit_clicked(self, e):
        # Crear campos de texto para editar los detalles del proyecto
        name_field = ft.TextField(label="Nombre", value=self.current_project["nombre"])
        start_date_field = ft.TextField(label="Fecha de Inicio", value=self.current_project["fecha_inicio"],disabled=True)
        end_date_field = ft.TextField(label="Fecha de Fin", value=self.current_project["fecha_fin"],disabled=True)
        client_field = ft.TextField(label="Cliente", value=self.current_project["cliente"])
        project_code_field = ft.TextField(label="Código del Proyecto", value=self.current_project["codigo_proyecto"])

        start_date_button = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e:  CustomDatePicker(self.page, start_date_field).open()
        )
        end_date_button = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e:  CustomDatePicker(self.page, end_date_field).open()
        )

        warning_signal = ft.Container(
            content=ft.Column(
                controls=[
                    create_info_box(
                        text_color="black",
                        background_color="#f3464a",
                        message="Por favor, complete todos los campos."
                    ),
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=350,  # Limitar el ancho del contenedor
            visible=False  # Inicialmente oculto
        )
        # Botones para aceptar y cancelar
        accept_button = ft.TextButton(
            "Aceptar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: self.submit_edit(name_field.value, start_date_field.value, end_date_field.value, client_field.value, project_code_field.value,warning_signal,dlg))
        cancel_button = ft.TextButton(
            "Cancelar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_ERROR
            ),
            on_click=lambda e: dlg.close(self.page))

        # Crear el modal para editar el proyecto
        dlg = ReusableModal(
            title="Editar Proyecto",
            content="",
            actions=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                warning_signal,
                                name_field,
                                ft.Row(controls=[start_date_field,start_date_button],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Row(controls=[end_date_field,end_date_button],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                client_field, 
                                project_code_field]),],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    width=350
                    ),
                ft.Container(
                    height=20  ),
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                                    ] ,
            modal=True
        )
        dlg.open(self.page)

    def submit_edit(self, nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto,warning_signal,dlg):
        if not nombre or not fecha_inicio or not fecha_fin or not cliente or not codigo_proyecto:
            warning_signal.visible = True  # Mostrar el mensaje de advertencia
            self.page.update()
        else:
            warning_signal.visible = False  # Ocultar el mensaje de advertencia
            # Si todos los campos están completos, proceder con el envío de datos
            modificar_proyecto(self.current_project["id"], nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto)
            dlg.close(self.page)
            self.proyecto_app.search_projects(None)  # Llamar a search_projects con None como evento
            self.mostrar_detalles(self.current_project["id"], nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto)  # Actualizar los detalles
        
class DocumentoDetalle(ft.Container):
    def __init__(self):
        super().__init__()
        self.scroll = ft.ScrollMode.AUTO
        self.width = 400
        self.height = 300
        self.border = ft.border.all(1, COLOR_BORDE)
        self.border_radius = ft.border_radius.all(BORDE_RADIO_GRANDE)
        self.padding = ESPACIADO_NORMAL
        self.bgcolor = COLOR_FONDO
        
        # Título del componente
        self.title = ft.Text(
            "Detalles del Documento",
            size=TEXTO_GRANDE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXTO,
            text_align=ft.TextAlign.CENTER
        )
        
        # Crear una columna scrolleable para los detalles
        self.details_column = ft.Column(
            controls=[],
            spacing=ESPACIADO_NORMAL,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        # Mensaje inicial
        self.initial_message = ft.Text(
            "Seleccione un documento para ver los detalles",
            size=TEXTO_GRANDE,
            color=COLOR_TEXTO_SECUNDARIO,
            text_align=ft.TextAlign.CENTER
        )
        self.details_column.controls.append(self.initial_message)

        # Botón de editar
        self.edit_button = ft.TextButton(
            "Editar",
            on_click=self.edit_clicked,
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON,
            ),
            tooltip="Editar documento"
        )
        
        self.current_document = {}
        
        # Contenedor principal que incluye título y detalles
        self.main_column = ft.Column(
            controls=[
                self.title,
                ft.Divider(color=COLOR_BORDE),
                self.details_column
            ],
            spacing=ESPACIADO_NORMAL,
            expand=True
        )
        
        self.content = self.main_column

    def mostrar_detalles(self, id_documento, codigo, nombre, tipo, disciplina, status, observaciones, revision):
        self.details_column.controls.clear()
        self.initial_message.visible = False

        self.current_document = {
            "id": id_documento,
            "codigo": codigo,
            "nombre": nombre,
            "tipo": tipo,
            "disciplina": disciplina,
            "status": status,
            "observaciones": observaciones,
            "revision": revision
        }

        # Sección de detalles
        details_section = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Detalles", size=TEXTO_NORMAL, weight=ft.FontWeight.BOLD, color=COLOR_TEXTO),
                        self.edit_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Text(f"Código: {codigo}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ft.Text(f"Nombre: {nombre}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ft.Text(f"Tipo: {tipo}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ft.Text(f"Disciplina: {disciplina}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ft.Text(f"Estado: {status}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ft.Text(f"Revisión: {revision}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ft.Text(f"Observaciones: {observaciones}", size=TEXTO_NORMAL, color=COLOR_TEXTO)
            ],
            spacing=ESPACIADO_NORMAL,
            scroll=ft.ScrollMode.AUTO
        )

        # Agregar sección a la columna principal
        self.details_column.controls.append(details_section)
        self.update()
    
    def edit_clicked(self, e):
        # Crear campos de texto para editar los detalles del documento
        codigo_field = ft.TextField(label="Código", value=self.current_document["codigo"])
        nombre_field = ft.TextField(label="Nombre", value=self.current_document["nombre"])
        tipo_field = ft.Dropdown(
            label="Tipo de documento",
            value=self.current_document["tipo"],
            options=[
                ft.dropdown.Option("Documento"),
                ft.dropdown.Option("Plano"),
            ],
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )
        disciplina_field = ft.TextField(label="Disciplina", value=self.current_document["disciplina"])
        status_field = ft.Dropdown(
            label="Estado",
            value=self.current_document["status"],
            options=[
                ft.dropdown.Option("Aprobado"),
                ft.dropdown.Option("Aprobado con comentarios"),
                ft.dropdown.Option("Pendiente"),
            ],
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )
        revision_field = ft.Dropdown(
            label="Revisión",
            value=self.current_document["revision"],
            options=[
                ft.dropdown.Option("Rev A"),
                ft.dropdown.Option("Rev B"),
                ft.dropdown.Option("Rev 0"),
            ],
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )
        observaciones_field = ft.TextField(
            label="Observaciones",
            value=self.current_document["observaciones"],
            multiline=True,
            min_lines=3,
            max_lines=5
        )

        warning_signal = ft.Container(
            content=ft.Column(
                controls=[
                    create_info_box(
                        text_color="black",
                        background_color="#f3464a",
                        message="Por favor, complete todos los campos obligatorios."
                    ),
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=350,
            visible=False
        )

        accept_button = ft.TextButton(
            "Aceptar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: self.submit_edit(
                codigo_field.value,
                nombre_field.value,
                tipo_field.value,
                disciplina_field.value,
                status_field.value,
                observaciones_field.value,
                revision_field.value,
                warning_signal,
                dlg
            )
        )
        cancel_button = ft.TextButton(
            "Cancelar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_ERROR
            ),
            on_click=lambda e: dlg.close(self.page)
        )

        dlg = ReusableModal(
            title="Editar Documento",
            content="",
            actions=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                warning_signal,
                                codigo_field,
                                nombre_field,
                                tipo_field,
                                disciplina_field,
                                status_field,
                                revision_field,
                                observaciones_field
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                            width=350
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(height=20),
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def submit_edit(self, codigo, nombre, tipo, disciplina, status, observaciones, revision, warning_signal, dlg):
        if not codigo or not nombre or not tipo or not disciplina or not status or not revision:
            warning_signal.visible = True
            self.page.update()
        else:
            warning_signal.visible = False
            modificar_documento(
                self.current_document["id"],
                codigo,
                nombre,
                tipo,
                disciplina,
                status,
                observaciones,
                revision
            )
            dlg.close(self.page)
            # Actualizar los detalles mostrados
            self.mostrar_detalles(
                self.current_document["id"],
                codigo,
                nombre,
                tipo,
                disciplina,
                status,
                observaciones,
                revision
            )
            # Recargar la lista de documentos
            for view in self.page.views:
                for control in view.controls:
                    if isinstance(control, ft.Container):
                        for child in control.content.controls:
                            if isinstance(child, ft.Column):
                                for grandchild in child.controls:
                                    if isinstance(grandchild, DocumentosApp):
                                        # Actualizar el documento en la lista
                                        for doc in grandchild.documents.controls:
                                            if isinstance(doc, Documento) and doc.id == self.current_document["id"]:
                                                doc.codigo = codigo
                                                doc.nombre = nombre
                                                doc.tipo = tipo
                                                doc.disciplina = disciplina
                                                doc.status = status
                                                doc.observaciones = observaciones
                                                doc.revision = revision
                                                doc.display_document.value = doc.mostrar_info()
                                                doc.display_document.update()
                                                break
                                        break

class VersionDetalle(ft.Container):
    def __init__(self):
        super().__init__()
        self.scroll = ft.ScrollMode.AUTO
        self.width = 400
        self.height = 300
        self.border = ft.border.all(1, COLOR_BORDE)
        self.border_radius = ft.border_radius.all(BORDE_RADIO_GRANDE)
        self.padding = ESPACIADO_NORMAL
        self.bgcolor = COLOR_FONDO
        
        # Título del componente
        self.title = ft.Text(
            "Detalles de la Versión",
            size=TEXTO_GRANDE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXTO,
            text_align=ft.TextAlign.CENTER
        )
        
        # Crear una columna scrolleable para los detalles
        self.details_column = ft.Column(
            controls=[],
            spacing=ESPACIADO_NORMAL,
            scroll=ft.ScrollMode.AUTO,
            height=280,
            expand=True
        )

        # Mensaje inicial
        self.initial_message = ft.Text(
            "Seleccione una versión para ver los detalles",
            size=TEXTO_GRANDE,
            color=COLOR_TEXTO_SECUNDARIO,
            text_align=ft.TextAlign.CENTER
        )
        self.details_column.controls.append(self.initial_message)

        # Contenedores para cada sección
        self.info_section = ft.Container(visible=False)
        self.dates_section = ft.Container(visible=False)
        self.file_section = ft.Container(visible=False)
        
        # Contenedor principal que incluye título y detalles
        self.main_column = ft.Column(
            controls=[
                self.title,
                ft.Divider(color=COLOR_BORDE),
                self.details_column
            ],
            spacing=ESPACIADO_NORMAL,
            expand=True
        )
        
        self.content = self.main_column

    def cargar_fechas(self, version_id):
        # Aquí cargaremos las fechas de la versión desde la base de datos
        fechas = obtener_fechas(version_id)
        fechas_list = self.dates_section.content.controls[1]
        fechas_list.controls.clear()
        
        for fecha in fechas:
            fecha_container = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(
                            value=fecha[2],  # fecha[2] es el nombre_fecha
                            size=TEXTO_NORMAL,
                            color=COLOR_TEXTO,
                            width=100
                        ),
                        ft.TextField(
                            value=fecha[3],  # fecha[3] es la fecha
                            disabled=True,
                            border_color=COLOR_BORDE,
                            text_size=TEXTO_NORMAL,
                            width=120
                        ),
                        ft.IconButton(
                            icon=ft.icons.CALENDAR_MONTH,
                            icon_color=COLOR_BOTON,
                            on_click=lambda e, f=fecha: self.abrir_calendario_fecha(e, f[0], f[2], f[3])
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_color=COLOR_ERROR,
                            on_click=lambda e, f=fecha: self.eliminar_fecha(e, f[0])
                        )
                    ],
                    spacing=ESPACIADO_NORMAL
                )
            )
            fechas_list.controls.append(fecha_container)
        
        self.update()

    def abrir_calendario_fecha(self, e, fecha_id, nombre_fecha, fecha_actual):
        # Crear campo para la fecha
        fecha_field = ft.TextField(
            value=fecha_actual,
            disabled=True,
            border_color=COLOR_BORDE,
            text_size=TEXTO_NORMAL
        )
        
        warning_signal = ft.Container(
            content=ft.Column(
                controls=[
                    create_info_box(
                        text_color=COLOR_TEXTO_ERROR,
                        background_color=COLOR_ERROR,
                        message="Por favor, seleccione una fecha."
                    ),
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=350,
            visible=False
        )

        accept_button = ft.TextButton(
            "Aceptar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: self.submit_fecha_modificada(
                fecha_id,
                nombre_fecha,
                fecha_field.value,
                warning_signal,
                dlg
            )
        )
        cancel_button = ft.TextButton(
            "Cancelar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_ERROR
            ),
            on_click=lambda e: dlg.close(self.page)
        )

        dlg = ReusableModal(
            title=f"Modificar Fecha: {nombre_fecha}",
            content="",
            actions=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                warning_signal,
                                ft.Row(
                                    controls=[
                                        fecha_field,
                                        ft.IconButton(
                                            icon=ft.icons.CALENDAR_MONTH,
                                            icon_color=COLOR_BOTON,
                                            on_click=lambda e: CustomDatePicker(self.page, fecha_field).open()
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ],
                            spacing=ESPACIADO_NORMAL,
                            alignment=ft.MainAxisAlignment.CENTER,
                            width=350
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(height=ESPACIADO_GRANDE),
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def submit_fecha_modificada(self, fecha_id, nombre_fecha, nueva_fecha, warning_signal, dlg):
        if not nueva_fecha:
            warning_signal.visible = True
            self.page.update()
        else:
            warning_signal.visible = False
            # Actualizar la fecha en la base de datos
            modificar_fecha(
                fecha_id=fecha_id,
                version_id=self.current_version_id,
                nombre_fecha=nombre_fecha,
                fecha=nueva_fecha
            )
            dlg.close(self.page)
            # Recargar las fechas para mostrar los cambios
            self.cargar_fechas(self.current_version_id)

    def eliminar_fecha(self, e, fecha_id):
        # Crear el modal de confirmación
        accept_button = ft.TextButton(
            "Eliminar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_ERROR
            ),
            on_click=lambda e: self.confirmar_eliminacion(dlg, fecha_id)
        )
        cancel_button = ft.TextButton(
            "Cancelar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: dlg.close(self.page)
        )

        dlg = ReusableModal(
            title="Confirmar Eliminación",
            content="¿Está seguro que desea eliminar esta fecha?",
            actions=[
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def confirmar_eliminacion(self, dlg, fecha_id):
        # Eliminar la fecha de la base de datos
        eliminar_fecha(fecha_id)
        # Cerrar el modal
        dlg.close(self.page)
        # Recargar las fechas para actualizar la vista
        self.cargar_fechas(self.current_version_id)

    def mostrar_detalles(self, id_version, nombre_version, status, archivo):
        self.details_column.controls.clear()
        self.initial_message.visible = False
        self.current_version_id = id_version
        self.current_version_name = nombre_version
        self.current_version_status = status
        self.current_document_id = self.current_document_id if hasattr(self, 'current_document_id') else None
        
        # Sección 1: Información básica
        self.info_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Información Básica", size=TEXTO_NORMAL, weight=ft.FontWeight.BOLD, color=COLOR_TEXTO),
                            ft.TextButton(
                                "Editar",
                                style=ft.ButtonStyle(
                                    color=COLOR_TEXTO_BOTON,
                                    bgcolor=COLOR_BOTON,
                                ),
                                on_click=self.edit_version_clicked,
                                tooltip="Editar versión"
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Text(f"Nombre: {nombre_version}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                    ft.Text(f"Estado: {status}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ],
                spacing=ESPACIADO_NORMAL
            )
        )

        # Sección 2: Fechas
        self.dates_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Fechas", size=TEXTO_NORMAL, weight=ft.FontWeight.BOLD, color=COLOR_TEXTO),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                tooltip="Agregar fecha",
                                icon_color=COLOR_BOTON,
                                on_click=lambda e: self.agregar_fecha(e, id_version)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.ListView(
                        controls=[],
                        height=100,
                        spacing=ESPACIADO_PEQUENO
                    )
                ],
                spacing=ESPACIADO_NORMAL
            )
        )

        # Sección 3: Archivo
        archivo_controls = []
        if not archivo:
            archivo_controls.extend([
                ft.Text("No hay archivo adjunto", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ft.ElevatedButton(
                    text="Subir PDF",
                    icon=ft.icons.UPLOAD_FILE,
                    style=ft.ButtonStyle(
                        color=COLOR_TEXTO_BOTON,
                        bgcolor=COLOR_BOTON
                    ),
                    on_click=lambda e: self.subir_pdf(e, id_version)
                )
            ])
        else:
            nombre_archivo = archivo.split("/")[-1] if "/" in archivo else archivo.split("\\")[-1] if "\\" in archivo else archivo
            archivo_controls.extend([
                ft.Text(f"Archivo: {nombre_archivo}", size=TEXTO_NORMAL, color=COLOR_TEXTO),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text="Cambiar PDF",
                            icon=ft.icons.UPLOAD_FILE,
                            style=ft.ButtonStyle(
                                color=COLOR_TEXTO_BOTON,
                                bgcolor=COLOR_BOTON
                            ),
                            on_click=lambda e: self.subir_pdf(e, id_version)
                        ),
                        ft.ElevatedButton(
                            text="Descargar PDF",
                            icon=ft.icons.DOWNLOAD,
                            style=ft.ButtonStyle(
                                color=COLOR_TEXTO_BOTON,
                                bgcolor=COLOR_BOTON
                            ),
                            on_click=lambda e: self.descargar_pdf(e, archivo)
                        )
                    ],
                    spacing=ESPACIADO_NORMAL
                )
            ])

        self.file_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Archivo", size=TEXTO_NORMAL, weight=ft.FontWeight.BOLD, color=COLOR_TEXTO),
                    *archivo_controls
                ],
                spacing=ESPACIADO_NORMAL
            )
        )

        # Agregar todas las secciones a la columna principal
        self.details_column.controls.extend([
            self.info_section,
            ft.Divider(color=COLOR_BORDE),
            self.dates_section,
            ft.Divider(color=COLOR_BORDE),
            self.file_section
        ])

        # Cargar las fechas de la versión
        self.cargar_fechas(id_version)

        # Actualizar la interfaz
        self.update()

    def subir_pdf(self, e, version_id):
        # Abrir el explorador de archivos para seleccionar un PDF
        file_picker = ft.FilePicker(
            on_result=lambda e: self.procesar_pdf_seleccionado(e, version_id)
        )
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(
            allowed_extensions=['pdf'],
            allow_multiple=False
        )

    def procesar_pdf_seleccionado(self, e, version_id):
        if e.files:
            archivo_seleccionado = e.files[0]
            # Almacenar el PDF usando la llave maestra del client_storage
            llave_maestra = self.page.client_storage.get("llave_maestra")
            nuevo_nombre = almacenar_pdf(archivo_seleccionado.path, llave_maestra)
            
            # Actualizar la versión en la base de datos con el nuevo nombre del archivo
            modificar_version(
                version_id=version_id,
                documento_id=self.current_document_id,
                nombre_version=self.current_version_name,
                status=self.current_version_status,
                archivo=nuevo_nombre
            )
            
            # Actualizar la vista
            self.mostrar_detalles(
                version_id,
                self.current_version_name,
                self.current_version_status,
                nuevo_nombre
            )

    def descargar_pdf(self, e, archivo):
        # Obtener la llave maestra y la ruta de descarga del client_storage
        llave_maestra = self.page.client_storage.get("llave_maestra")
        ruta_descarga = self.page.client_storage.get("download_path")
        
        # Descargar el PDF usando la llave maestra
        ruta_destino = descargar_pdf(archivo, llave_maestra, ruta_descarga)
        
        # Mostrar mensaje de éxito
        dlg = ReusableModal(
            title="Descarga Exitosa",
            content=f"El archivo se ha descargado en: {ruta_destino}",
            actions=[
                ft.TextButton(
                    "Aceptar",
                    style=ft.ButtonStyle(
                        color=COLOR_TEXTO_BOTON,
                        bgcolor=COLOR_BOTON
                    ),
                    on_click=lambda e: dlg.close(self.page)
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def edit_version_clicked(self, e):
        # Crear campos para editar la versión
        nombre_version_field = ft.Dropdown(
            label="Nombre de la versión",
            value=self.current_version_name,
            options=[
                ft.dropdown.Option("Versión A"),
                ft.dropdown.Option("Versión B"),
                ft.dropdown.Option("Versión 0"),
            ],
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )
        
        status_field = ft.Dropdown(
            label="Estado",
            value=self.current_version_status,
            options=[
                ft.dropdown.Option("Aprobado"),
                ft.dropdown.Option("Aprobado con comentarios"),
                ft.dropdown.Option("Pendiente"),
            ],
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )

        warning_signal = ft.Container(
            content=ft.Column(
                controls=[
                    create_info_box(
                        text_color=COLOR_TEXTO_ERROR,
                        background_color=COLOR_ERROR,
                        message="Por favor, complete todos los campos obligatorios."
                    ),
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=350,
            visible=False
        )

        accept_button = ft.TextButton(
            "Aceptar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: self.submit_version_edit(
                nombre_version_field.value,
                status_field.value,
                warning_signal,
                dlg
            )
        )
        cancel_button = ft.TextButton(
            "Cancelar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_ERROR
            ),
            on_click=lambda e: dlg.close(self.page)
        )

        dlg = ReusableModal(
            title="Editar Versión",
            content="",
            actions=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                warning_signal,
                                nombre_version_field,
                                status_field
                            ],
                            spacing=ESPACIADO_NORMAL,
                            alignment=ft.MainAxisAlignment.CENTER,
                            width=350
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(height=ESPACIADO_GRANDE),
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def submit_version_edit(self, nombre_version, status, warning_signal, dlg):
        if not nombre_version or not status:
            warning_signal.visible = True
            self.page.update()
        else:
            warning_signal.visible = False
            # Actualizar la versión en la base de datos
            modificar_version(
                version_id=self.current_version_id,
                documento_id=self.current_document_id,
                nombre_version=nombre_version,
                status=status,
                archivo=self.current_version_archivo if hasattr(self, 'current_version_archivo') else ""
            )
            dlg.close(self.page)
            # Actualizar la vista con los nuevos datos
            self.mostrar_detalles(
                self.current_version_id,
                nombre_version,
                status,
                self.current_version_archivo if hasattr(self, 'current_version_archivo') else ""
            )

    def agregar_fecha(self, e, version_id):
        # Crear campos para la nueva fecha
        nombre_fecha_field = ft.TextField(
            label="Nombre de la fecha",
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            width=350
        )
        
        fecha_field = ft.TextField(
            label="Fecha",
            disabled=True,
            border_color=COLOR_BORDE,
            text_size=TEXTO_NORMAL,
            width=350
        )
        
        fecha_button = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            icon_color=COLOR_BOTON,
            on_click=lambda e: CustomDatePicker(self.page, fecha_field).open()
        )

        warning_signal = ft.Container(
            content=ft.Column(
                controls=[
                    create_info_box(
                        text_color=COLOR_TEXTO_ERROR,
                        background_color=COLOR_ERROR,
                        message="Por favor, complete todos los campos obligatorios."
                    ),
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=350,
            visible=False
        )

        accept_button = ft.TextButton(
            "Aceptar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: self.submit_nueva_fecha(
                nombre_fecha_field.value,
                fecha_field.value,
                warning_signal,
                dlg
            )
        )
        cancel_button = ft.TextButton(
            "Cancelar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_ERROR
            ),
            on_click=lambda e: dlg.close(self.page)
        )

        dlg = ReusableModal(
            title="Nueva Fecha",
            content="",
            actions=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                warning_signal,
                                nombre_fecha_field,
                                ft.Row(
                                    controls=[fecha_field, fecha_button],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ],
                            spacing=ESPACIADO_NORMAL,
                            alignment=ft.MainAxisAlignment.CENTER,
                            width=400
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(height=ESPACIADO_GRANDE),
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def submit_nueva_fecha(self, nombre_fecha, fecha, warning_signal, dlg):
        if not nombre_fecha or not fecha:
            warning_signal.visible = True
            self.page.update()
        else:
            warning_signal.visible = False
            # Crear la nueva fecha en la base de datos
            crear_fecha(
                version_id=self.current_version_id,
                nombre_fecha=nombre_fecha,
                fecha=fecha
            )
            dlg.close(self.page)
            # Recargar las fechas para mostrar los cambios
            self.cargar_fechas(self.current_version_id)

class CustomDatePicker:
    def __init__(self, page, date_text_field):
        self.page = page
        self.date_text_field = date_text_field

    def open(self):
        date_picker = ft.DatePicker(
            on_change=self.create_date_change_handler()
        )
        self.page.open(date_picker)

    def create_date_change_handler(self):
        def handler(e):
            self.date_text_field.value = e.control.value.strftime('%Y-%m-%d')
            self.page.update()
        return handler   

class BienvenidaView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.route = '/'
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.spacing = ESPACIADO_NORMAL
        
        # Título y subtítulo
        self.title = Text(
            "Gestor de Documentos",
            size=TEXTO_GRANDE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_PRIMARIO
        )
        self.subtitle = Text(
            "Lisduer Parra",
            size=TEXTO_NORMAL,
            color=COLOR_TEXTO_SECUNDARIO
        )
        
        # Botón de registro/login
        self.action_button = ElevatedButton(
            text='Registrarse' if not verificar_usuarios_existentes() else 'Iniciar Sesion',
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda _: page.go('/Registro' if not verificar_usuarios_existentes() else '/Login')
        )
        
        # AppBar
        self.appbar = AppBar(
            title=Text('Bienvenido', color=COLOR_TEXTO_BOTON),
            bgcolor=COLOR_PRIMARIO
        )
        
        # Controles de la vista
        self.controls = [
            self.appbar,
            self.title,
            self.subtitle,
            self.action_button
        ]

class RegistroView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.route = '/Registro'
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.spacing = ESPACIADO_NORMAL
        
        # Título
        self.titulo = Text(
            "Registro de Usuario",
            size=TEXTO_GRANDE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXTO
        )
        
        # Campos de entrada
        self.username_input = TextField(
            label="Nombre de Usuario",
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        
        self.password_input = TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        
        # Botón de registro
        self.registro_button = ElevatedButton(
            text="Registrar",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: self.registro_pressed(e, page)
        )
        
        # Mensaje informativo
        self.info_box = ft.Container(
            content=ft.Column(
                controls=[
                    create_info_box(
                        text_color=COLOR_TEXTO,
                        background_color=COLOR_INFO,
                        message="Dado que no hay ningún usuario registrado, se registrará un administrador."
                    ),
                ],
                alignment=CrossAxisAlignment.CENTER,
            ),
            width=600,
        )
        
        # AppBar
        self.appbar = AppBar(
            title=Text('Registro', color=COLOR_TEXTO_BOTON),
            bgcolor=COLOR_PRIMARIO
        )
        
        # Contenedor principal
        self.main_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.username_input,
                    self.password_input,
                    self.registro_button
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=ESPACIADO_NORMAL
            ),
            width=400,
        )
        
        # Controles de la vista
        self.controls = [
            self.appbar,
            self.titulo,
            self.info_box,
            self.main_container
        ]
    
    def registrar_inicio(self, user, password):
        """Registra un nuevo usuario en el sistema."""
        password_hashed = hash_text(password)
        crear_usuario(user, password_hashed, True)
        llave_maestra = generar_clave()
        llave_encriptada = xor_encrypt_decrypt(llave_maestra, password)
        registrar_llave(llave_encriptada, password_hashed)
    
    def registro_pressed(self, e, page):
        """Maneja el proceso de registro de usuario."""
        username = self.username_input.value
        password = self.password_input.value
        
        if not username or not password:
            self.info_box.content.controls[0] = create_info_box(
                text_color=COLOR_TEXTO_ERROR,
                background_color=COLOR_ERROR,
                message="Por favor, complete todos los campos."
            )
            self.info_box.update()
            return

        try:
            self.registrar_inicio(username, password)
            self.info_box.content.controls[0] = create_info_box(
                text_color=COLOR_TEXTO,
                background_color=COLOR_INFO,
                message="Registro exitoso. Redirigiendo..."
            )
            self.info_box.update()
            page.update()
            page.go('/')
        except Exception as e:
            self.info_box.content.controls[0] = create_info_box(
                text_color=COLOR_TEXTO_ERROR,
                background_color=COLOR_ERROR,
                message=f"Error al registrar: {str(e)}"
            )
            self.info_box.update()

class LoginView(ft.View):
    def __init__(self, page: ft.Page, session):
        super().__init__()
        self.route = '/Login'
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.spacing = ESPACIADO_NORMAL
        
        # Título
        self.titulo = Text(
            "Iniciar Sesion",
            size=TEXTO_GRANDE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXTO
        )
        
        # Campos de entrada
        self.username_input = TextField(
            label="Nombre de Usuario",
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        
        self.password_input = TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        
        # Botón de inicio de sesión
        self.login_button = ElevatedButton(
            text="Iniciar sesion",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            ),
            on_click=lambda e: self.login_pressed(e, page, session)
        )
        
        # Mensaje de error
        self.warning_signal = ft.Container(
            content=ft.Column(
                controls=[
                    create_info_box(
                        text_color=COLOR_TEXTO_ERROR,
                        background_color=COLOR_ERROR,
                        message="Usuario o Contraseña incorrecta."
                    ),
                ],
                alignment=CrossAxisAlignment.CENTER,
            ),
            width=600,
            visible=False
        )
        
        # AppBar
        self.appbar = AppBar(
            title=Text('Login', color=COLOR_TEXTO_BOTON),
            bgcolor=COLOR_PRIMARIO
        )
        
        # Contenedor principal
        self.main_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.username_input,
                    self.password_input,
                    self.login_button
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=ESPACIADO_NORMAL
            ),
            width=400,
        )
        
        # Controles de la vista
        self.controls = [
            self.appbar,
            self.titulo,
            self.warning_signal,
            self.main_container
        ]
    
    def login_pressed(self, e, page, session):
        """Maneja el proceso de inicio de sesión."""
        username = self.username_input.value
        password = self.password_input.value
        
        if not username or not password:
            self.warning_signal.visible = True
            self.warning_signal.content.controls[0] = create_info_box(
                text_color=COLOR_TEXTO_ERROR,
                background_color=COLOR_ERROR,
                message="Por favor, complete todos los campos."
            )
            self.warning_signal.update()
            return
        
        try:
            if login_user(username, password):
                # Obtener la llave encriptada usando el hash de la contraseña
                password_hash = hash_text(password)
                llave_encriptada = buscar_llave(password_hash)
                
                if llave_encriptada:
                    # Desencriptar la llave maestra usando la contraseña
                    llave_maestra = xor_encrypt_decrypt(llave_encriptada, password)
                    
                    # Guardar todo en el client_storage
                    page.client_storage.set("llave_maestra", llave_maestra)
                    session["username"] = username
                    session["password"] = password
                    session["isadmin"] = isadmin(username)
                    
                    self.warning_signal.visible = False
                    self.warning_signal.content.controls[0] = create_info_box(
                        text_color=COLOR_TEXTO,
                        background_color=COLOR_INFO,
                        message="Inicio de sesión exitoso. Redirigiendo..."
                    )
                    self.warning_signal.visible = True
                    self.warning_signal.update()
                    page.update()
                    page.go('/Home')
                else:
                    self.warning_signal.visible = True
                    self.warning_signal.content.controls[0] = create_info_box(
                        text_color=COLOR_TEXTO_ERROR,
                        background_color=COLOR_ERROR,
                        message="Error: No se encontró la llave maestra."
                    )
                    self.warning_signal.update()
            else:
                self.warning_signal.visible = True
                self.warning_signal.content.controls[0] = create_info_box(
                    text_color=COLOR_TEXTO_ERROR,
                    background_color=COLOR_ERROR,
                    message="Usuario o Contraseña incorrecta."
                )
                self.warning_signal.update()
        except Exception as e:
            self.warning_signal.visible = True
            self.warning_signal.content.controls[0] = create_info_box(
                text_color=COLOR_TEXTO_ERROR,
                background_color=COLOR_ERROR,
                message=f"Error al iniciar sesión: {str(e)}"
            )
            self.warning_signal.update()

class HomeView(ft.View):
    def __init__(self, page: ft.Page, session):
        super().__init__()
        self.route = '/Home'
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.spacing = ESPACIADO_NORMAL
        
        # Columna 1: Proyectos
        documento_detalle = DocumentoDetalle()
        version_detalle = VersionDetalle()
        version_detalle.page = page  # Asegurarnos de que tenga acceso a page
        documentos_app = DocumentosApp(documento_detalle, version_detalle)
        documentos_app.page = page  # Asegurarnos de que DocumentosApp tenga acceso a page
        documento_detalle.page = page  # Asegurarnos de que DocumentoDetalle tenga acceso a page
        Detalle_Proyecto = ProyectoDetalle(documentos_app)
        Detalle_Proyecto.page = page  # Asegurarnos de que ProyectoDetalle tenga acceso a page
        self.proyectos = ProyectoApp(Detalle_Proyecto)  # Guardamos la referencia
        self.proyectos.page = page  # Asegurarnos de que ProyectoApp tenga acceso a page
        Detalle_Proyecto.set_proyecto_app(self.proyectos)
        
        # AppBar con botón de configuraciones
        self.appbar = AppBar(
            title=Text('Gestor de Documentos - Bienvenido: ' + session["username"] + ("(Admin)" if session["isadmin"] else ""), 
                color=COLOR_TEXTO_BOTON),
            bgcolor=COLOR_PRIMARIO,
            actions=[
                ft.IconButton(
                    icon=ft.icons.SETTINGS,
                    icon_color=COLOR_TEXTO_BOTON,
                    icon_size=24,
                    tooltip="Configuraciones",
                    on_click=lambda _: page.go('/Configuraciones')
                )
            ]
        )
        
        column1 = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[self.proyectos],
                        alignment=CrossAxisAlignment.START,
                        spacing=ESPACIADO_NORMAL
                    ),
                    width=400,
                    height=600,
                    padding=ESPACIADO_NORMAL,
                    border_radius=BORDE_RADIO
                )
            ],
            alignment=CrossAxisAlignment.START,
            spacing=ESPACIADO_NORMAL
        )

        column2 = ft.Column(
            controls=[
                Detalle_Proyecto,
                ft.Container(
                    content=ft.Column(
                        controls=[documentos_app],
                        alignment=CrossAxisAlignment.START,
                        spacing=ESPACIADO_NORMAL
                    ),
                    width=400,
                    height=500,
                    padding=ESPACIADO_NORMAL,
                    border_radius=BORDE_RADIO
                )
            ],
            alignment=CrossAxisAlignment.START,
            spacing=ESPACIADO_NORMAL
        )

        column3 = ft.Column(
            controls=[
                documento_detalle,
                version_detalle
            ],
            alignment=CrossAxisAlignment.START,
            spacing=ESPACIADO_NORMAL
        )
        
        # Controles de la vista
        self.controls = [
            self.appbar,
            ft.Container(
                content=ft.Row(
                    controls=[column1, column2, column3],
                    alignment=MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.START
                ),
                margin=ft.margin.only(top=20),
                alignment=ft.alignment.top_center
            )
        ]
        
        # Cargar proyectos después de que la vista esté lista
        self.did_mount = self.cargar_proyectos_iniciales
    
    def cargar_proyectos_iniciales(self):
        """Carga los proyectos después de que la vista esté completamente cargada."""
        self.proyectos.cargar_proyectos()

class ConfiguracionesView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.route = '/Configuraciones'
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.spacing = ESPACIADO_NORMAL
        
        # AppBar
        self.appbar = AppBar(
            title=Text('Gestor de Documentos - Configuraciones', color=COLOR_TEXTO_BOTON),
            bgcolor=COLOR_PRIMARIO
        )
        
        # Controles de la vista
        self.controls = [
            self.appbar,
            ft.Row(
                controls=[
                    Text("Configuraciones del Sistema", size=TEXTO_GRANDE, color=COLOR_TEXTO)
                ],
                alignment=MainAxisAlignment.SPACE_EVENLY,
            )
        ]

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Sistema de Gestión de Documentos"
        page.window_width = 800
        page.window_height = 600
        page.scroll = ft.ScrollMode.ADAPTIVE

        # Diccionario para mantener el estado de la sesión
        session = {"username": None, "password": None, "isadmin": False}
        
        def route_change(e: RouteChangeEvent):
            print(f"Cambiando ruta a: {e.route}")
            page.views.clear()
            
            if e.route == "/":
                print("Cargando vista de bienvenida")
                page.views.append(BienvenidaView(page))
            
            elif e.route == "/Registro":
                print("Cargando vista de registro")
                page.views.append(RegistroView(page))
                
            elif e.route == "/Login":
                print("Cargando vista de login")
                page.views.append(LoginView(page, session))
                
            elif e.route == "/Home":
                print(f"Intentando cargar Home. Estado de sesión: {session}")
                if not session["username"]:
                    print("No hay sesión activa, redirigiendo a login")
                    page.go("/Login")
                    return
                
            page.update()
            print(f"Vista actualizada: {page.route}")

        def view_pop(e: ViewPopEvent):
            print(f"Regresando a vista anterior: {e.view}")
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        
        print("Iniciando aplicación")
        page.go(page.route)

    ft.app(target=main, view=ft.WEB_BROWSER)
