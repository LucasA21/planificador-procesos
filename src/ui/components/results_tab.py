"""
Componente para la pestaña de resultados de la simulación.
"""

import customtkinter as ctk
import tkinter as tk

class PestañaResultados(ctk.CTkFrame):
    """Componente para mostrar los resultados de la simulación."""
    
    def __init__(self, parent, factor_escala=1.0, **kwargs):
        super().__init__(parent, corner_radius=15, fg_color="transparent", **kwargs)
        
        self.factor_escala = factor_escala
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Frame principal
        main_frame = ctk.CTkFrame(
            self,
            corner_radius=int(15 * self.factor_escala),
            border_width=0
        )
        main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Título de la pestaña
        titulo_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=int(50 * self.factor_escala))
        titulo_frame.grid(row=0, column=0, sticky="ew", padx=int(20 * self.factor_escala), pady=(int(20 * self.factor_escala), int(15 * self.factor_escala)))
        titulo_frame.grid_columnconfigure(0, weight=1)
        
        titulo = ctk.CTkLabel(
            titulo_frame,
            text="📊 Resultados de la Simulación",
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
        
        # Frame scrollable para el contenido
        self.scrollable_frame = ctk.CTkScrollableFrame(
            main_frame,
            corner_radius=int(12 * self.factor_escala),
            border_width=0
        )
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=int(20 * self.factor_escala), pady=(0, int(20 * self.factor_escala)))
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Configurar grid para que se expanda
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Crear secciones de resultados
        self._crear_seccion_procesos()
        self._crear_seccion_tanda()
        self._crear_seccion_cpu()
    
    def _crear_seccion_procesos(self):
        """Crea la sección de resultados por proceso."""
        # Frame principal de la sección
        seccion_frame = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=int(12 * self.factor_escala),
            border_width=1
        )
        seccion_frame.grid(row=0, column=0, sticky="ew", pady=(0, int(20 * self.factor_escala)))
        seccion_frame.grid_columnconfigure(0, weight=1)
        
        # Título de la sección
        titulo_seccion = ctk.CTkLabel(
            seccion_frame,
            text="📋 Resultados por Proceso",
            font=ctk.CTkFont(size=int(16 * self.factor_escala), weight="bold")
        )
        titulo_seccion.grid(row=0, column=0, pady=(int(20 * self.factor_escala), int(15 * self.factor_escala)), padx=int(20 * self.factor_escala), sticky="w")
        
        # Frame para la tabla de procesos
        tabla_frame = ctk.CTkFrame(
            seccion_frame,
            corner_radius=int(8 * self.factor_escala),
            border_width=1
        )
        tabla_frame.grid(row=1, column=0, sticky="ew", padx=int(20 * self.factor_escala), pady=(0, int(20 * self.factor_escala)))
        tabla_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Encabezados de la tabla
        headers = ["Proceso", "Tiempo de Retorno", "Tiempo de Retorno Normalizado", "Tiempo en Estado de Listo"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                tabla_frame,
                text=header,
                font=ctk.CTkFont(size=int(13 * self.factor_escala), weight="bold"),
                height=int(35 * self.factor_escala),
                anchor="center"
            )
            header_label.grid(row=0, column=i, padx=int(10 * self.factor_escala), pady=int(10 * self.factor_escala), sticky="ew")
        
        # Línea separadora
        separador = ctk.CTkFrame(
            tabla_frame,
            height=int(2 * self.factor_escala),
            corner_radius=int(1 * self.factor_escala)
        )
        separador.grid(row=1, column=0, columnspan=4, sticky="ew", padx=int(10 * self.factor_escala), pady=(0, int(5 * self.factor_escala)))
        
        # Frame para las filas de datos
        self.datos_procesos_frame = ctk.CTkFrame(
            tabla_frame,
            fg_color="transparent"
        )
        self.datos_procesos_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=int(10 * self.factor_escala), pady=(0, int(10 * self.factor_escala)))
        self.datos_procesos_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
    
    def _crear_seccion_tanda(self):
        """Crea la sección de resultados de la tanda."""
        # Frame principal de la sección
        seccion_frame = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=int(12 * self.factor_escala),
            border_width=1
        )
        seccion_frame.grid(row=1, column=0, sticky="ew", pady=(0, int(20 * self.factor_escala)))
        seccion_frame.grid_columnconfigure(0, weight=1)
        seccion_frame.grid_columnconfigure(1, weight=1)
        
        # Título de la sección
        titulo_seccion = ctk.CTkLabel(
            seccion_frame,
            text="🔄 Resultados de la Tanda",
            font=ctk.CTkFont(size=int(16 * self.factor_escala), weight="bold")
        )
        titulo_seccion.grid(row=0, column=0, columnspan=2, pady=(int(20 * self.factor_escala), int(15 * self.factor_escala)), padx=int(20 * self.factor_escala), sticky="w")
        
        # Tiempo de Retorno
        tr_frame = ctk.CTkFrame(
            seccion_frame,
            corner_radius=int(8 * self.factor_escala),
            border_width=1
        )
        tr_frame.grid(row=1, column=0, sticky="ew", padx=(int(20 * self.factor_escala), int(10 * self.factor_escala)), pady=(0, int(20 * self.factor_escala)))
        tr_frame.grid_columnconfigure(0, weight=1)
        
        self.label_tr = ctk.CTkLabel(
            tr_frame,
            text="⏱️ Tiempo de Retorno: --",
            font=ctk.CTkFont(size=int(16 * self.factor_escala), weight="bold"),
            anchor="center"
        )
        self.label_tr.grid(row=0, column=0, pady=int(20 * self.factor_escala), padx=int(15 * self.factor_escala), sticky="ew")
        
        # Tiempo Medio de Retorno
        tmr_frame = ctk.CTkFrame(
            seccion_frame,
            corner_radius=int(8 * self.factor_escala),
            border_width=1
        )
        tmr_frame.grid(row=1, column=1, sticky="ew", padx=(int(10 * self.factor_escala), int(20 * self.factor_escala)), pady=(0, int(20 * self.factor_escala)))
        tmr_frame.grid_columnconfigure(0, weight=1)
        
        self.label_tmr = ctk.CTkLabel(
            tmr_frame,
            text="📈 Tiempo Medio de Retorno: --",
            font=ctk.CTkFont(size=int(16 * self.factor_escala), weight="bold"),
            anchor="center"
        )
        self.label_tmr.grid(row=0, column=0, pady=int(20 * self.factor_escala), padx=int(15 * self.factor_escala), sticky="ew")
    
    def _crear_seccion_cpu(self):
        """Crea la sección de uso de CPU."""
        # Frame principal de la sección
        seccion_frame = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=int(12 * self.factor_escala),
            border_width=1
        )
        seccion_frame.grid(row=2, column=0, sticky="ew", pady=(0, int(20 * self.factor_escala)))
        seccion_frame.grid_columnconfigure(0, weight=1)
        seccion_frame.grid_columnconfigure(1, weight=1)
        seccion_frame.grid_columnconfigure(2, weight=1)
        
        # Título de la sección
        titulo_seccion = ctk.CTkLabel(
            seccion_frame,
            text="💻 Uso de CPU",
            font=ctk.CTkFont(size=int(16 * self.factor_escala), weight="bold")
        )
        titulo_seccion.grid(row=0, column=0, columnspan=3, pady=(int(20 * self.factor_escala), int(15 * self.factor_escala)), padx=int(20 * self.factor_escala), sticky="w")
        
        # CPU Desocupada
        cpu_desocupada_frame = ctk.CTkFrame(
            seccion_frame,
            corner_radius=int(8 * self.factor_escala),
            border_width=1
        )
        cpu_desocupada_frame.grid(row=1, column=0, sticky="ew", padx=(int(20 * self.factor_escala), int(10 * self.factor_escala)), pady=(0, int(20 * self.factor_escala)))
        cpu_desocupada_frame.grid_columnconfigure(0, weight=1)
        
        self.label_cpu_desocupada = ctk.CTkLabel(
            cpu_desocupada_frame,
            text="CPU Desocupada: --",
            font=ctk.CTkFont(size=int(15 * self.factor_escala), weight="bold"),
            anchor="center"
        )
        self.label_cpu_desocupada.grid(row=0, column=0, pady=int(20 * self.factor_escala), padx=int(15 * self.factor_escala), sticky="ew")
        
        # CPU por SO
        cpu_so_frame = ctk.CTkFrame(
            seccion_frame,
            corner_radius=int(8 * self.factor_escala),
            border_width=1
        )
        cpu_so_frame.grid(row=1, column=1, sticky="ew", padx=int(10 * self.factor_escala), pady=(0, int(20 * self.factor_escala)))
        cpu_so_frame.grid_columnconfigure(0, weight=1)
        
        self.label_cpu_so = ctk.CTkLabel(
            cpu_so_frame,
            text="CPU por SO: --",
            font=ctk.CTkFont(size=int(15 * self.factor_escala), weight="bold"),
            anchor="center"
        )
        self.label_cpu_so.grid(row=0, column=0, pady=int(20 * self.factor_escala), padx=int(15 * self.factor_escala), sticky="ew")
        
        # CPU por Procesos
        cpu_procesos_frame = ctk.CTkFrame(
            seccion_frame,
            corner_radius=int(8 * self.factor_escala),
            border_width=1
        )
        cpu_procesos_frame.grid(row=1, column=2, sticky="ew", padx=(int(10 * self.factor_escala), int(20 * self.factor_escala)), pady=(0, int(20 * self.factor_escala)))
        cpu_procesos_frame.grid_columnconfigure(0, weight=1)
        
        self.label_cpu_procesos = ctk.CTkLabel(
            cpu_procesos_frame,
            text="CPU por Procesos: --",
            font=ctk.CTkFont(size=int(15 * self.factor_escala), weight="bold"),
            anchor="center"
        )
        self.label_cpu_procesos.grid(row=0, column=0, pady=int(20 * self.factor_escala), padx=int(15 * self.factor_escala), sticky="ew")
    
    def actualizar_resultados_procesos(self, datos_procesos):
        """Actualiza los resultados por proceso."""
        # Limpiar datos anteriores
        for widget in self.datos_procesos_frame.winfo_children():
            widget.destroy()
        
        # Agregar filas de datos
        for i, proceso in enumerate(datos_procesos):
            # Nombre del proceso
            nombre_label = ctk.CTkLabel(
                self.datos_procesos_frame,
                text=proceso.get('nombre', '--'),
                font=ctk.CTkFont(size=int(12 * self.factor_escala)),
                height=int(30 * self.factor_escala),
                anchor="center"
            )
            nombre_label.grid(row=i, column=0, padx=int(10 * self.factor_escala), pady=int(5 * self.factor_escala), sticky="ew")
            
            # Tiempo de Retorno
            tr_label = ctk.CTkLabel(
                self.datos_procesos_frame,
                text=f"{proceso.get('tiempo_retorno', '--')}",
                font=ctk.CTkFont(size=int(12 * self.factor_escala)),
                height=int(30 * self.factor_escala),
                anchor="center"
            )
            tr_label.grid(row=i, column=1, padx=int(10 * self.factor_escala), pady=int(5 * self.factor_escala), sticky="ew")
            
            # Tiempo de Retorno Normalizado
            trn_label = ctk.CTkLabel(
                self.datos_procesos_frame,
                text=f"{proceso.get('tiempo_retorno_normalizado', '--')}",
                font=ctk.CTkFont(size=int(12 * self.factor_escala)),
                height=int(30 * self.factor_escala),
                anchor="center"
            )
            trn_label.grid(row=i, column=2, padx=int(10 * self.factor_escala), pady=int(5 * self.factor_escala), sticky="ew")
            
            # Tiempo en Estado de Listo
            tel_label = ctk.CTkLabel(
                self.datos_procesos_frame,
                text=f"{proceso.get('tiempo_estado_listo', '--')}",
                font=ctk.CTkFont(size=int(12 * self.factor_escala)),
                height=int(30 * self.factor_escala),
                anchor="center"
            )
            tel_label.grid(row=i, column=3, padx=int(10 * self.factor_escala), pady=int(5 * self.factor_escala), sticky="ew")
    
    def actualizar_resultados_tanda(self, tiempo_retorno, tiempo_medio_retorno):
        """Actualiza los resultados de la tanda."""
        self.label_tr.configure(text=f"⏱️ Tiempo de Retorno: {tiempo_retorno}")
        self.label_tmr.configure(text=f"📈 Tiempo Medio de Retorno: {tiempo_medio_retorno:.2f}")
    
    def actualizar_resultados_cpu(self, desocupada, por_so, por_procesos):
        """Actualiza los resultados de uso de CPU."""
        self.label_cpu_desocupada.configure(text=f"CPU Desocupada: {desocupada}")
        self.label_cpu_so.configure(text=f"CPU por SO: {por_so}")
        self.label_cpu_procesos.configure(text=f"CPU por Procesos: {por_procesos}")
    
    def limpiar_resultados(self):
        """Limpia todos los resultados."""
        # Limpiar datos de procesos
        for widget in self.datos_procesos_frame.winfo_children():
            widget.destroy()
        
        # Limpiar datos de tanda
        self.label_tr.configure(text="⏱️ Tiempo de Retorno: --")
        self.label_tmr.configure(text="📈 Tiempo Medio de Retorno: --")
        
        # Limpiar datos de CPU
        self.label_cpu_desocupada.configure(text="CPU Desocupada: --")
        self.label_cpu_so.configure(text="CPU por SO: --")
        self.label_cpu_procesos.configure(text="CPU por Procesos: --")
    
    def mostrar_mensaje_inicial(self):
        """Muestra un mensaje inicial cuando no hay resultados."""
        # Limpiar datos de procesos
        for widget in self.datos_procesos_frame.winfo_children():
            widget.destroy()
        
        mensaje_label = ctk.CTkLabel(
            self.datos_procesos_frame,
            text="Ejecuta una simulación para ver los resultados",
            font=ctk.CTkFont(size=int(14 * self.factor_escala)),
            text_color="gray"
        )
        mensaje_label.grid(row=0, column=0, columnspan=4, pady=int(20 * self.factor_escala), sticky="ew")
