import customtkinter as ctk
from src.ui.main_window import VentanaPrincipal

def main():
    """Función principal de la aplicación."""
    # Configuración inicial de CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Crear y ejecutar la ventana principal
    app = VentanaPrincipal()
    app.mainloop()

if __name__ == "__main__":
    main()
