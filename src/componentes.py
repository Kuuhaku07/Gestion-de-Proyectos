import datetime
import flet as ft
from database import obtener_proyectos,crear_proyecto, modificar_proyecto
from flet import Text, Icons



class Proyecto(ft.Column):
    def __init__(self, id, nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto,detalle_component):
        super().__init__()  # Llama al constructor de ft.Column
        self.id = id
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.cliente = cliente
        self.codigo_proyecto = codigo_proyecto
        self.detalle_component = detalle_component 

        self.edit_name = ft.TextField(expand=1, value=self.nombre)
        
        self.display_task = ft.Container(
            content=ft.Text(value=self.mostrar_info()),
            on_click=self.select_clicked,  
            padding=10,  
            border_radius=5,  # Opcional: para darle un aspecto más amigable
            bgcolor="#90D5FF",  # Color de fondo
            width=300
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
                            tooltip="Download Project",
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
        # Aquí deberías implementar la lógica para eliminar el proyecto
        dlg = ReusableModal(
            title="Deleting Project",
            content=f"Deleting project: {self.nombre}",
            actions=[ft.TextButton("Close", on_click=lambda e: dlg.close(self.page))],
            modal=False
        )
        dlg.open(self.page)


    def select_clicked(self, e):
        # Lógica para seleccionar el proyecto
         self.detalle_component.mostrar_detalles(self.id, self.nombre, self.fecha_inicio, self.fecha_fin, self.cliente, self.codigo_proyecto)

class ReusableModal:
    def __init__(self, title, content, actions, modal=True):
        self.title = title
        self.content = content
        self.actions = actions
        self.modal = modal
        self.dialog = ft.AlertDialog(
            title=ft.Text(self.title),
            content=ft.Text(self.content),
            actions=self.actions,
            modal=self.modal,
            on_dismiss=self.on_dismiss
        )

    def on_dismiss(self, e):
        pass

    def open(self, page):
        page.open(self.dialog)
    def close(self, page):
        page.close(self.dialog)


class ProyectoDetalle(ft.Container):
    def __init__(self):
        super().__init__()
        self.scroll = ft.ScrollMode.AUTO  # Habilitar scroll
        self.width = 400  # Ajustar el ancho para que coincida con ProyectoApp
        self.height = 300  # Ajustar la altura
        self.border = ft.border.all(1,"black")
        self.border_radius=ft.border_radius.all(10)
        # Establecer el borde y el fondo
        self.padding = 10  # Espaciado interno
        self.bgcolor = ft.colors.WHITE  # Color de fondo

        # Crear una columna para los detalles del proyecto
        self.details_column = ft.Column(controls=[], alignment=ft.MainAxisAlignment.CENTER)

        # Mensaje inicial
        self.initial_message = ft.Text("Seleccione un proyecto para ver los detalles", size=20, text_align=ft.TextAlign.CENTER)
        self.details_column.controls.append(self.initial_message)

        # Botón de editar
        self.edit_button = ft.TextButton("Editar", on_click=self.edit_clicked)  # Inicialmente invisible
        self.current_project={}
        self.proyecto_app=None

        # Agregar la columna al contenedor
        self.content = self.details_column
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
        # Agregar detalles a la columna
        self.details_column.controls.append(self.edit_button)
        self.details_column.controls.append(ft.Text(f"ID: {id_proyecto}", size=18, text_align=ft.TextAlign.CENTER))
        self.details_column.controls.append(ft.Text(f"Nombre: {nombre}", size=18, text_align=ft.TextAlign.CENTER))
        self.details_column.controls.append(ft.Text(f"Fecha de Inicio: {fecha_inicio}", size=18, text_align=ft.TextAlign.CENTER))
        self.details_column.controls.append(ft.Text(f"Fecha de Fin: {fecha_fin}", size=18, text_align=ft.TextAlign.CENTER))
        self.details_column.controls.append(ft.Text(f"Cliente: {cliente}", size=18, text_align=ft.TextAlign.CENTER))
        self.details_column.controls.append(ft.Text(f"Código del Proyecto: {codigo_proyecto}", size=18, text_align=ft.TextAlign.CENTER))


        # Actualizar la interfaz
        self.update()  # Actualizar la interfaz
    
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
        accept_button = ft.TextButton("Aceptar", on_click=lambda e: self.submit_edit(name_field.value, start_date_field.value, end_date_field.value, client_field.value, project_code_field.value,warning_signal,dlg))
        cancel_button = ft.TextButton("Cancelar", on_click=lambda e: dlg.close(self.page))

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
            self.proyecto_app.search_projects(self.proyecto_app.search_name.value)
            self.mostrar_detalles(self.current_project["id"], nombre, fecha_inicio, fecha_fin, cliente, codigo_proyecto)  # Actualizar los detalles
        
    

        
class ProyectoApp(ft.Column):
    def __init__(self,detalle_component):
        super().__init__()
        self.detalle_component=detalle_component
        self.search_name = ft.TextField(
            hint_text="Nombre del proyecto", expand=True
        )
        
        self.projects = ft.ListView(
            spacing=10,
            width=400,
            height=300,
            
        )

        self.items_left = ft.Text("0 proyectos")

        self.width = 400
        self.controls = [
            ft.Row(
                [ft.Text(value="Proyectos", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.search_name,
                    ft.FloatingActionButton(
                        icon=ft.icons.SEARCH,
                        on_click=self.search_projects  
                    ),
                ],
            ),
            ft.Row(
                controls=[
                    self.items_left,
                    ft.FloatingActionButton(
                        text= "Nuevo", height=20, on_click=self.open_project_modal
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            self.projects,
        ]

    def open_project_modal(self, e):
        # Create a modal for project data entry
        project_name = ft.TextField(hint_text="Nombre del proyecto")
        
        
        start_date = ft.TextField(hint_text="Fecha de inicio",disabled=True)
        start_date_button = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e:  CustomDatePicker(self.page, start_date).open()
        )
        end_date = ft.TextField(hint_text="Fecha de fin", disabled=True)
        end_date_button = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e:  CustomDatePicker(self.page, end_date).open()
        )
        
        client = ft.TextField(hint_text="Cliente")
        project_code = ft.TextField(hint_text="Código del proyecto")
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
        accept_button = ft.TextButton("Aceptar", on_click=lambda e: self.submit_project_data(project_name.value, start_date.value, end_date.value, client.value, project_code.value,warning_signal,dlg))
        cancel_button = ft.TextButton("Cancelar", on_click=lambda e: dlg.close(self.page))

        dlg = ReusableModal(
            title="Nuevo Proyecto",
            content="",
            actions=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[warning_signal,
                                      project_name,
                                      ft.Row(controls=[start_date,start_date_button],
                                             alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                      ft.Row(controls=[end_date,end_date_button],
                                             alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                                      client,
                                      project_code],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    width=350),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(
                    height=20  ),
                    
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN) ],
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
            self.search_projects


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
        self.items_left.value = f"{len(proyectos)} proyecto(s) found"
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
                ft.Icon(icon, color=text_color),
                Text(message, color=text_color)
            ]
        ),
        bgcolor=background_color,
        padding=10,
        margin=10,
        border_radius=5
    )

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

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "ToDo App"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.scroll = ft.ScrollMode.ADAPTIVE

        detalle=ProyectoDetalle()
        proyecto_app=ProyectoApp(detalle)
        detalle.set_proyecto_app(proyecto_app)
        # Create app control and add it to the page
        app = ft.Row(controls=[proyecto_app,detalle])
        page.add(app)


    ft.app(main)
