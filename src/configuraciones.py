import flet as ft
from paleta import *
from database import *
from componentes import ReusableModal,create_info_box
class ConfiguracionesView(ft.View):
    def __init__(self, page, session):
        super().__init__()
        self.page = page
        self.session = session
        self.initialize_view()

    def initialize_view(self):
        # AppBar con botón para volver a home y cerrar sesión
        self.appbar = ft.AppBar(
            title=ft.Text("Configuraciones", color=COLOR_TEXTO_BOTON),
            bgcolor=COLOR_PRIMARIO,
            actions=[
                ft.IconButton(
                    icon=ft.icons.HOME,
                    icon_color=COLOR_TEXTO_BOTON,
                    icon_size=24,
                    tooltip="Volver al Inicio",
                    on_click=lambda _: self.page.go('/Home')
                ),
                ft.IconButton(
                    icon=ft.icons.LOGOUT,
                    icon_color=COLOR_TEXTO_BOTON,
                    icon_size=24,
                    tooltip="Cerrar Sesión",
                    on_click=self.show_logout_dialog
                )
            ]
        )

        # Tabs de navegación
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            on_change=self.on_tab_change,
            tabs=[
                ft.Tab(
                    text="General",
                    icon=ft.icons.SETTINGS_OUTLINED,
                    content=self.create_general_section()
                ),
            ],
            expand=1
        )

        # Si es admin, agregar pestaña de usuarios
        if self.session.get("isadmin"):
            self.tabs.tabs.append(
                ft.Tab(
                    text="Usuarios",
                    icon=ft.icons.PEOPLE_OUTLINED,
                    content=self.create_users_section()
                )
            )

        # Contenedor principal
        main_container = ft.Container(
            content=self.tabs,
            margin=ft.margin.only(top=20),
            padding=ESPACIADO_NORMAL
        )

        # Estructura de la vista
        self.controls = [
            self.appbar,
            main_container
        ]

    def on_tab_change(self, e):
        # Si se selecciona la pestaña de usuarios (índice 1 para admin)
        if self.session.get("isadmin") and e.control.selected_index == 1:
            self.cargar_usuarios()

    def create_general_section(self):
        # Campo para mostrar la ruta actual
        self.ruta_descarga = ft.TextField(
            label="Ruta de Descarga de PDFs",
            read_only=True,
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL,
            expand=True
        )
        
        # Botón para seleccionar carpeta
        self.select_folder_button = ft.ElevatedButton(
            "Seleccionar Carpeta",
            icon=ft.icons.FOLDER_OPEN,
            on_click=self.select_download_folder,
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_BOTON
            )
        )
        
        # Cargar ruta actual
        ruta_actual = self.page.client_storage.get("download_path")
        if ruta_actual:
            self.ruta_descarga.value = ruta_actual
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Configuración General",
                        size=TEXTO_GRANDE,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXTO
                    ),
                    ft.Divider(color=COLOR_BORDE),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Ruta de Descarga",
                                    size=TEXTO_NORMAL,
                                    weight=ft.FontWeight.BOLD,
                                    color=COLOR_TEXTO
                                ),
                                ft.Row(
                                    controls=[
                                        self.ruta_descarga,
                                        self.select_folder_button
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Text(
                                    "Seleccione la carpeta donde se guardarán los PDFs descargados",
                                    size=TEXTO_PEQUEÑO,
                                    color=COLOR_TEXTO_SECUNDARIO
                                )
                            ],
                            spacing=ESPACIADO_NORMAL
                        ),
                        padding=ESPACIADO_NORMAL,
                        border=ft.border.all(1, COLOR_BORDE),
                        border_radius=10
                    )
                ],
                spacing=ESPACIADO_NORMAL,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=ESPACIADO_NORMAL
        )

    def select_download_folder(self, e):
        def handle_result(e: ft.FilePickerResultEvent):
            if e.path:
                # Guardar la ruta seleccionada
                self.page.client_storage.set("download_path", e.path)
                self.ruta_descarga.value = e.path
                self.ruta_descarga.update()

        # Crear el diálogo de selección de carpeta
        pick_files_dialog = ft.FilePicker(
            on_result=handle_result
        )
        
        # Agregar el diálogo a la página
        self.page.overlay.append(pick_files_dialog)
        self.page.update()
        
        # Abrir el diálogo
        pick_files_dialog.get_directory_path()

    def create_users_section(self):
        # Crear ListView para usuarios
        self.usuarios_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            height=400
        )
        
        # Crear botón de agregar
        self.add_button = ft.FloatingActionButton(
            icon=ft.icons.ADD,
            text="Agregar Usuario",
            on_click=self.show_add_user_dialog,
            bgcolor=COLOR_BOTON
        )
        
        # Crear contenedor principal
        container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Usuarios del Sistema",
                        size=TITULO,
                        color=COLOR_TEXTO,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(height=ESPACIADO_NORMAL),
                    self.usuarios_list,
                    self.add_button
                ],
                spacing=ESPACIADO_NORMAL
            ),
            padding=ESPACIADO_GRANDE
        )
        
        return container

    def cargar_usuarios(self):
        # Obtener datos de usuarios
        usuarios = obtener_datos_usuarios()
        
        # Limpiar lista actual
        self.usuarios_list.controls.clear()
        
        # Agregar cada usuario a la lista
        for username, isadmin in usuarios:
            # Crear fila de usuario
            user_row = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(
                            username,
                            size=TEXTO_NORMAL,
                            color=COLOR_TEXTO,
                            expand=True
                        ),
                        ft.Text(
                            "Admin" if isadmin else "Usuario",
                            size=TEXTO_NORMAL,
                            color=COLOR_TEXTO_SECUNDARIO,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_color=COLOR_ERROR,
                            tooltip="Eliminar",
                            on_click=lambda e, u=username: self.show_delete_user_dialog(u)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=10,
                border=ft.border.all(1, COLOR_BORDE),
                border_radius=10
            )
            self.usuarios_list.controls.append(user_row)
        
        # Actualizar la lista
        self.usuarios_list.update()

    def show_logout_dialog(self, e):
        # Crear el modal de confirmación
        accept_button = ft.TextButton(
            "Cerrar Sesión",
            style=ft.ButtonStyle(
                color=COLOR_TEXTO_BOTON,
                bgcolor=COLOR_ERROR
            ),
            on_click=lambda e: self.confirm_logout(dlg)
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
            title="Confirmar Cierre de Sesión",
            content="¿Está seguro que desea cerrar la sesión?",
            actions=[
                ft.Row(
                    controls=[accept_button, cancel_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def confirm_logout(self, dlg):
        # Cerrar el modal
        dlg.close(self.page)
        
        # Limpiar la sesión
        self.session["username"] = None
        self.session["password"] = None
        self.session["isadmin"] = False
        self.session["llave_maestra"] = None
        
        # Volver a la página inicial
        self.page.go("/")

    def show_add_user_dialog(self, e):
        # Campos del formulario
        username_field = ft.TextField(
            label="Nombre de Usuario",
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        
        password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        
        confirm_password_field = ft.TextField(
            label="Confirmar Contraseña",
            password=True,
            can_reveal_password=True,
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        
        isadmin_field = ft.Checkbox(
            label="Administrador",
            value=False
        )

        warning_signal = ft.Container(
            content=ft.Column(
                controls=[
                    create_info_box(
                        text_color=COLOR_TEXTO_ERROR,
                        background_color=COLOR_ERROR,
                        message="Por favor, complete todos los campos correctamente."
                    ),
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=350,
            visible=False
        )

        def submit_user(e):
            username = username_field.value
            password = password_field.value
            confirm_password = confirm_password_field.value
            isadmin = isadmin_field.value

            if not username or not password or not confirm_password:
                warning_signal.visible = True
                warning_signal.update()
                return

            if password != confirm_password:
                warning_signal.content.controls[0] = create_info_box(
                    text_color=COLOR_TEXTO_ERROR,
                    background_color=COLOR_ERROR,
                    message="Las contraseñas no coinciden."
                )
                warning_signal.visible = True
                warning_signal.update()
                return

            try:
                # Crear usuario
                crear_usuario(username, hash_text(password), isadmin)
                
                # Obtener la llave maestra existente
                llave_maestra = self.page.client_storage.get("llave_maestra")
                if llave_maestra:
                    # Encriptar la llave con la contraseña del nuevo usuario
                    llave_encriptada = xor_encrypt_decrypt(llave_maestra, password)
                    registrar_llave(llave_encriptada, hash_text(password))

                dlg.close(self.page)
                self.cargar_usuarios()
            except Exception as e:
                warning_signal.content.controls[0] = create_info_box(
                    text_color=COLOR_TEXTO_ERROR,
                    background_color=COLOR_ERROR,
                    message=f"Error al crear usuario: {str(e)}"
                )
                warning_signal.visible = True
                warning_signal.update()

        dlg = ReusableModal(
            title="Nuevo Usuario",
            content="",
            actions=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                warning_signal,
                                username_field,
                                password_field,
                                confirm_password_field,
                                isadmin_field
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
                    controls=[
                        ft.TextButton(
                            "Cancelar",
                            style=ft.ButtonStyle(
                                color=COLOR_TEXTO_BOTON,
                                bgcolor=COLOR_ERROR
                            ),
                            on_click=lambda e: dlg.close(self.page)
                        ),
                        ft.TextButton(
                            "Crear",
                            style=ft.ButtonStyle(
                                color=COLOR_TEXTO_BOTON,
                                bgcolor=COLOR_BOTON
                            ),
                            on_click=submit_user
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def show_edit_user_dialog(self, username):
        # Obtener datos del usuario
        isadmin = isadmin(username)

        # Campos del formulario
        username_field = ft.TextField(
            label="Nombre de Usuario",
            value=username,
            disabled=True,
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        
        password_field = ft.TextField(
            label="Nueva Contraseña",
            password=True,
            can_reveal_password=True,
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        
        confirm_password_field = ft.TextField(
            label="Confirmar Nueva Contraseña",
            password=True,
            can_reveal_password=True,
            border_color=COLOR_BORDE,
            focused_border_color=COLOR_PRIMARIO,
            text_size=TEXTO_NORMAL
        )
        
        isadmin_field = ft.Checkbox(
            label="Administrador",
            value=isadmin
        )

        warning_signal = ft.Container(
            content=ft.Column(
                controls=[
                    create_info_box(
                        text_color=COLOR_TEXTO_ERROR,
                        background_color=COLOR_ERROR,
                        message="Por favor, complete todos los campos correctamente."
                    ),
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=350,
            visible=False
        )

        def submit_edit(e):
            new_password = password_field.value
            confirm_password = confirm_password_field.value
            new_isadmin = isadmin_field.value

            if new_password and new_password != confirm_password:
                warning_signal.content.controls[0] = create_info_box(
                    text_color=COLOR_TEXTO_ERROR,
                    background_color=COLOR_ERROR,
                    message="Las contraseñas no coinciden."
                )
                warning_signal.visible = True
                warning_signal.update()
                return

            try:
                # Actualizar usuario
                if new_password:
                    # Actualizar contraseña y llave
                    crear_usuario(username, hash_text(new_password), new_isadmin)
                    llave_maestra = self.page.client_storage.get("llave_maestra")
                    if llave_maestra:
                        llave_encriptada = xor_encrypt_decrypt(llave_maestra, new_password)
                        registrar_llave(llave_encriptada, hash_text(new_password))
                else:
                    # Solo actualizar rol
                    crear_usuario(username, hash_text(self.session["password"]), new_isadmin)

                dlg.close(self.page)
                self.cargar_usuarios()
            except Exception as e:
                warning_signal.content.controls[0] = create_info_box(
                    text_color=COLOR_TEXTO_ERROR,
                    background_color=COLOR_ERROR,
                    message=f"Error al actualizar usuario: {str(e)}"
                )
                warning_signal.visible = True
                warning_signal.update()

        dlg = ReusableModal(
            title="Editar Usuario",
            content="",
            actions=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                warning_signal,
                                username_field,
                                password_field,
                                confirm_password_field,
                                isadmin_field
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
                    controls=[
                        ft.TextButton(
                            "Cancelar",
                            style=ft.ButtonStyle(
                                color=COLOR_TEXTO_BOTON,
                                bgcolor=COLOR_ERROR
                            ),
                            on_click=lambda e: dlg.close(self.page)
                        ),
                        ft.TextButton(
                            "Guardar",
                            style=ft.ButtonStyle(
                                color=COLOR_TEXTO_BOTON,
                                bgcolor=COLOR_BOTON
                            ),
                            on_click=submit_edit
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def show_delete_user_dialog(self, username):
        dlg = ReusableModal(
            title="Eliminar Usuario",
            content=f"¿Está seguro que desea eliminar el usuario '{username}'?",
            actions=[
                ft.Row(
                    controls=[
                        ft.TextButton(
                            "Cancelar",
                            style=ft.ButtonStyle(
                                color=COLOR_TEXTO_BOTON,
                                bgcolor=COLOR_BOTON
                            ),
                            on_click=lambda e: dlg.close(self.page)
                        ),
                        ft.TextButton(
                            "Eliminar",
                            style=ft.ButtonStyle(
                                color=COLOR_TEXTO_BOTON,
                                bgcolor=COLOR_ERROR
                            ),
                            on_click=lambda e: self.confirm_delete_user(username, dlg)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            modal=True
        )
        dlg.open(self.page)

    def confirm_delete_user(self, username, dlg):
        try:
            # Eliminar usuario
            eliminar_usuario(username)
            dlg.close(self.page)
            self.cargar_usuarios()
        except Exception as e:
            error_dlg = ReusableModal(
                title="Error",
                content=f"Error al eliminar usuario: {str(e)}",
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