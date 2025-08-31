# Paleta de colores moderna, accesible y profesional
COLORES_TEMA = {
    # Colores de fondo - Sistema de capas
    "bg_primary": "#0a0a0a",      # Fondo principal muy oscuro
    "bg_secondary": "#1a1a1a",    # Fondo secundario
    "bg_card": "#2d2d2d",         # Fondo de tarjetas
    "bg_elevated": "#3a3a3a",     # Fondo elevado
    "bg_overlay": "#404040",      # Fondo de overlay
    
    # Colores de acento - Azul profesional
    "accent": "#2196f3",          # Azul principal (Material Blue)
    "accent_hover": "#1976d2",    # Azul hover
    "accent_secondary": "#00bcd4", # Azul claro
    "accent_light": "#64b5f6",    # Azul muy claro
    
    # Colores de texto - Alta legibilidad
    "text_primary": "#ffffff",    # Texto principal
    "text_secondary": "#e0e0e0",  # Texto secundario
    "text_muted": "#bdbdbd",      # Texto atenuado
    "text_disabled": "#9e9e9e",   # Texto deshabilitado
    "text_inverse": "#212121",    # Texto sobre fondos claros
    
    # Colores de estado - Semánticos y accesibles
    "success": "#4caf50",         # Verde éxito (Material Green)
    "success_light": "#81c784",   # Verde claro
    "warning": "#ff9800",         # Naranja advertencia (Material Orange)
    "warning_light": "#ffb74d",   # Naranja claro
    "error": "#f44336",           # Rojo error (Material Red)
    "error_light": "#e57373",     # Rojo claro
    "info": "#2196f3",            # Azul información
    "info_light": "#64b5f6",      # Azul claro
    
    # Colores de borde - Sutiles y definidos
    "border": "#424242",          # Borde principal
    "border_light": "#616161",    # Borde claro
    "border_dark": "#212121",     # Borde oscuro
    "border_accent": "#2196f3",   # Borde de acento
    
    # Colores de sombra - Profundidad visual
    "shadow": "#000000",          # Sombra principal
    "shadow_light": "#1a1a1a",    # Sombra clara
    "shadow_accent": "#2196f3",   # Sombra de acento
    
    # Colores de gráficos - Paleta profesional
    "chart_1": "#2196f3",        # Azul principal
    "chart_2": "#4caf50",        # Verde
    "chart_3": "#ff9800",        # Naranja
    "chart_4": "#f44336",        # Rojo
    "chart_5": "#9c27b0",        # Púrpura
    "chart_6": "#00bcd4",        # Cian
    "chart_7": "#ff5722",        # Rojo oscuro
    "chart_8": "#795548",        # Marrón
    
    # Colores de interfaz - Elementos específicos
    "input_bg": "#424242",       # Fondo de inputs
    "input_border": "#616161",   # Borde de inputs
    "input_focus": "#2196f3",    # Borde de focus
    "button_primary": "#2196f3", # Botón primario
    "button_secondary": "#424242", # Botón secundario
    "button_success": "#4caf50", # Botón éxito
    "button_warning": "#ff9800", # Botón advertencia
    "button_error": "#f44336",   # Botón error
}

# Configuración de fuentes - Sistema tipográfico coherente
FUENTES = {
    "titulo_principal": {"size": 28, "weight": "bold", "family": "Segoe UI"},
    "titulo_seccion": {"size": 22, "weight": "bold", "family": "Segoe UI"},
    "titulo_componente": {"size": 18, "weight": "bold", "family": "Segoe UI"},
    "texto_normal": {"size": 16, "weight": "normal", "family": "Segoe UI"},
    "texto_pequeno": {"size": 14, "weight": "normal", "family": "Segoe UI"},
    "texto_muy_pequeno": {"size": 12, "weight": "normal", "family": "Segoe UI"},
    "monospace": {"size": 14, "family": "Consolas", "weight": "normal"},
    "boton": {"size": 14, "weight": "bold", "family": "Segoe UI"},
}

# Configuración de espaciado - Sistema de espaciado coherente
ESPACIADO = {
    "xs": 4,      # 4px - Espaciado mínimo
    "sm": 8,      # 8px - Espaciado pequeño
    "md": 16,     # 16px - Espaciado medio
    "lg": 24,     # 24px - Espaciado grande
    "xl": 32,     # 32px - Espaciado extra grande
    "xxl": 48,    # 48px - Espaciado máximo
}

# Configuración de bordes - Sistema de bordes coherente
BORDES = {
    "radius_small": 4,      # 4px - Bordes pequeños
    "radius_medium": 8,     # 8px - Bordes medianos
    "radius_large": 12,     # 12px - Bordes grandes
    "radius_xlarge": 16,    # 16px - Bordes extra grandes
    "width_thin": 1,        # 1px - Borde fino
    "width_normal": 2,      # 2px - Borde normal
    "width_thick": 3,       # 3px - Borde grueso
}

# Configuración de sombras - Sistema de elevación
SOMBRAS = {
    "elevation_1": "0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)",
    "elevation_2": "0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23)",
    "elevation_3": "0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23)",
    "elevation_4": "0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22)",
    "elevation_5": "0 19px 38px rgba(0,0,0,0.30), 0 15px 12px rgba(0,0,0,0.22)",
}

# Configuración de transiciones - Animaciones suaves
TRANSICIONES = {
    "fast": "0.15s ease-in-out",
    "normal": "0.25s ease-in-out",
    "slow": "0.35s ease-in-out",
}

def obtener_color(nombre_color):
    """Obtiene un color del tema."""
    return COLORES_TEMA.get(nombre_color, "#ffffff")

def obtener_fuente(nombre_fuente):
    """Obtiene una configuración de fuente del tema."""
    return FUENTES.get(nombre_fuente, {"size": 14, "weight": "normal", "family": "Segoe UI"})

def obtener_espaciado(nombre_espaciado):
    """Obtiene un valor de espaciado del tema."""
    return ESPACIADO.get(nombre_espaciado, 16)

def obtener_borde(nombre_borde):
    """Obtiene una configuración de borde del tema."""
    return BORDES.get(nombre_borde, 8)

def obtener_sombra(nombre_sombra):
    """Obtiene una configuración de sombra del tema."""
    return SOMBRAS.get(nombre_sombra, "0 1px 3px rgba(0,0,0,0.12)")

def obtener_transicion(nombre_transicion):
    """Obtiene una configuración de transición del tema."""
    return TRANSICIONES.get(nombre_transicion, "0.25s ease-in-out") 