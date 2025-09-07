"""
Componente para la pestaña de estadísticas de la simulación.
"""

import customtkinter as ctk
import tkinter as tk

class PestañaEstadisticas(ctk.CTkFrame):
    """Componente para mostrar estadísticas de la simulación."""
    
    def __init__(self, parent, factor_escala=1.0, **kwargs):
        super().__init__(parent, corner_radius=15, fg_color="transparent", **kwargs)
        
        self.factor_escala = factor_escala
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Frame principal con borde y sombra
        main_frame = ctk.CTkFrame(
            self,
            corner_radius=int(15 * self.factor_escala),
            border_width=1
        )
        main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Título de la pestaña con icono visual
        titulo_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=int(50 * self.factor_escala))
        titulo_frame.grid(row=0, column=0, sticky="ew", padx=int(20 * self.factor_escala), pady=(int(20 * self.factor_escala), int(15 * self.factor_escala)))
        titulo_frame.grid_columnconfigure(0, weight=1)
        
        titulo = ctk.CTkLabel(
            titulo_frame,
            text="📊 Estadísticas y Métricas de la Simulación",
            font=ctk.CTkFont(size=int(18 * self.factor_escala), weight="bold")
        )
        titulo.grid(row=0, column=0, sticky="w")
        
        # Línea decorativa
        linea = ctk.CTkFrame(
            titulo_frame,
            height=int(3 * self.factor_escala),
            corner_radius=int(2 * self.factor_escala)
        )
        linea.grid(row=1, column=0, pady=(int(8 * self.factor_escala), 0), sticky="ew")
        
        # Frame para las estadísticas
        frame_stats = ctk.CTkFrame(
            main_frame, 
            corner_radius=int(12 * self.factor_escala),
            border_width=1
        )
        frame_stats.grid(row=1, column=0, sticky="nsew", padx=int(20 * self.factor_escala), pady=(0, int(20 * self.factor_escala)))
        frame_stats.grid_columnconfigure(0, weight=1)
        frame_stats.grid_columnconfigure(1, weight=1)
        
        # Crear widgets de estadísticas
        self._crear_widgets_estadisticas(frame_stats)
        
        # Configurar grid para que se expanda
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
    
    def _crear_widgets_estadisticas(self, parent):
        """Crea los widgets de estadísticas."""
        # Estadísticas por proceso
        frame_procesos = ctk.CTkFrame(
            parent, 
            corner_radius=int(10 * self.factor_escala),
            border_width=1
        )
        frame_procesos.grid(row=0, column=0, sticky="nsew", padx=(0, int(10 * self.factor_escala)), pady=int(10 * self.factor_escala))
        frame_procesos.grid_columnconfigure(0, weight=1)
        frame_procesos.grid_rowconfigure(1, weight=1)
        
        titulo_procesos = ctk.CTkLabel(
            frame_procesos,
            text="📋 Por Proceso",
            font=ctk.CTkFont(size=int(15 * self.factor_escala), weight="bold")
        )
        titulo_procesos.grid(row=0, column=0, pady=(int(15 * self.factor_escala), int(10 * self.factor_escala)), padx=int(15 * self.factor_escala), sticky="w")
        
        # Lista de procesos con diseño moderno
        self.lista_procesos = ctk.CTkTextbox(
            frame_procesos, 
            width=300, 
            height=200,
            corner_radius=int(8 * self.factor_escala),
            font=ctk.CTkFont(size=int(13 * self.factor_escala), family="Consolas"),
            border_width=0
        )
        self.lista_procesos.grid(row=1, column=0, pady=(0, int(15 * self.factor_escala)), padx=int(15 * self.factor_escala), sticky="nsew")
        
        # Estadísticas de la tanda
        frame_tanda = ctk.CTkFrame(
            parent, 
            corner_radius=int(10 * self.factor_escala),
            border_width=1
        )
        frame_tanda.grid(row=0, column=1, sticky="nsew", padx=(int(10 * self.factor_escala), 0), pady=int(10 * self.factor_escala))
        frame_tanda.grid_columnconfigure(0, weight=1)
        
        titulo_tanda = ctk.CTkLabel(
            frame_tanda,
            text="🔄 Tanda Completa",
            font=ctk.CTkFont(size=int(15 * self.factor_escala), weight="bold")
        )
        titulo_tanda.grid(row=0, column=0, pady=(int(15 * self.factor_escala), int(10 * self.factor_escala)), padx=int(15 * self.factor_escala), sticky="w")
        
        # Métricas de la tanda con diseño moderno
        self.label_tr_tanda = ctk.CTkLabel(
            frame_tanda, 
            text="⏱️ Tiempo de Retorno: --",
            font=ctk.CTkFont(size=int(13 * self.factor_escala))
        )
        self.label_tr_tanda.grid(row=1, column=0, pady=int(8 * self.factor_escala), padx=int(15 * self.factor_escala), sticky="w")
        
        self.label_tmr_tanda = ctk.CTkLabel(
            frame_tanda, 
            text="📈 Tiempo Medio de Retorno: --",
            font=ctk.CTkFont(size=int(13 * self.factor_escala))
        )
        self.label_tmr_tanda.grid(row=2, column=0, pady=int(8 * self.factor_escala), padx=int(15 * self.factor_escala), sticky="w")
        
        # Uso de CPU
        frame_cpu = ctk.CTkFrame(
            parent, 
            corner_radius=int(10 * self.factor_escala),
            border_width=1
        )
        frame_cpu.grid(row=1, column=0, columnspan=2, sticky="ew", padx=0, pady=(int(10 * self.factor_escala), 0))
        frame_cpu.grid_columnconfigure(0, weight=1)
        
        titulo_cpu = ctk.CTkLabel(
            frame_cpu,
            text="💻 Uso de CPU",
            font=ctk.CTkFont(size=int(15 * self.factor_escala), weight="bold")
        )
        titulo_cpu.grid(row=0, column=0, pady=(int(15 * self.factor_escala), int(10 * self.factor_escala)), padx=int(15 * self.factor_escala), sticky="w")
        
        # Métricas de CPU con diseño moderno
        self.label_cpu_desocupada = ctk.CTkLabel(
            frame_cpu, 
            text="🟢 CPU Desocupada: --",
            font=ctk.CTkFont(size=int(13 * self.factor_escala))
        )
        self.label_cpu_desocupada.grid(row=1, column=0, pady=int(8 * self.factor_escala), padx=int(15 * self.factor_escala), sticky="w")
        
        self.label_cpu_so = ctk.CTkLabel(
            frame_cpu, 
            text="🔧 CPU por SO: --",
            font=ctk.CTkFont(size=int(13 * self.factor_escala))
        )
        self.label_cpu_so.grid(row=2, column=0, pady=int(8 * self.factor_escala), padx=int(15 * self.factor_escala), sticky="w")
        
        self.label_cpu_procesos = ctk.CTkLabel(
            frame_cpu, 
            text="⚡ CPU por Procesos: --",
            font=ctk.CTkFont(size=int(13 * self.factor_escala))
        )
        self.label_cpu_procesos.grid(row=3, column=0, pady=int(8 * self.factor_escala), padx=int(15 * self.factor_escala), sticky="w")
    
    def actualizar_estadisticas_proceso(self, texto_estadisticas):
        """Actualiza las estadísticas por proceso."""
        self.lista_procesos.delete("1.0", "end")
        self.lista_procesos.insert("1.0", texto_estadisticas)
    
    def actualizar_estadisticas_tanda(self, tiempo_retorno, tiempo_medio_retorno):
        """Actualiza las estadísticas de la tanda."""
        self.label_tr_tanda.configure(text=f"⏱️ Tiempo de Retorno: {tiempo_retorno}")
        self.label_tmr_tanda.configure(text=f"📈 Tiempo Medio de Retorno: {tiempo_medio_retorno:.2f}")
    
    def actualizar_estadisticas_cpu(self, desocupada, por_so, por_procesos):
        """Actualiza las estadísticas de uso de CPU."""
        self.label_cpu_desocupada.configure(text=f"🟢 CPU Desocupada: {desocupada}")
        self.label_cpu_so.configure(text=f"🔧 CPU por SO: {por_so}")
        self.label_cpu_procesos.configure(text=f"⚡ CPU por Procesos: {por_procesos}")
    
    def limpiar_estadisticas(self):
        """Limpia todas las estadísticas."""
        self.lista_procesos.delete("1.0", "end")
        self.label_tr_tanda.configure(text="⏱️ Tiempo de Retorno: --")
        self.label_tmr_tanda.configure(text="📈 Tiempo Medio de Retorno: --")
        self.label_cpu_desocupada.configure(text="🟢 CPU Desocupada: --")
        self.label_cpu_so.configure(text="🔧 CPU por SO: --")
        self.label_cpu_procesos.configure(text="⚡ CPU por Procesos: --")
