"""
Componente para la selección de políticas de planificación.
"""

import customtkinter as ctk

class SelectorPoliticas(ctk.CTkFrame):
    """Componente para seleccionar políticas de planificación."""
    
    def __init__(self, parent, factor_escala=1.0, **kwargs):
        super().__init__(parent, corner_radius=15, fg_color="transparent", **kwargs)
        
        self.factor_escala = factor_escala
        self.politica_var = ctk.StringVar(value="FCFS")
        self.callback_cambio_politica = None
        
        # Configurar grid para que ocupe todo el ancho
        self.grid_columnconfigure(0, weight=1)
        
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Frame principal con borde y sombra
        main_frame = ctk.CTkFrame(
            self,
            corner_radius=int(15 * self.factor_escala),
            border_width=1
        )
        main_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Título de sección con icono visual
        titulo_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=int(50 * self.factor_escala))
        titulo_frame.grid(row=0, column=0, sticky="ew", padx=int(20 * self.factor_escala), pady=(int(20 * self.factor_escala), int(20 * self.factor_escala)))
        titulo_frame.grid_columnconfigure(0, weight=1)
        
        titulo = ctk.CTkLabel(
            titulo_frame, 
            text="Política de Planificación",
            font=ctk.CTkFont(size=int(18 * self.factor_escala), weight="bold")
        )
        titulo.grid(row=0, column=0, sticky="w")
        
        self.menu_politica = ctk.CTkComboBox(
            main_frame, 
            variable=self.politica_var,
            values=["FCFS", "Prioridad Externa", "Round Robin", "SPN", "SRTN"],
            width=int(300 * self.factor_escala), 
            height=int(50 * self.factor_escala),  
            corner_radius=int(12 * self.factor_escala),
            font=ctk.CTkFont(size=int(16 * self.factor_escala), weight="bold"),  
            dropdown_font=ctk.CTkFont(size=int(24 * self.factor_escala), weight="normal"),  
            command=self._cambio_politica,
            state="readonly",  
            justify="left" 
        )
        self.menu_politica.grid(row=1, column=0, pady=(0, int(25 * self.factor_escala)), padx=int(20 * self.factor_escala), sticky="ew")
        
        main_frame.grid_columnconfigure(0, weight=1)
    
    def _cambio_politica(self, value):
        """Maneja el cambio de política de planificación."""
        # Notificar cambio de política
        if self.callback_cambio_politica:
            self.callback_cambio_politica(value)
    
    def obtener_politica_seleccionada(self):
        """Retorna la política seleccionada."""
        return self.politica_var.get()
    
    def establecer_callback(self, callback):
        """Establece el callback cuando cambia la política."""
        self.callback_cambio_politica = callback
