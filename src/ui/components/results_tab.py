"""
Componente para la pestaña de resultados de la simulación.
"""

import customtkinter as ctk
import tkinter as tk

class PestañaResultados(ctk.CTkFrame):
    """Componente para mostrar los resultados de la simulación."""
    
    def __init__(self, parent, colores=None, factor_escala=1.0, **kwargs):
        super().__init__(parent, corner_radius=15, fg_color="transparent", **kwargs)
        
        self.colores = colores or {}
        self.factor_escala = factor_escala
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Frame principal con borde y sombra
        main_frame = ctk.CTkFrame(
            self,
            corner_radius=int(15 * self.factor_escala),
            fg_color=self.colores.get("bg_secondary", "#2d2d2d"),
            border_width=0,  # Sin borde para eliminar la línea molesta
            border_color=self.colores.get("border", "#404040")
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
            text="📊 Log de Eventos de la Simulación",
            font=ctk.CTkFont(size=int(18 * self.factor_escala), weight="bold"),
            text_color=self.colores.get("text_primary", "#ffffff")
        )
        titulo.grid(row=0, column=0, sticky="w")
        
        # Línea decorativa
        linea = ctk.CTkFrame(
            titulo_frame,
            height=int(3 * self.factor_escala),
            fg_color=self.colores["border_light"],
            corner_radius=int(2 * self.factor_escala)
        )
        linea.grid(row=1, column=0, pady=(int(8 * self.factor_escala), 0), sticky="ew")
        
        # Frame para el área de texto
        text_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=int(12 * self.factor_escala),
            fg_color=self.colores.get("bg_card", "#3a3a3a"),
            border_width=0,  # Sin borde para eliminar la línea molesta
            border_color=self.colores.get("border", "#404040")
        )
        text_frame.grid(row=1, column=0, sticky="nsew", padx=int(20 * self.factor_escala), pady=(0, int(20 * self.factor_escala)))
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)
        
        # Área de texto para logs con diseño moderno
        self.texto_resultados = ctk.CTkTextbox(
            text_frame, 
            width=600, 
            height=400,
            corner_radius=int(8 * self.factor_escala),
            fg_color=self.colores.get("bg_card", "#3a3a3a"),
            text_color=self.colores.get("text_primary", "#ffffff"),
            font=ctk.CTkFont(size=int(13 * self.factor_escala), family="Consolas"),
            border_width=0
        )
        self.texto_resultados.grid(row=0, column=0, pady=int(15 * self.factor_escala), padx=int(15 * self.factor_escala), sticky="nsew")
        
        # Configurar grid para que se expanda
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
    
    def agregar_resultado(self, texto):
        """Agrega texto a los resultados."""
        # Configurar colores para diferentes tipos de texto
        if texto.startswith("=") or texto.startswith("-"):
            # Separadores
            self.texto_resultados.insert("end", texto + "\n", "separator")
        elif texto.startswith("["):
            # Timestamps
            self.texto_resultados.insert("end", texto + "\n", "timestamp")
        elif texto.startswith("•"):
            # Elementos de lista
            self.texto_resultados.insert("end", texto + "\n", "list_item")
        elif texto.upper() == texto and len(texto) > 10:
            # Títulos en mayúsculas
            self.texto_resultados.insert("end", texto + "\n", "title")
        else:
            # Texto normal
            self.texto_resultados.insert("end", texto + "\n", "normal")
        
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
    
    def configurar_tags(self):
        """Configura los tags de color para el texto."""
        # Configurar colores para diferentes tipos de texto
        self.texto_resultados.tag_config("normal", foreground=self.colores.get("text_primary", "#ffffff"))
        self.texto_resultados.tag_config("title", foreground=self.colores.get("accent", "#4f9eff"))
        self.texto_resultados.tag_config("separator", foreground=self.colores.get("accent", "#4f9eff"))
        self.texto_resultados.tag_config("timestamp", foreground=self.colores.get("success", "#4ade80"))
        self.texto_resultados.tag_config("list_item", foreground=self.colores.get("text_secondary", "#b3b3b3"))
