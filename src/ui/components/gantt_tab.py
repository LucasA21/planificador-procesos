"""
Componente para la pestaña del diagrama de Gantt.
"""

import customtkinter as ctk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PestañaGantt(ctk.CTkFrame):
    """Componente para mostrar el diagrama de Gantt."""
    
    def __init__(self, parent, factor_escala=1.0, **kwargs):
        super().__init__(parent, corner_radius=15, fg_color="transparent", **kwargs)
        
        self.factor_escala = factor_escala
        self._crear_widgets()
        self._crear_gantt_ejemplo()
    
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
            text="📈 Diagrama de Gantt - Cronograma de Procesos",
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
        
        # Frame 
        frame_grafico = ctk.CTkFrame(
            main_frame, 
            corner_radius=int(12 * self.factor_escala),
            border_width=1
        )
        frame_grafico.grid(row=1, column=0, sticky="nsew", padx=int(20 * self.factor_escala), pady=(0, int(20 * self.factor_escala)))
        frame_grafico.grid_columnconfigure(0, weight=1)
        frame_grafico.grid_rowconfigure(0, weight=1)
        
        # Crear gráfico de Gantt
        self._crear_grafico_gantt(frame_grafico)
        
        # Configurar grid para que se expanda
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
    
    def _crear_grafico_gantt(self, parent):
        """Crea el gráfico de Gantt."""
        # Crear figura de matplotlib con colores del tema oscuro
        bg_color = "#2b2b2b"
        text_color = "white"
        
        # Tamaño del gráfico escalado
        fig_width = int(10 * self.factor_escala)
        fig_height = int(5 * self.factor_escala)
        
        self.figura_gantt = Figure(figsize=(fig_width, fig_height), dpi=100, facecolor=bg_color)
        self.ax_gantt = self.figura_gantt.add_subplot(111, facecolor=bg_color)
        
        # Configurar estilo del gráfico con colores del tema
        self.ax_gantt.set_title("Diagrama de Gantt - Simulación de Planificación", 
                               color=text_color, fontsize=int(16 * self.factor_escala), fontweight='bold', pad=20)
        self.ax_gantt.set_xlabel("Tiempo (unidades)", color=text_color, fontsize=int(14 * self.factor_escala), fontweight='bold')
        self.ax_gantt.set_ylabel("Procesos", color=text_color, fontsize=int(14 * self.factor_escala), fontweight='bold')
        self.ax_gantt.tick_params(colors=text_color, labelsize=int(12 * self.factor_escala))
        self.ax_gantt.grid(True, alpha=0.2, color="gray")
        
        # Configurar colores de los ejes
        self.ax_gantt.spines['bottom'].set_color("gray")
        self.ax_gantt.spines['top'].set_color("gray")
        self.ax_gantt.spines['left'].set_color("gray")
        self.ax_gantt.spines['right'].set_color("gray")
        
        # Crear canvas
        self.canvas_gantt = FigureCanvasTkAgg(self.figura_gantt, master=parent)
        self.canvas_gantt.draw()
        self.canvas_gantt.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=int(15 * self.factor_escala), pady=int(15 * self.factor_escala))
    
    def _crear_gantt_ejemplo(self):
        """Crea un diagrama de Gantt de ejemplo."""
        # Colores modernos para el ejemplo
        colores_ejemplo = ["#4f9eff", "#4ade80", "#fbbf24"]
        
        # Obtener color de texto
        text_color = "white"
        
        # Datos de ejemplo
        self.ax_gantt.barh(["P1", "P2", "P3"], [3, 2, 4], left=[0, 3, 5], 
                           color=colores_ejemplo, alpha=0.8, edgecolor="gray", linewidth=1)
        
        # Agregar anotaciones de tiempo
        for i, (proceso, inicio, duracion) in enumerate([("P1", 0, 3), ("P2", 3, 2), ("P3", 5, 4)]):
            self.ax_gantt.text(inicio + duracion/2, i, f"{duracion}u", 
                              ha='center', va='center', color=text_color, fontweight='bold')
        
        # Redibujar canvas
        self.canvas_gantt.draw()
    
    def actualizar_gantt(self, procesos, inicios, duraciones):
        """Actualiza el diagrama de Gantt con datos reales."""
        # Limpiar gráfico anterior
        self.ax_gantt.clear()
        
        # Configurar nuevo gráfico
        bg_color = "#2b2b2b"
        text_color = "white"
        
        self.ax_gantt.set_facecolor(bg_color)
        self.ax_gantt.set_title("Diagrama de Gantt - Resultados de la Simulación", 
                               color=text_color, fontsize=int(16 * self.factor_escala), fontweight='bold', pad=20)
        self.ax_gantt.set_xlabel("Tiempo (unidades)", color=text_color, fontsize=int(14 * self.factor_escala), fontweight='bold')
        self.ax_gantt.set_ylabel("Procesos", color=text_color, fontsize=int(14 * self.factor_escala), fontweight='bold')
        self.ax_gantt.tick_params(colors=text_color, labelsize=int(12 * self.factor_escala))
        self.ax_gantt.grid(True, alpha=0.2, color="gray")
        
        # Configurar colores de los ejes
        self.ax_gantt.spines['bottom'].set_color("gray")
        self.ax_gantt.spines['top'].set_color("gray")
        self.ax_gantt.spines['left'].set_color("gray")
        self.ax_gantt.spines['right'].set_color("gray")
        
        # Colores modernos para los procesos
        colores = ["#4f9eff", "#4ade80", "#fbbf24", "#f87171", "#9c27b0"]
        
        # Crear barras del diagrama
        self.ax_gantt.barh(procesos, duraciones, left=inicios, 
                           color=colores[:len(procesos)], alpha=0.8, 
                           edgecolor="gray", linewidth=1)
        
        # Agregar anotaciones de tiempo
        for i, (proceso, inicio, duracion) in enumerate(zip(procesos, inicios, duraciones)):
            self.ax_gantt.text(inicio + duracion/2, i, f"{duracion}u", 
                              ha='center', va='center', color=text_color, fontweight='bold')
        
        # Redibujar canvas
        self.canvas_gantt.draw()
    
    def limpiar_gantt(self):
        """Limpia el diagrama de Gantt."""
        self.ax_gantt.clear()
        self._crear_gantt_ejemplo()
