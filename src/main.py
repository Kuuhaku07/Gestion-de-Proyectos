import sys
import flet as ft
from flet import View, Icons, Page, AppBar, ElevatedButton, TextField, Text, RouteChangeEvent, ViewPopEvent, CrossAxisAlignment, MainAxisAlignment
from database import *
from funciones import *
from componentes import *
from paleta import *
from configuraciones import ConfiguracionesView

def main(page: ft.Page):
    # Configuración inicial de la página
    page.title = "Gestor de Documentos"
    page.window.width = 800
    page.window.height = 600
    page.window.maximized = False
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    
    # Inicializar la sesión
    session = {
                "username": None,
                "password": None,
                "isadmin": False
            }   

    def route_change(e: RouteChangeEvent):
        page.views.clear()
        
        # Bienvenida
        if page.route == "/" or page.route == "":
            page.window.width = 800
            page.window.height = 600
            page.window.maximized = False
            page.views.append(BienvenidaView(page))
        
        # Registro
        elif page.route == '/Registro':
            page.window.width = 600
            page.window.height = 800
            page.views.append(RegistroView(page))
        
        # Login
        elif page.route == '/Login':
            page.window.width = 600
            page.window.height = 800
            page.views.append(LoginView(page, session))

        # Home
        elif page.route == '/Home':
            if not session["username"]:
                page.go("/Login")
                return
                
            page.window.maximized = True  # Maximizar la ventana
            page.window.width = 1920  # Tamaño por defecto si no se maximiza
            page.window.height = 1080
            page.views.append(HomeView(page, session))

        # Configuraciones
        elif page.route == '/Configuraciones':
            if not session["username"]:
                page.go("/Login")
                return
                
            page.window.maximized = True  
            page.window.width = 1920
            page.window.height = 1080
            page.views.append(ConfiguracionesView(page, session))
            
        # Actualizar la página después de cargar cualquier vista
        page.update()

    def view_pop(e: ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Configurar los manejadores de eventos
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Asegurarse de que las tablas estén inicializadas
    inicializar_tablas()
    
    # Ir a la ruta inicial
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
