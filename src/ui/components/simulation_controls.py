"""
Componente para los controles de simulación.
"""

import customtkinter as ctk

class ControlesSimulacion(ctk.CTkFrame):
    """Componente para los controles de simulación."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        self.callback_simular = None
        self.callback_limpiar = None
        
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Título de sección
        titulo = ctk.CTkLabel(
            self, 
            text="CONTROLES", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(15, 15), padx=15)
        
        # Botón para ejecutar simulación
        self.boton_simular = ctk.CTkButton(
            self, 
            text="EJECUTAR SIMULACION", 
            command=self._simular,
            height=40,
            fg_color="green",
            hover_color="darkgreen",
            state="disabled"
        )
        self.boton_simular.grid(row=1, column=0, pady=(0, 10), padx=15, sticky="ew")
        
        # Botón para limpiar resultados
        self.boton_limpiar = ctk.CTkButton(
            self,
            text="Limpiar Resultados",
            command=self._limpiar_resultados,
            height=30,
            fg_color="red",
            hover_color="darkred"
        )
        self.boton_limpiar.grid(row=2, column=0, pady=(0, 15), padx=15, sticky="ew")
    
    def _simular(self):
        """Ejecuta la simulación."""
        if self.callback_simular:
            self.callback_simular()
    
    def _limpiar_resultados(self):
        """Limpia los resultados."""
        if self.callback_limpiar:
            self.callback_limpiar()
    
    def habilitar_simulacion(self, habilitar=True):
        """Habilita o deshabilita el botón de simulación."""
        estado = "normal" if habilitar else "disabled"
        self.boton_simular.configure(state=estado)
    
    def establecer_callback_simulacion(self, callback):
        """Establece el callback para la simulación."""
        self.callback_simular = callback
    
    def establecer_callback_limpiar(self, callback):
        """Establece el callback para limpiar resultados."""
        self.callback_limpiar = callback
