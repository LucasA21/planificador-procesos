"""
Componente para la carga de archivos de procesos.
"""

import customtkinter as ctk
import tkinter.filedialog as fd

class CargadorArchivos(ctk.CTkFrame):
    """Componente para cargar archivos de procesos."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        self.archivo_cargado = None
        self.procesos_cargados = []
        self.callback_archivo_cargado = None
        
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Título de sección
        titulo = ctk.CTkLabel(
            self, 
            text="ARCHIVO DE PROCESOS", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(15, 10), padx=15)
        
        # Botón para cargar archivo
        self.boton_cargar = ctk.CTkButton(
            self, 
            text="Seleccionar Archivo", 
            command=self._cargar_archivo,
            height=35
        )
        self.boton_cargar.grid(row=1, column=0, pady=(0, 10), padx=15, sticky="ew")
        
        # Label para mostrar archivo seleccionado
        self.label_archivo = ctk.CTkLabel(
            self, 
            text="Ningún archivo seleccionado",
            text_color="gray"
        )
        self.label_archivo.grid(row=2, column=0, pady=(0, 15), padx=15)
    
    def _cargar_archivo(self):
        """Carga el archivo de procesos."""
        ruta = fd.askopenfilename(
            title="Selecciona archivo de procesos", 
            filetypes=[("Archivos de texto", "*.txt")]
        )
        
        if ruta:
            try:
                self.archivo_cargado = ruta
                self.label_archivo.configure(
                    text=f"Archivo: {ruta.split('/')[-1]}",
                    text_color="lightgreen"
                )
                
                # Leer y parsear el archivo
                self._leer_archivo_procesos(ruta)
                
                # Notificar que se cargó un archivo
                if self.callback_archivo_cargado:
                    self.callback_archivo_cargado(self.procesos_cargados)
                    
            except Exception as e:
                self.label_archivo.configure(
                    text=f"Error al cargar archivo",
                    text_color="red"
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
