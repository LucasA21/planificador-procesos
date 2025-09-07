
"""
Componente para la carga de archivos de procesos.
"""

import customtkinter as ctk
import tkinter.filedialog as fd
import json

class CargadorArchivos(ctk.CTkFrame):
    """Componente para cargar archivos de procesos."""
    
    def __init__(self, parent, factor_escala=1.0, **kwargs):
        super().__init__(parent, corner_radius=15, fg_color="transparent", **kwargs)
        
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
            border_width=1
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
            font=ctk.CTkFont(size=int(16 * self.factor_escala), weight="bold")
        )
        titulo.grid(row=0, column=0, sticky="w")
        
        # Botón para cargar archivo con diseño moderno
        self.boton_cargar = ctk.CTkButton(
            main_frame, 
            text="Seleccionar Archivo",
            command=self._cargar_archivo,
            height=int(45 * self.factor_escala),
            corner_radius=int(12 * self.factor_escala),
            font=ctk.CTkFont(size=int(14 * self.factor_escala), weight="bold"),
            border_width=0
        )
        self.boton_cargar.grid(row=1, column=0, pady=(0, int(15 * self.factor_escala)), padx=int(20 * self.factor_escala), sticky="ew")
        
        # Frame para mostrar información del archivo
        info_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=int(10 * self.factor_escala),
            border_width=1
        )
        info_frame.grid(row=2, column=0, sticky="ew", padx=int(20 * self.factor_escala), pady=(0, int(20 * self.factor_escala)))
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Label para mostrar archivo seleccionado
        self.label_archivo = ctk.CTkLabel(
            info_frame,
            text="Ningún archivo seleccionado",
            font=ctk.CTkFont(size=int(13 * self.factor_escala)),
            height=int(35 * self.factor_escala)
        )
        self.label_archivo.grid(row=0, column=0, pady=int(10 * self.factor_escala), padx=int(15 * self.factor_escala))
        
        # Indicador de estado
        self.indicator = ctk.CTkFrame(
            info_frame,
            width=int(8 * self.factor_escala),
            height=int(8 * self.factor_escala),
            corner_radius=int(4 * self.factor_escala)
        )
        self.indicator.grid(row=0, column=1, pady=int(10 * self.factor_escala), padx=(0, int(15 * self.factor_escala)), sticky="e")
    
    def _cargar_archivo(self):
        """Carga el archivo de procesos."""
        ruta = fd.askopenfilename(
            title="Selecciona archivo de procesos", 
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
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
                    font=ctk.CTkFont(size=int(13 * self.factor_escala), weight="bold")
                )
                
                # Cambiar indicador a verde
                self.indicator.configure(fg_color="green")
                
                # Mantener el color azul del botón
                # No cambiar el color del botón
                
                # Notificar que se cargó un archivo
                if self.callback_archivo_cargado:
                    self.callback_archivo_cargado(self.procesos_cargados)
                    
            except Exception as e:
                # Actualizar interfaz con error
                self.label_archivo.configure(
                    text=f"✗ Error al cargar archivo",
                    font=ctk.CTkFont(size=int(13 * self.factor_escala), weight="bold")
                )
                
                # Cambiar indicador a rojo
                self.indicator.configure(fg_color="red")
    
    def _leer_archivo_procesos(self, ruta):
        """Lee y parsea el archivo JSON de procesos."""
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                datos_json = json.load(archivo)
            
            # Validar que sea una lista
            if not isinstance(datos_json, list):
                raise Exception("El archivo JSON debe contener una lista de procesos")
            
            self.procesos_cargados = []
            for i, proceso_data in enumerate(datos_json):
                # Validar campos requeridos
                campos_requeridos = ['nombre', 'tiempo_arribo', 'cantidad_rafagas_cpu', 
                                   'duracion_rafaga_cpu', 'duracion_rafaga_es', 'prioridad_externa']
                
                for campo in campos_requeridos:
                    if campo not in proceso_data:
                        raise Exception(f"Falta el campo '{campo}' en el proceso {i+1}")
                
                # Crear proceso con la estructura esperada por el resto de la aplicación
                proceso = {
                    'nombre': str(proceso_data['nombre']),
                    'tiempo_arribo': int(proceso_data['tiempo_arribo']),
                    'rafagas_cpu': int(proceso_data['cantidad_rafagas_cpu']),
                    'duracion_rafaga_cpu': int(proceso_data['duracion_rafaga_cpu']),
                    'duracion_rafaga_io': int(proceso_data['duracion_rafaga_es']),
                    'prioridad': int(proceso_data['prioridad_externa'])
                }
                self.procesos_cargados.append(proceso)
            
            if not self.procesos_cargados:
                raise Exception("No se encontraron procesos válidos en el archivo")
            
        except json.JSONDecodeError as e:
            raise Exception(f"Error al parsear JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al leer archivo: {str(e)}")
    
    def obtener_procesos(self):
        """Retorna los procesos cargados."""
        return self.procesos_cargados
    
    def establecer_callback(self, callback):
        """Establece el callback cuando se carga un archivo."""
        self.callback_archivo_cargado = callback
    
    def actualizar_escalado(self, nuevo_factor_escala):
        """Actualiza el escalado del componente dinámicamente."""
        self.factor_escala = nuevo_factor_escala
        
        # Actualizar elementos principales
        if hasattr(self, 'boton_cargar'):
            self.boton_cargar.configure(
                height=int(45 * self.factor_escala),
                corner_radius=int(12 * self.factor_escala),
                font=ctk.CTkFont(size=int(14 * self.factor_escala), weight="bold")
            )
        
        if hasattr(self, 'label_archivo'):
            self.label_archivo.configure(
                font=ctk.CTkFont(size=int(13 * self.factor_escala)),
                height=int(35 * self.factor_escala)
            )