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
        self.ruta_pdf_actual = None
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
        
        # Frame principal para la tabla con scroll
        self.scrollable_tabla = ctk.CTkScrollableFrame(
            seccion_frame,
            corner_radius=int(8 * self.factor_escala),
            border_width=1,
            height=int(300 * self.factor_escala)
        )
        self.scrollable_tabla.grid(row=1, column=0, sticky="nsew", padx=int(20 * self.factor_escala), pady=(0, int(20 * self.factor_escala)))
        self.scrollable_tabla.grid_columnconfigure(0, weight=1)
        
        # Frame interno para la tabla
        self.tabla_frame = ctk.CTkFrame(
            self.scrollable_tabla,
            fg_color="transparent",
            corner_radius=0
        )
        self.tabla_frame.grid(row=0, column=0, sticky="nsew")
        
        self.tabla_frame.grid_columnconfigure(0, weight=1, minsize=int(120 * self.factor_escala)) 
        self.tabla_frame.grid_columnconfigure(1, weight=1, minsize=int(120 * self.factor_escala)) 
        self.tabla_frame.grid_columnconfigure(2, weight=1, minsize=int(120 * self.factor_escala))  
        self.tabla_frame.grid_columnconfigure(3, weight=1, minsize=int(120 * self.factor_escala))  
        
        # Frame para todas las filas (encabezados + datos)
        self.tabla_datos_frame = ctk.CTkFrame(
            self.tabla_frame,
            fg_color="transparent"
        )
        self.tabla_datos_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        
        # Configurar anchos fijos para las columnas de datos (igual que la tabla principal)
        self.tabla_datos_frame.grid_columnconfigure(0, weight=1, minsize=int(120 * self.factor_escala)) 
        self.tabla_datos_frame.grid_columnconfigure(1, weight=1, minsize=int(120 * self.factor_escala)) 
        self.tabla_datos_frame.grid_columnconfigure(2, weight=1, minsize=int(120 * self.factor_escala))  
        self.tabla_datos_frame.grid_columnconfigure(3, weight=1, minsize=int(120 * self.factor_escala))  
    
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
        
        # Contenedor separado para el botón de PDF
        self.pdf_frame = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=int(12 * self.factor_escala),
            border_width=1
        )
        self.pdf_frame.grid(row=3, column=0, sticky="ew", pady=(0, int(20 * self.factor_escala)))
        self.pdf_frame.grid_columnconfigure(0, weight=1)
        
        # Botón para abrir PDF (inicialmente oculto)
        self.boton_abrir_pdf = ctk.CTkButton(
            self.pdf_frame,
            text="Resultados de la simulacion",
            command=self._abrir_pdf,
            font=ctk.CTkFont(size=int(14 * self.factor_escala), weight="bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            height=int(35 * self.factor_escala),
            width=int(120 * self.factor_escala)
        )
        self.boton_abrir_pdf.grid(row=0, column=0, pady=int(20 * self.factor_escala), padx=int(20 * self.factor_escala), sticky="ew")
        self.pdf_frame.grid_remove()  # Ocultar inicialmente
    
    def actualizar_resultados_procesos(self, datos_procesos):
        """Actualiza los resultados por proceso."""
        # Limpiar datos anteriores
        for widget in self.tabla_datos_frame.winfo_children():
            widget.destroy()
        
        # Crear encabezados como primera fila (títulos más cortos)
        headers = ["Proceso", "Tiempo Retorno", "Tr.Normalizado", "Tiempo Listo"]
        self._crear_fila_tabla(0, headers, "#404040", True)  # Color gris para encabezados
        
        # Agregar filas de datos
        for i, proceso in enumerate(datos_procesos):
            # Color alternado para las filas de datos
            row_color = "#2b2b2b" if i % 2 == 0 else "#333333"
            
            # Datos de la fila
            datos_fila = [
                proceso.get('nombre', '--'),
                str(proceso.get('tiempo_retorno', '--')),
                f"{proceso.get('tiempo_retorno_normalizado', '--'):.2f}" if proceso.get('tiempo_retorno_normalizado', '--') != '--' else '--',
                str(proceso.get('tiempo_estado_listo', '--'))
            ]
            
            self._crear_fila_tabla(i + 1, datos_fila, row_color, False)
    
    def _crear_fila_tabla(self, row_index, datos_fila, color_fondo, es_encabezado=False):
        """Crea una fila de la tabla con el estilo apropiado."""
        # Crear frame para la fila completa
        row_frame = ctk.CTkFrame(
            self.tabla_datos_frame,
            fg_color=color_fondo,
            corner_radius=int(4 * self.factor_escala),
            border_width=1,
            border_color="#555555"
        )
        row_frame.grid(row=row_index, column=0, columnspan=4, sticky="ew", padx=int(1 * self.factor_escala), pady=int(1 * self.factor_escala))
        
        # Configurar anchos fijos para las columnas de la fila
        row_frame.grid_columnconfigure(0, weight=1, minsize=int(120 * self.factor_escala))  
        row_frame.grid_columnconfigure(1, weight=1, minsize=int(120 * self.factor_escala))  
        row_frame.grid_columnconfigure(2, weight=1, minsize=int(120 * self.factor_escala))  
        row_frame.grid_columnconfigure(3, weight=1, minsize=int(120 * self.factor_escala)) 
        
        # Crear celdas para cada columna
        for j, valor in enumerate(datos_fila):
            # Configurar fuente según si es encabezado o no
            if es_encabezado:
                font = ctk.CTkFont(size=int(13 * self.factor_escala), weight="bold")
                height = int(35 * self.factor_escala)
                padx = int(8 * self.factor_escala)  # Padding uniforme para encabezados
            else:
                font = ctk.CTkFont(size=int(12 * self.factor_escala))
                height = int(35 * self.factor_escala)
                padx = int(8 * self.factor_escala)  # Padding uniforme para datos
            
            cell_label = ctk.CTkLabel(
                row_frame,
                text=valor,
                font=font,
                height=height,
                anchor="center",
                justify="center",
                fg_color="transparent"
            )
            cell_label.grid(row=0, column=j, sticky="ew", padx=padx, pady=int(6 * self.factor_escala))
    
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
        for widget in self.tabla_datos_frame.winfo_children():
            widget.destroy()
        
        # Limpiar datos de tanda
        self.label_tr.configure(text="⏱️ Tiempo de Retorno: --")
        self.label_tmr.configure(text="📈 Tiempo Medio de Retorno: --")
        
        # Limpiar datos de CPU
        self.label_cpu_desocupada.configure(text="CPU Desocupada: --")
        self.label_cpu_so.configure(text="CPU por SO: --")
        self.label_cpu_procesos.configure(text="CPU por Procesos: --")
        
        # Ocultar contenedor de PDF
        self.pdf_frame.grid_remove()
        self.ruta_pdf_actual = None
    
    def mostrar_mensaje_inicial(self):
        """Muestra un mensaje inicial cuando no hay resultados."""
        # Limpiar datos de procesos
        for widget in self.tabla_datos_frame.winfo_children():
            widget.destroy()
        
        # Crear frame para el mensaje
        mensaje_frame = ctk.CTkFrame(
            self.tabla_datos_frame,
            fg_color="#2b2b2b",
            corner_radius=int(8 * self.factor_escala),
            border_width=1,
            border_color="#555555"
        )
        mensaje_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=int(2 * self.factor_escala), pady=int(10 * self.factor_escala))
        mensaje_frame.grid_columnconfigure(0, weight=1)
        
        mensaje_label = ctk.CTkLabel(
            mensaje_frame,
            text="Ejecuta una simulación para ver los resultados",
            font=ctk.CTkFont(size=int(14 * self.factor_escala)),
            text_color="gray",
            fg_color="transparent"
        )
        mensaje_label.grid(row=0, column=0, pady=int(20 * self.factor_escala), sticky="ew")
    
    def _abrir_pdf(self):
        """Abre el PDF actual."""
        if not self.ruta_pdf_actual:
            print("Error: No hay ruta de PDF configurada")
            return
            
        import os
        import subprocess
        import platform
        
        # Convertir a ruta absoluta y verificar que existe
        ruta_absoluta = os.path.abspath(self.ruta_pdf_actual)
        print(f"Intentando abrir PDF: {ruta_absoluta}")
        
        if not os.path.exists(ruta_absoluta):
            print(f"Error: El archivo PDF no existe en {ruta_absoluta}")
            # Intentar buscar en el directorio actual
            directorio_actual = os.getcwd()
            print(f"Directorio actual: {directorio_actual}")
            
            # Buscar archivos PDF en el directorio actual y subdirectorios
            for root, dirs, files in os.walk(directorio_actual):
                for file in files:
                    if file.endswith('.pdf') and 'reporte_simulacion' in file:
                        ruta_encontrada = os.path.join(root, file)
                        print(f"PDF encontrado: {ruta_encontrada}")
                        ruta_absoluta = ruta_encontrada
                        break
                if ruta_absoluta != self.ruta_pdf_actual:
                    break
            
            if not os.path.exists(ruta_absoluta):
                print("No se encontró ningún PDF de simulación")
                return
        
        try:
            sistema = platform.system()
            print(f"Sistema operativo detectado: {sistema}")
            
            if sistema == "Windows":
                print("Usando os.startfile para Windows")
                os.startfile(ruta_absoluta)
            elif sistema == "Darwin":  # macOS
                print("Usando comando 'open' para macOS")
                subprocess.run(["open", ruta_absoluta], check=True)
            else:  # Linux
                print("Usando comando 'xdg-open' para Linux")
                # Intentar diferentes comandos para abrir PDF en Linux
                comandos = ["xdg-open", "evince", "okular", "firefox", "google-chrome", "chromium-browser"]
                
                for comando in comandos:
                    try:
                        print(f"Intentando con: {comando}")
                        subprocess.run([comando, ruta_absoluta], check=True, timeout=5)
                        print(f"PDF abierto exitosamente con {comando}")
                        return
                    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                        print(f"Comando {comando} falló, probando siguiente...")
                        continue
                
                print("Error: No se pudo abrir el PDF con ningún comando disponible")
                
        except Exception as e:
            print(f"Error al abrir el PDF: {e}")
            import traceback
            traceback.print_exc()
    
    def mostrar_notificacion_pdf(self, ruta_pdf):
        """Muestra el botón para abrir el PDF."""
        self.ruta_pdf_actual = ruta_pdf
        self.pdf_frame.grid()  # Mostrar el contenedor del botón
    
    def actualizar_escalado(self, nuevo_factor_escala):
        """Actualiza el escalado del componente dinámicamente."""
        self.factor_escala = nuevo_factor_escala
        
        # Actualizar elementos principales
        if hasattr(self, 'label_tr'):
            self.label_tr.configure(
                font=ctk.CTkFont(size=int(15 * self.factor_escala), weight="bold")
            )
        
        if hasattr(self, 'label_tmr'):
            self.label_tmr.configure(
                font=ctk.CTkFont(size=int(15 * self.factor_escala), weight="bold")
            )
        
        if hasattr(self, 'label_cpu_desocupada'):
            self.label_cpu_desocupada.configure(
                font=ctk.CTkFont(size=int(15 * self.factor_escala), weight="bold")
            )
        
        if hasattr(self, 'label_cpu_so'):
            self.label_cpu_so.configure(
                font=ctk.CTkFont(size=int(15 * self.factor_escala), weight="bold")
            )
        
        if hasattr(self, 'label_cpu_procesos'):
            self.label_cpu_procesos.configure(
                font=ctk.CTkFont(size=int(15 * self.factor_escala), weight="bold")
            )
        
        # Actualizar altura del scrollable frame
        if hasattr(self, 'scrollable_tabla'):
            self.scrollable_tabla.configure(height=int(300 * self.factor_escala))