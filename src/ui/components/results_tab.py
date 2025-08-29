"""
Componente para la pestaña de resultados de la simulación.
"""

import customtkinter as ctk

class PestañaResultados(ctk.CTkFrame):
    """Componente para mostrar los resultados de la simulación."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Título de la pestaña
        titulo = ctk.CTkLabel(
            self,
            text="Log de Eventos de la Simulacion",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(15, 10), padx=15, sticky="w")
        
        # Área de texto para logs
        self.texto_resultados = ctk.CTkTextbox(
            self, 
            width=600, 
            height=400
        )
        self.texto_resultados.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="nsew")
        
        # Configurar grid para que se expanda
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
    
    def agregar_resultado(self, texto):
        """Agrega texto a los resultados."""
        self.texto_resultados.insert("end", texto + "\n")
        self.texto_resultados.see("end")
    
    def limpiar_resultados(self):
        """Limpia todos los resultados."""
        self.texto_resultados.delete("1.0", "end")
    
    def establecer_resultados(self, texto):
        """Establece el contenido completo de los resultados."""
        self.limpiar_resultados()
        self.agregar_resultado(texto)
    
    def obtener_resultados(self):
        """Obtiene el contenido actual de los resultados."""
        return self.texto_resultados.get("1.0", "end-1c")
