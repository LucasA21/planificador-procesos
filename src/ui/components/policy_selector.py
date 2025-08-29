"""
Componente para la selección de políticas de planificación.
"""

import customtkinter as ctk

class SelectorPoliticas(ctk.CTkFrame):
    """Componente para seleccionar políticas de planificación."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        self.politica_var = ctk.StringVar(value="FCFS")
        self.callback_cambio_politica = None
        
        # Configurar descripciones primero
        self._configurar_descripciones()
        # Luego crear widgets
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Título de sección
        titulo = ctk.CTkLabel(
            self, 
            text="POLITICA DE PLANIFICACION", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(15, 15), padx=15)
        
        # Selector de política
        self.menu_politica = ctk.CTkOptionMenu(
            self, 
            variable=self.politica_var,
            values=["FCFS", "Prioridad Externa", "Round Robin", "SPN", "SRTN"],
            height=35,
            command=self._cambio_politica
        )
        self.menu_politica.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="ew")
        
        # Descripción de la política seleccionada
        self.label_descripcion = ctk.CTkLabel(
            self,
            text="",
            text_color="lightblue",
            wraplength=250
        )
        self.label_descripcion.grid(row=2, column=0, pady=(0, 15), padx=15)
        
        # Actualizar descripción inicial
        self._actualizar_descripcion("FCFS")
    
    def _configurar_descripciones(self):
        """Configura las descripciones de cada política."""
        self.descripciones = {
            "FCFS": "FCFS: First Come First Served - Procesos se ejecutan en orden de llegada",
            "Prioridad Externa": "Prioridad Externa: Se ejecuta el proceso con mayor prioridad",
            "Round Robin": "Round Robin: Cada proceso ejecuta por un quantum fijo",
            "SPN": "SPN: Shortest Process Next - Se ejecuta el proceso con menor tiempo total",
            "SRTN": "SRTN: Shortest Remaining Time Next - Se ejecuta el proceso con menor tiempo restante"
        }
    
    def _cambio_politica(self, value):
        """Maneja el cambio de política de planificación."""
        self._actualizar_descripcion(value)
        
        # Notificar cambio de política
        if self.callback_cambio_politica:
            self.callback_cambio_politica(value)
    
    def _actualizar_descripcion(self, politica):
        """Actualiza la descripción de la política seleccionada."""
        descripcion = self.descripciones.get(politica, "")
        self.label_descripcion.configure(text=descripcion)
    
    def obtener_politica_seleccionada(self):
        """Retorna la política seleccionada."""
        return self.politica_var.get()
    
    def establecer_callback(self, callback):
        """Establece el callback cuando cambia la política."""
        self.callback_cambio_politica = callback
