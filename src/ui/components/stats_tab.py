"""
Componente para la pestaña de estadísticas de la simulación.
"""

import customtkinter as ctk

class PestañaEstadisticas(ctk.CTkFrame):
    """Componente para mostrar estadísticas de la simulación."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Título de la pestaña
        titulo = ctk.CTkLabel(
            self,
            text="Estadisticas y Metricas de la Simulacion",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(15, 10), padx=15, sticky="w")
        
        # Frame para las estadísticas
        frame_stats = ctk.CTkFrame(self, corner_radius=10)
        frame_stats.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="nsew")
        frame_stats.grid_columnconfigure(0, weight=1)
        frame_stats.grid_columnconfigure(1, weight=1)
        
        # Crear widgets de estadísticas
        self._crear_widgets_estadisticas(frame_stats)
        
        # Configurar grid para que se expanda
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
    
    def _crear_widgets_estadisticas(self, parent):
        """Crea los widgets de estadísticas."""
        # Estadísticas por proceso
        frame_procesos = ctk.CTkFrame(parent, corner_radius=10)
        frame_procesos.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        frame_procesos.grid_columnconfigure(0, weight=1)
        
        titulo_procesos = ctk.CTkLabel(
            frame_procesos,
            text="Por Proceso",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titulo_procesos.grid(row=0, column=0, pady=(15, 10), padx=15, sticky="w")
        
        # Lista de procesos
        self.lista_procesos = ctk.CTkTextbox(frame_procesos, width=300, height=200)
        self.lista_procesos.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="nsew")
        
        # Estadísticas de la tanda
        frame_tanda = ctk.CTkFrame(parent, corner_radius=10)
        frame_tanda.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        frame_tanda.grid_columnconfigure(0, weight=1)
        
        titulo_tanda = ctk.CTkLabel(
            frame_tanda,
            text="Tanda Completa",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titulo_tanda.grid(row=0, column=0, pady=(15, 10), padx=15, sticky="w")
        
        # Métricas de la tanda
        self.label_tr_tanda = ctk.CTkLabel(frame_tanda, text="Tiempo de Retorno: --")
        self.label_tr_tanda.grid(row=1, column=0, pady=5, padx=15, sticky="w")
        
        self.label_tmr_tanda = ctk.CTkLabel(frame_tanda, text="Tiempo Medio de Retorno: --")
        self.label_tmr_tanda.grid(row=2, column=0, pady=5, padx=15, sticky="w")
        
        # Uso de CPU
        frame_cpu = ctk.CTkFrame(parent, corner_radius=10)
        frame_cpu.grid(row=1, column=0, columnspan=2, sticky="ew", padx=0, pady=(10, 0))
        frame_cpu.grid_columnconfigure(0, weight=1)
        
        titulo_cpu = ctk.CTkLabel(
            frame_cpu,
            text="Uso de CPU",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titulo_cpu.grid(row=0, column=0, pady=(15, 10), padx=15, sticky="w")
        
        # Métricas de CPU
        self.label_cpu_desocupada = ctk.CTkLabel(frame_cpu, text="CPU Desocupada: --")
        self.label_cpu_desocupada.grid(row=1, column=0, pady=5, padx=15, sticky="w")
        
        self.label_cpu_so = ctk.CTkLabel(frame_cpu, text="CPU por SO: --")
        self.label_cpu_so.grid(row=2, column=0, pady=5, padx=15, sticky="w")
        
        self.label_cpu_procesos = ctk.CTkLabel(frame_cpu, text="CPU por Procesos: --")
        self.label_cpu_procesos.grid(row=3, column=0, pady=5, padx=15, sticky="w")
    
    def actualizar_estadisticas_proceso(self, texto_estadisticas):
        """Actualiza las estadísticas por proceso."""
        self.lista_procesos.delete("1.0", "end")
        self.lista_procesos.insert("1.0", texto_estadisticas)
    
    def actualizar_estadisticas_tanda(self, tiempo_retorno, tiempo_medio_retorno):
        """Actualiza las estadísticas de la tanda."""
        self.label_tr_tanda.configure(text=f"Tiempo de Retorno: {tiempo_retorno}")
        self.label_tmr_tanda.configure(text=f"Tiempo Medio de Retorno: {tiempo_medio_retorno:.2f}")
    
    def actualizar_estadisticas_cpu(self, desocupada, por_so, por_procesos):
        """Actualiza las estadísticas de uso de CPU."""
        self.label_cpu_desocupada.configure(text=f"CPU Desocupada: {desocupada}")
        self.label_cpu_so.configure(text=f"CPU por SO: {por_so}")
        self.label_cpu_procesos.configure(text=f"CPU por Procesos: {por_procesos}")
    
    def limpiar_estadisticas(self):
        """Limpia todas las estadísticas."""
        self.lista_procesos.delete("1.0", "end")
        self.label_tr_tanda.configure(text="Tiempo de Retorno: --")
        self.label_tmr_tanda.configure(text="Tiempo Medio de Retorno: --")
        self.label_cpu_desocupada.configure(text="CPU Desocupada: --")
        self.label_cpu_so.configure(text="CPU por SO: --")
        self.label_cpu_procesos.configure(text="CPU por Procesos: --")
