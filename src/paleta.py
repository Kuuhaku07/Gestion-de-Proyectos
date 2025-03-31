import flet as ft
# Paleta de colores basada en IBM Carbon Design System

# Colores principales
COLOR_PRIMARIO = "#0f62fe"  # Blue 60
COLOR_SECUNDARIO = "#393939"  # Gray 80
COLOR_TERCIARIO = "#6f6f6f"  # Gray 60

# Colores de estado
COLOR_ERROR = "#da1e28"  # Red 60
COLOR_EXITO = "#198038"  # Green 60
COLOR_ADVERTENCIA = "#f1c21b"  # Yellow 30
COLOR_INFO = "#0043ce"  # Blue 70

# Colores de fondo
COLOR_FONDO = "#ffffff"  # White
COLOR_FONDO_SECUNDARIO = "#f4f4f4"  # Gray 10
COLOR_FONDO_HOVER = "#e8e8e8"  # Gray 20

# Colores de texto
COLOR_TEXTO = "#161616"  # Gray 100
COLOR_TEXTO_SECUNDARIO = "#525252"  # Gray 70
COLOR_TEXTO_TERCIARIO = "#6f6f6f"  # Gray 60
COLOR_TEXTO_ERROR = "#ffffff"  # White (para mensajes de error)
COLOR_TEXTO_BOTON = "#ffffff"  # White (para texto en botones)
COLOR_TEXTO_PLACEHOLDER = "#a8a8a8"  # Gray 40

# Colores de borde
COLOR_BORDE = "#8d8d8d"  # Gray 50
COLOR_BORDE_ENFASIS = "#4589ff"  # Blue 50

# Colores de componentes específicos
COLOR_BOTON = COLOR_PRIMARIO
COLOR_BOTON_HOVER = "#0353e9"  # Blue 70
COLOR_BOTON_ACTIVO = "#002d9c"  # Blue 80
COLOR_BOTON_DESHABILITADO = "#c6c6c6"  # Gray 30

# Colores para elementos de lista/tarjetas
COLOR_ITEM = "#f4f4f4"  # Gray 10
COLOR_ITEM_HOVER = "#e0e0e0"  # Gray 20
COLOR_ITEM_SELECCIONADO = "#a6c8ff"  # Blue 30

# Colores para versiones
COLOR_VERSION = "#e8daff"  # Purple 20
COLOR_VERSION_HOVER = "#d4bbff"  # Purple 30

# Colores para modo oscuro
COLOR_FONDO_DARK = "#161616"  # Gray 100
COLOR_FONDO_SECUNDARIO_DARK = "#262626"  # Gray 90
COLOR_FONDO_HOVER_DARK = "#393939"  # Gray 80

COLOR_TEXTO_DARK = "#ffffff"  # White
COLOR_TEXTO_SECUNDARIO_DARK = "#c6c6c6"  # Gray 30
COLOR_TEXTO_TERCIARIO_DARK = "#a8a8a8"  # Gray 40

COLOR_BORDE_DARK = "#6f6f6f"  # Gray 60
COLOR_BORDE_ENFASIS_DARK = "#78a9ff"  # Blue 40

COLOR_ITEM_DARK = "#262626"  # Gray 90
COLOR_ITEM_HOVER_DARK = "#393939"  # Gray 80
COLOR_ITEM_SELECCIONADO_DARK = "#054ada"  # Blue 70

COLOR_VERSION_DARK = "#491d8b"  # Purple 70
COLOR_VERSION_HOVER_DARK = "#6929c4"  # Purple 60

# Tamaños de texto
TEXTO_PEQUEÑO = 12
TEXTO_NORMAL = 14
TEXTO_GRANDE = 16
TITULO = 20
TEXTO_EXTRA_GRANDE = 24
TEXTO_TITULO = 24

# Espaciado
ESPACIADO_PEQUENO = 5
ESPACIADO_NORMAL = 10
ESPACIADO_GRANDE = 20

# Bordes
BORDE_RADIO = 5
BORDE_RADIO_GRANDE = 10

# Sombras
SOMBRA_NORMAL = ft.BoxShadow(
    spread_radius=1,
    blur_radius=4,
    color=ft.colors.with_opacity(0.25, "#000000")
)
SOMBRA_ELEVADA = "0 4px 8px rgba(0, 0, 0, 0.2)"

def get_color(color_claro, color_oscuro, theme_mode):
    """Retorna el color apropiado según el modo del tema"""
    return color_oscuro if theme_mode == ft.ThemeMode.DARK else color_claro