import customtkinter as ctk
import tkinter as tk

from .components.file_loader import CargadorArchivos
from .components.policy_selector import SelectorPoliticas
from .components.parameter_input import EntradaParametros
from .components.results_tab import PestañaResultados

class VentanaPrincipal(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        # Configurar tema moderno
        self._configurar_tema()
        
        # Configurar escalado dinámico
        self._configurar_escalado()
        
        # Configuración de la ventana
        self.title("Simulador de Planificación de Procesos")
        self.geometry(f"{self.ancho_ventana}x{self.alto_ventana}")
        self.minsize(int(self.ancho_ventana * 0.8), int(self.alto_ventana * 0.8))
        
        
        # Variables de estado
        self.procesos_cargados = []
        self.sidebar_colapsado = False
        
        # Configurar grid principal - 3 columnas
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(2, weight=1)  # Área principal
        self.grid_rowconfigure(0, weight=1)
        
        # Crear componentes
        self._crear_componentes()
        self._configurar_callbacks()
    
    def _configurar_tema(self):
        """Configura el tema moderno de la aplicación."""
        ctk.set_appearance_mode("Dark")  # Siempre modo oscuro
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    
    def _configurar_escalado(self):
        """Configura el escalado dinámico basado en la resolución de pantalla."""
        # Obtener resolución de la pantalla principal
        ancho_pantalla = self._obtener_ancho_pantalla_principal()
        
        # Calcular factor de escala basado en resolución
        self._calcular_factor_escala(ancho_pantalla)
        
        # Aplicar escalado
        self._aplicar_escalado()
    
    def _obtener_ancho_pantalla_principal(self):
        """Obtiene el ancho de la pantalla principal usando screeninfo."""
        from screeninfo import get_monitors
        monitors = get_monitors()
        
        # Buscar el monitor principal
        for monitor in monitors:
            if monitor.is_primary:
                return monitor.width
        
        # Si no hay monitor marcado como principal, usar el primero
        if monitors:
            return monitors[0].width
        
        # Si no hay monitores detectados, usar 1920 como fallback
        return 1920
    
    def _calcular_factor_escala(self, ancho_pantalla):
        """Calcula el factor de escala basado en la resolución de pantalla."""
        if ancho_pantalla >= 3840:
            self.factor_escala = 2.0
        elif ancho_pantalla >= 2560:
            self.factor_escala = 1.8 
        elif ancho_pantalla >= 1920:
            self.factor_escala = 1 
        else:  # HD o menor
            self.factor_escala = 0.9
    
    def _aplicar_escalado(self):
        """Aplica el escalado calculado a todos los elementos de la interfaz."""
        # Calcular dimensiones de ventana
        self.ancho_ventana = int(1800 * self.factor_escala)
        self.alto_ventana = int(1000 * self.factor_escala)
        
        # Calcular tamaños de fuente escalados
        self.fuentes = {
            "titulo_principal": int(28 * self.factor_escala),
            "titulo_seccion": int(22 * self.factor_escala),
            "titulo_componente": int(18 * self.factor_escala),
            "texto_normal": int(16 * self.factor_escala),
            "texto_pequeno": int(14 * self.factor_escala),
            "texto_muy_pequeno": int(12 * self.factor_escala),
        }
        
        # Calcular espaciado escalado
        self.espaciado = {
            "xs": int(4 * self.factor_escala),
            "sm": int(8 * self.factor_escala),
            "md": int(16 * self.factor_escala),
            "lg": int(24 * self.factor_escala),
            "xl": int(32 * self.factor_escala),
            "xxl": int(48 * self.factor_escala),
        }
        
        # Calcular bordes escalados
        self.bordes = {
            "radius_small": int(4 * self.factor_escala),
            "radius_medium": int(8 * self.factor_escala),
            "radius_large": int(12 * self.factor_escala),
            "radius_xlarge": int(16 * self.factor_escala),
        }
    
    def _recalcular_escalado(self):
        """Recalcula el escalado basado en la resolución actual."""
        ancho_pantalla = self.winfo_screenwidth()
        self._calcular_factor_escala(ancho_pantalla)
        
        # Aplicar nuevo escalado
        self._aplicar_escalado()
        
        # Redimensionar ventana
        self.geometry(f"{self.ancho_ventana}x{self.alto_ventana}")
        
        # Actualizar todos los componentes
        self._actualizar_escalado_componentes()
    
    def _actualizar_escalado_componentes(self):
        """Actualiza el escalado de todos los componentes existentes."""
        # Actualizar sidebar
        if hasattr(self, 'sidebar'):
            self.sidebar.configure(
                width=int(420 * self.factor_escala),
                corner_radius=self.bordes["radius_xlarge"]
            )
        
        # Actualizar botón de simulación
        if hasattr(self, 'boton_simular_header'):
            self.boton_simular_header.configure(
                height=int(60 * self.factor_escala),
                corner_radius=int(12 * self.factor_escala),
                font=ctk.CTkFont(size=int(16 * self.factor_escala), weight="bold")
            )
        
        
        # Notificar a los componentes que actualicen su escalado
        if hasattr(self, 'cargador_archivos'):
            self.cargador_archivos.actualizar_escalado(self.factor_escala)
        if hasattr(self, 'selector_politicas'):
            self.selector_politicas.actualizar_escalado(self.factor_escala)
        if hasattr(self, 'entrada_parametros'):
            self.entrada_parametros.actualizar_escalado(self.factor_escala)
        if hasattr(self, 'pestaña_resultados'):
            self.pestaña_resultados.actualizar_escalado(self.factor_escala)
    
    def _crear_componentes(self):
        """Crea todos los componentes de la interfaz."""
        # Sidebar izquierdo - Configuración
        self._crear_sidebar()
        # Área principal derecha - Resultados
        self._crear_area_principal()
    
    def _crear_sidebar(self):
        """Crea el sidebar izquierdo con componentes de configuración."""
        # Frame principal del sidebar
        self.sidebar = ctk.CTkFrame(
            self, 
            corner_radius=self.bordes["radius_xlarge"],
            width=int(420 * self.factor_escala)  # Aumentado de 350 a 420
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=self.espaciado["lg"], pady=self.espaciado["lg"])
        self.sidebar.grid_propagate(False)  # Mantener ancho fijo
        self.sidebar.grid_columnconfigure(0, weight=1)
        
        # Header del sidebar con botón de simulación
        header_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
            height=int(80 * self.factor_escala)
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=self.espaciado["lg"], pady=(self.espaciado["xl"], self.espaciado["lg"]))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Botón de simulación en el header
        self.boton_simular_header = ctk.CTkButton(
            header_frame,
            text="Ejecutar Simulación",
            height=int(60 * self.factor_escala),
            corner_radius=int(12 * self.factor_escala),
            font=ctk.CTkFont(size=int(16 * self.factor_escala), weight="bold"),
            border_width=0,
            state="disabled",
            command=self._simular
        )
        self.boton_simular_header.grid(row=0, column=0, sticky="ew")
        
        
        # Línea decorativa con sombra
        linea = ctk.CTkFrame(
            header_frame,
            height=int(3 * self.factor_escala),
            corner_radius=int(2 * self.factor_escala)
        )
        linea.grid(row=1, column=0, pady=(int(8 * self.factor_escala), 0), sticky="ew")
        
        # Frame scrollable para los componentes
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color="transparent"
            # No especificar height para que se expanda automáticamente
        )
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=self.espaciado["md"], pady=(0, self.espaciado["lg"]))
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Configurar que la fila del scrollable frame se expanda
        self.sidebar.grid_rowconfigure(1, weight=1)
        
        # Componente de carga de archivos
        self.cargador_archivos = CargadorArchivos(
            self.scrollable_frame, 
            factor_escala=self.factor_escala
        )
        self.cargador_archivos.grid(row=0, column=0, sticky="ew", pady=(0, self.espaciado["lg"]))
        
        # Componente de selección de política
        self.selector_politicas = SelectorPoliticas(
            self.scrollable_frame, 
            factor_escala=self.factor_escala
        )
        self.selector_politicas.grid(row=1, column=0, sticky="ew", pady=(0, self.espaciado["lg"]))
        
        # Componente de parámetros del sistema
        self.entrada_parametros = EntradaParametros(
            self.scrollable_frame, 
            factor_escala=self.factor_escala
        )
        self.entrada_parametros.grid(row=2, column=0, sticky="ew", pady=(0, self.espaciado["lg"]))
        
    
    
    def _crear_area_principal(self):
        """Crea el área principal derecha con la pestaña de resultados."""
        # Frame principal del área derecha
        self.area_principal = ctk.CTkFrame(
            self, 
            corner_radius=self.bordes["radius_xlarge"],
            border_width=0  # Sin borde para eliminar la línea externa
        )
        self.area_principal.grid(row=0, column=2, sticky="nsew", padx=(0, self.espaciado["lg"]), pady=self.espaciado["lg"])
        self.area_principal.grid_columnconfigure(0, weight=1)
        self.area_principal.grid_rowconfigure(0, weight=1)
        
        # Crear directamente la pestaña de resultados
        self._crear_pestaña_resultados()
    
    def _crear_pestaña_resultados(self):
        """Crea la pestaña de resultados directamente."""
        # Crear pestaña de resultados
        self.pestaña_resultados = PestañaResultados(
            self.area_principal, 
            factor_escala=self.factor_escala
        )
        self.pestaña_resultados.grid(row=0, column=0, sticky="nsew", padx=self.espaciado["lg"], pady=self.espaciado["lg"])
    
    
    
    def _configurar_callbacks(self):
        """Configura los callbacks entre componentes."""
        # File loader callbacks
        self.cargador_archivos.establecer_callback(self._archivo_cargado)
        
        # Policy selector callbacks
        self.selector_politicas.establecer_callback(self._cambio_politica)
        
        # Parameter input callbacks
        self.entrada_parametros.establecer_callback(self._cambio_parametro)
        
        # Configurar estado inicial del quantum (FCFS por defecto)
        self._cambio_politica("FCFS")
        
        # Simulation controls callbacks (solo para limpiar)
        # self.controles_simulacion.establecer_callback_limpiar(self._limpiar_resultados) # Eliminado
    
    def _archivo_cargado(self, procesos):
        """Callback cuando se carga un archivo."""
        self.procesos_cargados = procesos
        self._verificar_estado_simulacion()
    
    def _cambio_politica(self, politica):
        """Callback cuando cambia la política de planificación."""
        # Habilitar/deshabilitar quantum según la política
        if politica == "Round Robin":
            self.entrada_parametros.habilitar_quantum(True)
        else:
            self.entrada_parametros.habilitar_quantum(False)
        
        self._verificar_estado_simulacion()
    
    def _cambio_parametro(self, nombre_param, valor):
        """Callback cuando cambian los parámetros."""
        self._verificar_estado_simulacion()
    
    def _verificar_estado_simulacion(self):
        """Verifica si se pueden habilitar los controles de simulación."""
        # Verificar que haya archivo cargado
        if not self.procesos_cargados:
            self.boton_simular_header.configure(state="disabled")
            return
        
        # Verificar que los parámetros sean válidos
        es_valido, _ = self.entrada_parametros.validar_parametros()
        if not es_valido:
            self.boton_simular_header.configure(state="disabled")
            return
        
        # Si todo está bien, habilitar el botón
        self.boton_simular_header.configure(state="normal")
    
    
    def _simular(self):
        """Ejecuta la simulación."""
        if not self.procesos_cargados:
            return
        
        # Validar parámetros
        es_valido, mensaje = self.entrada_parametros.validar_parametros()
        if not es_valido:
            return
        
        # Obtener parámetros
        parametros = self.entrada_parametros.obtener_todos_parametros()
        politica = self.selector_politicas.obtener_politica_seleccionada()
        
        # Limpiar resultados anteriores
        self.pestaña_resultados.limpiar_resultados()
        
        # Ejecutar simulación (por ahora solo muestra información)
        self._ejecutar_simulacion_basica(politica, parametros)
    
    def _ejecutar_simulacion_basica(self, politica, parametros):
        """Ejecuta la simulación usando el algoritmo seleccionado."""
        
        # Importar el simulador
        from ..simulador.simulador import Simulador
        
        # Crear instancia del simulador
        simulador = Simulador()
        
        # Ejecutar simulación según la política seleccionada
        if politica == "FCFS":
            resultados = simulador.ejecutar_fcfs(
                self.procesos_cargados,
                parametros['tip'],
                parametros['tcp'],
                parametros['tfp']
            )
        else:
            # Para otros algoritmos, mostrar mensaje de no implementado
            self.pestaña_resultados.mostrar_mensaje_inicial()
            return
        
        # Actualizar la interfaz con los resultados reales
        if resultados:
            self.pestaña_resultados.actualizar_resultados_procesos(resultados['procesos'])
            self.pestaña_resultados.actualizar_resultados_tanda(
                resultados['tiempo_total'], 
                resultados['tiempo_medio_retorno']
            )
            self.pestaña_resultados.actualizar_resultados_cpu(
                resultados['cpu_desocupada'],
                resultados['cpu_so'],
                resultados['cpu_procesos']
            )
            
    
    def _limpiar_resultados(self):
        """Limpia todos los resultados."""
        self.pestaña_resultados.limpiar_resultados()
    
