"""
Componente para la pestaña del diagrama de Gantt.
"""

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PestañaGantt(ctk.CTkFrame):
    """Componente para mostrar el diagrama de Gantt."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        self._crear_widgets()
        self._crear_gantt_ejemplo()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Título de la pestaña
        titulo = ctk.CTkLabel(
            self,
            text="Diagrama de Gantt - Cronograma de Procesos",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(15, 10), padx=15, sticky="w")
        
        # Frame para el gráfico
        frame_grafico = ctk.CTkFrame(self, corner_radius=10)
        frame_grafico.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="nsew")
        frame_grafico.grid_columnconfigure(0, weight=1)
        frame_grafico.grid_rowconfigure(0, weight=1)
        
        # Crear gráfico de Gantt
        self._crear_grafico_gantt(frame_grafico)
        
        # Configurar grid para que se expanda
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
    
    def _crear_grafico_gantt(self, parent):
        """Crea el gráfico de Gantt."""
        # Crear figura de matplotlib
        self.figura_gantt = Figure(figsize=(8, 4), dpi=100, facecolor='#2b2b2b')
        self.ax_gantt = self.figura_gantt.add_subplot(111, facecolor='#2b2b2b')
        
        # Configurar estilo del gráfico
        self.ax_gantt.set_title("Diagrama de Gantt - Simulacion de Planificacion", 
                               color='white', fontsize=14, fontweight='bold')
        self.ax_gantt.set_xlabel("Tiempo (unidades)", color='white', fontsize=12)
        self.ax_gantt.set_ylabel("Procesos", color='white', fontsize=12)
        self.ax_gantt.tick_params(colors='white')
        self.ax_gantt.grid(True, alpha=0.3)
        
        # Crear canvas
        self.canvas_gantt = FigureCanvasTkAgg(self.figura_gantt, master=parent)
        self.canvas_gantt.draw()
        self.canvas_gantt.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    def _crear_gantt_ejemplo(self):
        """Crea un diagrama de Gantt de ejemplo."""
        # Datos de ejemplo
        self.ax_gantt.barh(["P1", "P2", "P3"], [3, 2, 4], left=[0, 3, 5], 
                           color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
        
        # Redibujar canvas
        self.canvas_gantt.draw()
    
    def actualizar_gantt(self, procesos, inicios, duraciones):
        """Actualiza el diagrama de Gantt con datos reales."""
        # Limpiar gráfico anterior
        self.ax_gantt.clear()
        
        # Configurar nuevo gráfico
        self.ax_gantt.set_title("Diagrama de Gantt - Resultados de la Simulacion", 
                               color='white', fontsize=14, fontweight='bold')
        self.ax_gantt.set_xlabel("Tiempo (unidades)", color='white', fontsize=12)
        self.ax_gantt.set_ylabel("Procesos", color='white', fontsize=12)
        self.ax_gantt.tick_params(colors='white')
        self.ax_gantt.grid(True, alpha=0.3)
        
        # Crear barras del diagrama
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        self.ax_gantt.barh(procesos, duraciones, left=inicios, 
                           color=colores[:len(procesos)], alpha=0.8)
        
        # Redibujar canvas
        self.canvas_gantt.draw()
    
    def limpiar_gantt(self):
        """Limpia el diagrama de Gantt."""
        self.ax_gantt.clear()
        self._crear_gantt_ejemplo()
