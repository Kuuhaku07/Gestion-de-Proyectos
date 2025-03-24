import sys
import flet as ft
from flet import View,Icons, Page, AppBar, ElevatedButton,TextField, Text, RouteChangeEvent, ViewPopEvent,CrossAxisAlignment,MainAxisAlignment
from database import *
from funciones import *
from componentes import *

inicializar_tablas()

def main(page: ft.Page):
    page.title = "Gestor de Documentos"
    
    page.window.width = 600
    page.window.height = 800
    session = {
                "username": None,
                "password": None,
                "isadmin": False
            }   
    def route_change(e: RouteChangeEvent):
        



        

        page.views.clear()
        #Bienvenida

        title = Text("Gestor de Documentos", size=30, weight=ft.FontWeight.BOLD, color="#1E88E5")
        subtitle = Text("Lisduer Parra", size=20, color="#808080")  # Updated to valid hex color
        page.views.append(
            View(
                route='/',
                controls=[AppBar(title=Text('Bienvenido'),bgcolor='blue'),
                         title,subtitle,
                         ElevatedButton(
                          text='Registrarse' if not verificar_usuarios_existentes() else 'Iniciar Sesion',
                          on_click=lambda _: page.go('/Registro' if not verificar_usuarios_existentes() else '/Login'))
                           ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=20))
        
        
        
        
        
        
        #Registro
        if page.route == '/Registro':
            page.window.width = 600
            page.window.height = 800
            def registro_pressed(e):
                registrar_inicio(username_input.value, password_input.value)
                page.go('/')

            registro_titulo = Text("Registro de Usuario", size=30, weight=ft.FontWeight.BOLD)
            username_input = TextField(label="Nombre de Usuario")
            password_input = TextField(label="Contraseña", password=True,can_reveal_password=True)
            registro_button = ElevatedButton(text="Registrar", 
                                             on_click=registro_pressed
                                             )
            
                                  

            page.views.append(
            View(
                route='/Registro',
                controls=[AppBar(title=Text('Registro'),bgcolor='blue'),
                         registro_titulo,
                         ft.Container(
                            content=ft.Column(
                                controls=[
                                    create_info_box(
                                        text_color="black",
                                        background_color="#90D5FF",
                                        message="Dado que no hay ningún usuario registrado, se registrará un administrador."
                                    ),],
                                alignment=CrossAxisAlignment.CENTER,
                            ),
                            width=600,  # Limit the width of the container

                        ),           
                         ft.Container(
                            content=ft.Column(
                                controls=[
                                    
                                    username_input, 
                                    password_input, 
                                    registro_button],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            width=400,  # Limit the width of the container

                        )
                           ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=20))
            
        
        
        
        
        #Login
        if page.route == '/Login':
            page.window.width = 600
            page.window.height = 800
            error_login = False

            

            def Login_pressed(e):
                nonlocal error_login
                nonlocal session
                if login_user(username_input.value, password_input.value):
                    error_login = False
                    session["username"] = username_input.value  # Set the username in session
                    session["password"] = password_input.value  # Set the password in session
                    session["isadmin"] = isadmin(username_input.value)  # Check if the user is admin
                    page.go('/Home')
                else: 
                     error_login = True
                
                if error_login:
                    warning_signal.visible = True  # Show the warning signal
                else:
                    warning_signal.visible = False  # Hide the warning signal
                page.update()


            inicio_titulo = Text("Iniciar Sesion", size=30, weight=ft.FontWeight.BOLD)
            username_input = TextField(label="Nombre de Usuario", border=ft.InputBorder.UNDERLINE,)
            password_input = TextField(label="Contraseña", password=True, can_reveal_password=True, border=ft.InputBorder.UNDERLINE,)
            inicio_button = ElevatedButton(text="Iniciar sesion",
                                             on_click=Login_pressed
                                             )
            warning_signal = ft.Container(
                            content=ft.Column(
                                controls=[
                                    create_info_box(
                                        text_color="black",
                                        background_color="#f3464a",
                                        message="Usuario o Contraseña incorrecta."
                                    ),],
                                alignment=CrossAxisAlignment.CENTER,
                            ),
                            width=600,  # Limit the width of the container
                            visible=False  # Initially hidden

                        )                                      

            page.views.append(
            View(
                route='/Login',
                controls=[AppBar(title=Text('Registro'),bgcolor='blue'),
                         inicio_titulo,  
                         warning_signal,
                         
                         ft.Container(
                            content=ft.Column(
                                controls=[
                                    
                                    username_input, 
                                    password_input, 
                                    inicio_button],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            width=400,  # Limit the width of the container

                        )
                           ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=20))
        


        #Home
        if page.route == '/Home':
            page.window.width = 1000
            page.window.height = 800

            # Columna 1: Proyectos
            Detalle_Proyecto=ProyectoDetalle()
            Proyectos= ProyectoApp(Detalle_Proyecto)
            Detalle_Proyecto.set_proyecto_app(Proyectos)
            
            column1 = ft.Column(
                controls=[
                    ElevatedButton(
                        text="Configuraciones",
                        icon=Icons.SETTINGS,
                        on_click=lambda _: page.go('/Configuraciones')  # Redireccionar a configuraciones
                    ),
                    
                    Text("Proyectos", size=30, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                Proyectos
                            ],
                            alignment=CrossAxisAlignment.START,
                            spacing=10
                        ),
                        width=400,  # Set a specific width for the container to match the column width
                        height=500,  # Adjust height to occupy remaining space
                        bgcolor="#f0f0f0",  # Background color for visibility
                        padding=10,
                        border_radius=5
                    )
                ],
                alignment=CrossAxisAlignment.START,
                spacing=10
                )
                

            column2 = ft.Column(
                controls=[
                    Detalle_Proyecto
                ],
                alignment=CrossAxisAlignment.START,
                spacing=10
            )

            column3 = ft.Column(
                controls=[
                    Text("Column 3: Additional Information", size=20, weight=ft.FontWeight.BOLD),
                    # Add additional information or settings here
                ],
                alignment=CrossAxisAlignment.START,
                spacing=10
            )

            


                                     

            page.views.append(
            View(
                route='/Home',
                controls=[AppBar(title=Text('Gestor de Documentos - Bienvenido: ' + session["username"]+"(Admin)" if session["isadmin"] else ""),bgcolor='blue'),
                          ft.Row(
                    controls=[column1, column2, column3],
                    alignment=MainAxisAlignment.SPACE_EVENLY,  # Distribute space evenly
                ),
                           ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=20))
            page.update()
            Proyectos.cargar_proyectos()
        
            
            





        #Configuraciones
        if page.route == '/Configuraciones':
            page.window.width = 1000
            page.window.height = 800

                                  

            page.views.append(
            View(
                route='/Configuraciones',
                controls=[AppBar(title=Text('Gestor de Documentos - Configuraciones ' ),bgcolor='blue'),
                          ft.Row(
                    controls=[
                        Text("por hacer")
                    ],
                    alignment=MainAxisAlignment.SPACE_EVENLY,  
                ),
                           ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=20))

        page.update()

    def view_pop (e:ViewPopEvent):
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop =view_pop
    page.go (page.route)

def registrar_inicio(user,password):
    password_hashed=hash_text(password)
    crear_usuario(user, password_hashed, True)
    llave_maestra=generar_clave()
    llave_encriptada=xor_encrypt_decrypt(llave_maestra,password)
    registrar_llave(llave_encriptada,password_hashed)


    

        





ft.app(main)
