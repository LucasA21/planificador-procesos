import customtkinter as ctk
from datetime import datetime

from .components.file_loader import CargadorArchivos
from .components.policy_selector import SelectorPoliticas
from .components.parameter_input import EntradaParametros
from .components.simulation_controls import ControlesSimulacion
from .components.results_tab import PestañaResultados
from .components.gantt_tab import PestañaGantt
from .components.stats_tab import PestañaEstadisticas

class VentanaPrincipal(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Simulador de Planificacion de Procesos")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # Variables de estado
        self.procesos_cargados = []
        self.tab_actual = "resultados"
        
        # Configurar grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
        # Crear componentes
        self._crear_componentes()
        self._configurar_callbacks()
        
        # Crear barra de estado
        self._crear_barra_estado()
    
    def _crear_componentes(self):
        """Crea todos los componentes de la interfaz."""
        # Panel izquierdo - Configuración
        self._crear_panel_izquierdo()
        
        # Panel derecho - Resultados
        self._crear_panel_derecho()
    
    def _crear_panel_izquierdo(self):
        """Crea el panel izquierdo con componentes de configuración."""
        # Frame principal del panel izquierdo
        self.panel_izquierdo = ctk.CTkFrame(self, corner_radius=15)
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.panel_izquierdo.grid_columnconfigure(0, weight=1)
        
        # Título principal
        titulo = ctk.CTkLabel(
            self.panel_izquierdo, 
            text="CONFIGURACION", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(20, 30), padx=20)
        
        # Componente de carga de archivos
        self.cargador_archivos = CargadorArchivos(self.panel_izquierdo)
        self.cargador_archivos.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Componente de selección de política
        self.selector_politicas = SelectorPoliticas(self.panel_izquierdo)
        self.selector_politicas.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Componente de parámetros del sistema
        self.entrada_parametros = EntradaParametros(self.panel_izquierdo)
        self.entrada_parametros.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Componente de controles de simulación
        self.controles_simulacion = ControlesSimulacion(self.panel_izquierdo)
        self.controles_simulacion.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 20))
    
    def _crear_panel_derecho(self):
        """Crea el panel derecho con pestañas de resultados."""
        # Frame principal del panel derecho
        self.panel_derecho = ctk.CTkFrame(self, corner_radius=15)
        self.panel_derecho.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.panel_derecho.grid_columnconfigure(0, weight=1)
        self.panel_derecho.grid_rowconfigure(1, weight=1)
        
        # Título del panel derecho
        titulo_resultados = ctk.CTkLabel(
            self.panel_derecho, 
            text="RESULTADOS Y VISUALIZACIONES", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo_resultados.grid(row=0, column=0, pady=(20, 20), padx=20)
        
        # Crear sistema de pestañas
        self._crear_sistema_pestañas()
    
    def _crear_sistema_pestañas(self):
        """Crea el sistema de pestañas para los resultados."""
        # Frame para las pestañas
        frame_tabs = ctk.CTkFrame(self.panel_derecho, corner_radius=10)
        frame_tabs.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        frame_tabs.grid_columnconfigure(0, weight=1)
        frame_tabs.grid_rowconfigure(1, weight=1)
        
        # Botones de pestañas
        self._crear_botones_pestañas(frame_tabs)
        
        # Contenido de las pestañas
        self._crear_contenido_pestañas(frame_tabs)
    
    def _crear_botones_pestañas(self, parent):
        """Crea los botones de navegación entre pestañas."""
        # Botón pestaña resultados
        self.boton_tab_resultados = ctk.CTkButton(
            parent,
            text="Resultados",
            command=lambda: self._cambiar_tab("resultados"),
            height=35,
            fg_color="blue"
        )
        self.boton_tab_resultados.grid(row=0, column=0, pady=(15, 0), padx=(15, 5), sticky="ew")
        
        # Botón pestaña Gantt
        self.boton_tab_gantt = ctk.CTkButton(
            parent,
            text="Diagrama Gantt",
            command=lambda: self._cambiar_tab("gantt"),
            height=35
        )
        self.boton_tab_gantt.grid(row=0, column=1, pady=(15, 0), padx=5, sticky="ew")
        
        # Botón pestaña estadísticas
        self.boton_tab_estadisticas = ctk.CTkButton(
            parent,
            text="Estadisticas",
            command=lambda: self._cambiar_tab("estadisticas"),
            height=35
        )
        self.boton_tab_estadisticas.grid(row=0, column=2, pady=(15, 0), padx=(5, 15), sticky="ew")
    
    def _crear_contenido_pestañas(self, parent):
        """Crea el contenido de las pestañas."""
        # Pestaña de resultados
        self.pestaña_resultados = PestañaResultados(parent)
        self.pestaña_resultados.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=15, pady=15)
        
        # Pestaña de Gantt
        self.pestaña_gantt = PestañaGantt(parent)
        self.pestaña_gantt.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=15, pady=15)
        self.pestaña_gantt.grid_remove()  # Ocultar inicialmente
        
        # Pestaña de estadísticas
        self.pestaña_estadisticas = PestañaEstadisticas(parent)
        self.pestaña_estadisticas.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=15, pady=15)
        self.pestaña_estadisticas.grid_remove()  # Ocultar inicialmente
    
    def _crear_barra_estado(self):
        """Crea la barra de estado inferior."""
        self.barra_estado = ctk.CTkFrame(self, height=30)
        self.barra_estado.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 15))
        self.barra_estado.grid_columnconfigure(0, weight=1)
        
        # Label de estado
        self.label_estado = ctk.CTkLabel(
            self.barra_estado,
            text="Estado: Listo para cargar archivo",
            text_color="lightgreen"
        )
        self.label_estado.grid(row=0, column=0, pady=5, padx=15, sticky="w")
        
        # Label de tiempo
        self.label_tiempo = ctk.CTkLabel(
            self.barra_estado,
            text=f"Ultima actualizacion: {datetime.now().strftime('%H:%M:%S')}",
            text_color="gray"
        )
        self.label_tiempo.grid(row=0, column=1, pady=5, padx=15, sticky="e")
    
    def _configurar_callbacks(self):
        """Configura los callbacks entre componentes."""
        # File loader callbacks
        self.cargador_archivos.establecer_callback(self._archivo_cargado)
        
        # Policy selector callbacks
        self.selector_politicas.establecer_callback(self._cambio_politica)
        
        # Parameter input callbacks
        self.entrada_parametros.establecer_callback(self._cambio_parametro)
        
        # Simulation controls callbacks
        self.controles_simulacion.establecer_callback_simulacion(self._simular)
        self.controles_simulacion.establecer_callback_limpiar(self._limpiar_resultados)
    
    def _archivo_cargado(self, procesos):
        """Callback cuando se carga un archivo."""
        self.procesos_cargados = procesos
        self.controles_simulacion.habilitar_simulacion(True)
        self.label_estado.configure(
            text=f"Estado: {len(procesos)} procesos cargados correctamente",
            text_color="lightgreen"
        )
        self._actualizar_tiempo()
    
    def _cambio_politica(self, politica):
        """Callback cuando cambia la política de planificación."""
        # Habilitar/deshabilitar quantum según la política
        if politica == "Round Robin":
            self.entrada_parametros.habilitar_quantum(True)
        else:
            self.entrada_parametros.habilitar_quantum(False)
    
    def _cambio_parametro(self, nombre_param, valor):
        """Callback cuando cambian los parámetros."""
        # Aquí podrías agregar validación adicional si es necesario
        pass
    
    def _cambiar_tab(self, tab):
        """Cambia entre las pestañas de resultados."""
        self.tab_actual = tab
        
        # Ocultar todas las pestañas
        self.pestaña_resultados.grid_remove()
        self.pestaña_gantt.grid_remove()
        self.pestaña_estadisticas.grid_remove()
        
        # Mostrar la pestaña seleccionada
        if tab == "resultados":
            self.pestaña_resultados.grid()
            self.boton_tab_resultados.configure(fg_color="blue")
            self.boton_tab_gantt.configure(fg_color="transparent")
            self.boton_tab_estadisticas.configure(fg_color="transparent")
        elif tab == "gantt":
            self.pestaña_gantt.grid()
            self.boton_tab_resultados.configure(fg_color="transparent")
            self.boton_tab_gantt.configure(fg_color="blue")
            self.boton_tab_estadisticas.configure(fg_color="transparent")
        elif tab == "estadisticas":
            self.pestaña_estadisticas.grid()
            self.boton_tab_resultados.configure(fg_color="transparent")
            self.boton_tab_gantt.configure(fg_color="transparent")
            self.boton_tab_estadisticas.configure(fg_color="blue")
    
    def _simular(self):
        """Ejecuta la simulación."""
        if not self.procesos_cargados:
            self.label_estado.configure(
                text="Estado: No hay procesos cargados para simular",
                text_color="red"
            )
            return
        
        # Validar parámetros
        es_valido, mensaje = self.entrada_parametros.validar_parametros()
        if not es_valido:
            self.label_estado.configure(
                text=f"Estado: {mensaje}",
                text_color="red"
            )
            return
        
        # Obtener parámetros
        parametros = self.entrada_parametros.obtener_todos_parametros()
        politica = self.selector_politicas.obtener_politica_seleccionada()
        
        # Cambiar a la pestaña de resultados
        self._cambiar_tab("resultados")
        
        # Ejecutar simulación (por ahora solo muestra información)
        self._ejecutar_simulacion_basica(politica, parametros)
        
        # Actualizar estado
        self.label_estado.configure(
            text="Estado: Simulacion completada (ejemplo)",
            text_color="lightgreen"
        )
        self._actualizar_tiempo()
    
    def _ejecutar_simulacion_basica(self, politica, parametros):
        """Ejecuta una simulación básica de ejemplo."""
        # Limpiar resultados anteriores
        self.pestaña_resultados.limpiar_resultados()
        
        # Agregar información de la simulación
        self.pestaña_resultados.agregar_resultado("INICIANDO SIMULACION")
        self.pestaña_resultados.agregar_resultado("=" * 50)
        self.pestaña_resultados.agregar_resultado(f"Politica seleccionada: {politica}")
        self.pestaña_resultados.agregar_resultado("Parametros del sistema:")
        self.pestaña_resultados.agregar_resultado(f"  • TIP: {parametros['tip']}")
        self.pestaña_resultados.agregar_resultado(f"  • TFP: {parametros['tfp']}")
        self.pestaña_resultados.agregar_resultado(f"  • TCP: {parametros['tcp']}")
        if parametros['quantum'] > 0:
            self.pestaña_resultados.agregar_resultado(f"  • Quantum: {parametros['quantum']}")
        self.pestaña_resultados.agregar_resultado(f"Procesos a simular: {len(self.procesos_cargados)}")
        self.pestaña_resultados.agregar_resultado("")
        
        # Simular eventos básicos
        self.pestaña_resultados.agregar_resultado("EVENTOS DE LA SIMULACION:")
        self.pestaña_resultados.agregar_resultado("-" * 30)
        
        tiempo_actual = 0
        for proceso in self.procesos_cargados:
            self.pestaña_resultados.agregar_resultado(f"[{tiempo_actual}] Arriba proceso {proceso['nombre']}")
            tiempo_actual += parametros['tip']
            self.pestaña_resultados.agregar_resultado(f"[{tiempo_actual}] Proceso {proceso['nombre']} incorporado al sistema")
            tiempo_actual += parametros['tcp']
            self.pestaña_resultados.agregar_resultado(f"[{tiempo_actual}] Proceso {proceso['nombre']} comienza ejecucion")
            tiempo_actual += proceso['duracion_rafaga_cpu']
            self.pestaña_resultados.agregar_resultado(f"[{tiempo_actual}] Proceso {proceso['nombre']} completa rafaga de CPU")
            tiempo_actual += parametros['tfp']
            self.pestaña_resultados.agregar_resultado(f"[{tiempo_actual}] Proceso {proceso['nombre']} terminado")
            self.pestaña_resultados.agregar_resultado("")
        
        self.pestaña_resultados.agregar_resultado(f"Tiempo total de simulacion: {tiempo_actual} unidades")
        self.pestaña_resultados.agregar_resultado("Simulacion completada (ejemplo basico)")
        self.pestaña_resultados.agregar_resultado("")
        self.pestaña_resultados.agregar_resultado("Para ver resultados reales, conecta tu logica de simulacion")
    
    def _limpiar_resultados(self):
        """Limpia todos los resultados."""
        self.pestaña_resultados.limpiar_resultados()
        self.pestaña_gantt.limpiar_gantt()
        self.pestaña_estadisticas.limpiar_estadisticas()
        
        self.label_estado.configure(
            text="Estado: Resultados limpiados",
            text_color="yellow"
        )
        self._actualizar_tiempo()
    
    def _actualizar_tiempo(self):
        """Actualiza el timestamp de última actualización."""
        self.label_tiempo.configure(
            text=f"Ultima actualizacion: {datetime.now().strftime('%H:%M:%S')}"
        )

