"""
Componente para la carga de archivos de procesos.
"""

import customtkinter as ctk
import tkinter.filedialog as fd

class CargadorArchivos(ctk.CTkFrame):
    """Componente para cargar archivos de procesos."""
    
    def __init__(self, parent, colores=None, factor_escala=1.0, **kwargs):
        super().__init__(parent, corner_radius=15, fg_color="transparent", **kwargs)
        
        self.colores = colores or {}
        self.factor_escala = factor_escala
        self.archivo_cargado = None
        self.procesos_cargados = []
        self.callback_archivo_cargado = None
        
        # Configurar grid para que ocupe todo el ancho
        self.grid_columnconfigure(0, weight=1)
        
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Frame principal con borde y sombra
        main_frame = ctk.CTkFrame(
            self,
            corner_radius=int(15 * self.factor_escala),
            fg_color=self.colores.get("bg_secondary", "#2d2d2d"),
            border_width=1,
            border_color=self.colores.get("border", "#404040")
        )
        main_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Título de sección con icono visual
        titulo_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=int(40 * self.factor_escala))
        titulo_frame.grid(row=0, column=0, sticky="ew", padx=int(20 * self.factor_escala), pady=(int(20 * self.factor_escala), int(15 * self.factor_escala)))
        titulo_frame.grid_columnconfigure(0, weight=1)
        
        titulo = ctk.CTkLabel(
            titulo_frame, 
            text="Archivo de Procesos",
            font=ctk.CTkFont(size=int(16 * self.factor_escala), weight="bold"),
            text_color=self.colores.get("text_primary", "#ffffff")
        )
        titulo.grid(row=0, column=0, sticky="w")
        
        # Botón para cargar archivo con diseño moderno
        self.boton_cargar = ctk.CTkButton(
            main_frame, 
            text="Seleccionar Archivo",
            command=self._cargar_archivo,
            height=int(45 * self.factor_escala),
            corner_radius=int(12 * self.factor_escala),
            fg_color=self.colores.get("accent", "#4f9eff"),
            hover_color=self.colores.get("accent_hover", "#3d7fd9"),
            font=ctk.CTkFont(size=int(14 * self.factor_escala), weight="bold"),
            border_width=0
        )
        self.boton_cargar.grid(row=1, column=0, pady=(0, int(15 * self.factor_escala)), padx=int(20 * self.factor_escala), sticky="ew")
        
        # Frame para mostrar información del archivo
        info_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=int(10 * self.factor_escala),
            fg_color=self.colores.get("bg_card", "#3a3a3a"),
            border_width=1,
            border_color=self.colores.get("border", "#404040")
        )
        info_frame.grid(row=2, column=0, sticky="ew", padx=int(20 * self.factor_escala), pady=(0, int(20 * self.factor_escala)))
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Label para mostrar archivo seleccionado
        self.label_archivo = ctk.CTkLabel(
            info_frame,
            text="Ningún archivo seleccionado",
            text_color=self.colores.get("text_muted", "#808080"),
            font=ctk.CTkFont(size=int(13 * self.factor_escala)),
            height=int(35 * self.factor_escala)
        )
        self.label_archivo.grid(row=0, column=0, pady=int(10 * self.factor_escala), padx=int(15 * self.factor_escala))
        
        # Indicador de estado
        self.indicator = ctk.CTkFrame(
            info_frame,
            width=int(8 * self.factor_escala),
            height=int(8 * self.factor_escala),
            corner_radius=int(4 * self.factor_escala),
            fg_color=self.colores.get("text_muted", "#808080")
        )
        self.indicator.grid(row=0, column=1, pady=int(10 * self.factor_escala), padx=(0, int(15 * self.factor_escala)), sticky="e")
    
    def _cargar_archivo(self):
        """Carga el archivo de procesos."""
        ruta = fd.askopenfilename(
            title="Selecciona archivo de procesos", 
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if ruta:
            try:
                self.archivo_cargado = ruta
                nombre_archivo = ruta.split('/')[-1]
                
                # Leer y parsear el archivo
                self._leer_archivo_procesos(ruta)
                
                # Actualizar interfaz con éxito
                self.label_archivo.configure(
                    text=f"✓ {nombre_archivo}",
                    text_color=self.colores.get("success", "#4ade80"),
                    font=ctk.CTkFont(size=int(13 * self.factor_escala), weight="bold")
                )
                
                # Cambiar indicador a verde
                self.indicator.configure(fg_color=self.colores.get("success", "#4ade80"))
                
                # Mantener el color azul del botón
                # No cambiar el color del botón
                
                # Notificar que se cargó un archivo
                if self.callback_archivo_cargado:
                    self.callback_archivo_cargado(self.procesos_cargados)
                    
            except Exception as e:
                # Actualizar interfaz con error
                self.label_archivo.configure(
                    text=f"✗ Error al cargar archivo",
                    text_color=self.colores.get("error", "#f87171"),
                    font=ctk.CTkFont(size=int(13 * self.factor_escala), weight="bold")
                )
                
                # Cambiar indicador a rojo
                self.indicator.configure(fg_color=self.colores.get("error", "#f87171"))
                
                # Restaurar botón
                self.boton_cargar.configure(
                    fg_color=self.colores.get("accent", "#4f9eff"),
                    hover_color=self.colores.get("accent_hover", "#3d7fd9")
                )
    
    def _leer_archivo_procesos(self, ruta):
        """Lee y parsea el archivo de procesos."""
        try:
            with open(ruta, 'r') as archivo:
                lineas = archivo.readlines()
            
            self.procesos_cargados = []
            for linea in lineas:
                linea = linea.strip()
                if linea and not linea.startswith('#'):
                    campos = linea.split(',')
                    if len(campos) == 6:
                        proceso = {
                            'nombre': campos[0].strip(),
                            'tiempo_arribo': int(campos[1].strip()),
                            'rafagas_cpu': int(campos[2].strip()),
                            'duracion_rafaga_cpu': int(campos[3].strip()),
                            'duracion_rafaga_io': int(campos[4].strip()),
                            'prioridad': int(campos[5].strip())
                        }
                        self.procesos_cargados.append(proceso)
            
        except Exception as e:
            raise Exception(f"Error al leer archivo: {str(e)}")
    
    def obtener_procesos(self):
        """Retorna los procesos cargados."""
        return self.procesos_cargados
    
    def establecer_callback(self, callback):
        """Establece el callback cuando se carga un archivo."""
        self.callback_archivo_cargado = callback
