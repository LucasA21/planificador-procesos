import customtkinter as ctk
import tkinter as tk

from .components.file_loader import CargadorArchivos
from .components.policy_selector import SelectorPoliticas
from .components.parameter_input import EntradaParametros
from .components.results_tab import PestañaResultados
from .components.gantt_tab import PestañaGantt

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
        self.tab_actual = "resultados"
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
        # Obtener resolución de pantalla
        root = tk.Tk()
        root.withdraw()
        ancho_pantalla = root.winfo_screenwidth()
        alto_pantalla = root.winfo_screenheight()
        root.destroy()
        
        if ancho_pantalla >= 3840:  # 4K
            self.factor_escala = 2.0  # Aumentado de 1.5 a 2.0
        elif ancho_pantalla >= 2560:  # 2K/QHD (3K)
            self.factor_escala = 1.8  # Aumentado de 1.3 a 1.8
        elif ancho_pantalla >= 1920:  # Full HD
            self.factor_escala = 1.2  # Aumentado de 1.0 a 1.2
        else:  # HD o menor
            self.factor_escala = 1.0  # Aumentado de 0.8 a 1.0
        
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
        """Crea el área principal derecha con pestañas de resultados."""
        # Frame principal del área derecha
        self.area_principal = ctk.CTkFrame(
            self, 
            corner_radius=self.bordes["radius_xlarge"],
            border_width=0  # Sin borde para eliminar la línea externa
        )
        self.area_principal.grid(row=0, column=2, sticky="nsew", padx=(0, self.espaciado["lg"]), pady=self.espaciado["lg"])
        self.area_principal.grid_columnconfigure(0, weight=1)
        self.area_principal.grid_rowconfigure(0, weight=1)
        
        # Crear sistema de pestañas directamente
        self._crear_sistema_pestañas()
    
    def _crear_sistema_pestañas(self):
        """Crea el sistema de pestañas para los resultados."""
        # Frame para las pestañas con el color gris de fondo
        frame_tabs = ctk.CTkFrame(
            self.area_principal, 
            corner_radius=self.bordes["radius_large"],
            border_width=0  # Sin borde para eliminar la línea molesta
        )
        frame_tabs.grid(row=0, column=0, sticky="nsew", padx=self.espaciado["lg"], pady=self.espaciado["lg"])
        frame_tabs.grid_columnconfigure(0, weight=1)
        frame_tabs.grid_rowconfigure(1, weight=1)
        
        # Botones de pestañas
        self._crear_botones_pestañas(frame_tabs)
        
        # Contenido de las pestañas
        self._crear_contenido_pestañas(frame_tabs)
    
    def _crear_botones_pestañas(self, parent):
        """Crea los botones de navegación entre pestañas."""
        # Frame para los botones de pestañas
        tabs_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            height=int(50 * self.factor_escala)
        )
        tabs_frame.grid(row=0, column=0, sticky="ew", padx=self.espaciado["lg"], pady=(self.espaciado["lg"], 0))
        tabs_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Botón pestaña resultados
        self.boton_tab_resultados = ctk.CTkButton(
            tabs_frame,
            text="📊 Resultados de Simulación",
            command=lambda: self._cambiar_tab("resultados"),
            height=int(40 * self.factor_escala),
            corner_radius=self.bordes["radius_small"],
            font=ctk.CTkFont(size=int(14 * self.factor_escala), weight="bold")
        )
        self.boton_tab_resultados.grid(row=0, column=0, pady=(0, 0), padx=(0, 5), sticky="ew")
        
        # Botón pestaña Gantt
        self.boton_tab_gantt = ctk.CTkButton(
            tabs_frame,
            text="📈 Diagrama Gantt",
            command=lambda: self._cambiar_tab("gantt"),
            height=int(40 * self.factor_escala),
            corner_radius=self.bordes["radius_small"],
            fg_color="transparent",
            font=ctk.CTkFont(size=int(14 * self.factor_escala))
        )
        self.boton_tab_gantt.grid(row=0, column=1, pady=(0, 0), padx=(5, 0), sticky="ew")
    
    def _crear_contenido_pestañas(self, parent):
        """Crea el contenido de las pestañas."""
        # Pestaña de resultados
        self.pestaña_resultados = PestañaResultados(
            parent, 
            factor_escala=self.factor_escala
        )
        self.pestaña_resultados.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=self.espaciado["lg"], pady=self.espaciado["lg"])
        self.pestaña_resultados.mostrar_mensaje_inicial()
        
        # Pestaña de Gantt
        self.pestaña_gantt = PestañaGantt(
            parent, 
            factor_escala=self.factor_escala
        )
        self.pestaña_gantt.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=self.espaciado["lg"], pady=self.espaciado["lg"])
        self.pestaña_gantt.grid_remove()  # Ocultar inicialmente
    
    def _configurar_callbacks(self):
        """Configura los callbacks entre componentes."""
        # File loader callbacks
        self.cargador_archivos.establecer_callback(self._archivo_cargado)
        
        # Policy selector callbacks
        self.selector_politicas.establecer_callback(self._cambio_politica)
        
        # Parameter input callbacks
        self.entrada_parametros.establecer_callback(self._cambio_parametro)
        
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
    
    def _cambiar_tab(self, tab):
        """Cambia entre las pestañas de resultados."""
        self.tab_actual = tab
        
        # Ocultar todas las pestañas
        self.pestaña_resultados.grid_remove()
        self.pestaña_gantt.grid_remove()
        
        # Mostrar la pestaña seleccionada
        if tab == "resultados":
            self.pestaña_resultados.grid()
            self.boton_tab_resultados.configure(
                font=ctk.CTkFont(size=int(14 * self.factor_escala), weight="bold")
            )
            self.boton_tab_gantt.configure(
                fg_color="transparent",
                font=ctk.CTkFont(size=int(14 * self.factor_escala))
            )
        elif tab == "gantt":
            self.pestaña_gantt.grid()
            self.boton_tab_resultados.configure(
                fg_color="transparent",
                font=ctk.CTkFont(size=int(14 * self.factor_escala))
            )
            self.boton_tab_gantt.configure(
                font=ctk.CTkFont(size=int(14 * self.factor_escala), weight="bold")
            )
    
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
        
        # Cambiar a la pestaña de resultados
        self._cambiar_tab("resultados")
        
        # Ejecutar simulación (por ahora solo muestra información)
        self._ejecutar_simulacion_basica(politica, parametros)
    
    def _ejecutar_simulacion_basica(self, politica, parametros):
        """Ejecuta una simulación básica de ejemplo."""
        # Limpiar resultados anteriores
        self.pestaña_resultados.limpiar_resultados()
        
        # Simular datos de ejemplo para mostrar el diseño
        datos_procesos = []
        tiempo_total = 0
        
        for i, proceso in enumerate(self.procesos_cargados):
            # Calcular tiempos de ejemplo
            tiempo_arribo = proceso['tiempo_arribo']
            tiempo_ejecucion = proceso['duracion_rafaga_cpu']
            tiempo_fin = tiempo_arribo + tiempo_ejecucion + parametros['tcp'] + parametros['tfp']
            tiempo_retorno = tiempo_fin - tiempo_arribo
            tiempo_retorno_normalizado = tiempo_retorno / tiempo_ejecucion if tiempo_ejecucion > 0 else 0
            tiempo_estado_listo = max(0, tiempo_retorno - tiempo_ejecucion)
            
            datos_procesos.append({
                'nombre': proceso['nombre'],
                'tiempo_retorno': tiempo_retorno,
                'tiempo_retorno_normalizado': round(tiempo_retorno_normalizado, 2),
                'tiempo_estado_listo': tiempo_estado_listo
            })
            
            tiempo_total = max(tiempo_total, tiempo_fin)
        
        # Calcular estadísticas de la tanda
        tiempos_retorno = [p['tiempo_retorno'] for p in datos_procesos]
        tiempo_medio_retorno = sum(tiempos_retorno) / len(tiempos_retorno) if tiempos_retorno else 0
        
        # Calcular uso de CPU (ejemplo)
        tiempo_cpu_procesos = sum(proceso['duracion_rafaga_cpu'] for proceso in self.procesos_cargados)
        tiempo_cpu_so = len(self.procesos_cargados) * parametros['tcp']
        tiempo_cpu_desocupada = max(0, tiempo_total - tiempo_cpu_procesos - tiempo_cpu_so)
        
        # Actualizar la interfaz con los resultados
        self.pestaña_resultados.actualizar_resultados_procesos(datos_procesos)
        self.pestaña_resultados.actualizar_resultados_tanda(tiempo_total, tiempo_medio_retorno)
        self.pestaña_resultados.actualizar_resultados_cpu(
            f"{tiempo_cpu_desocupada} ({tiempo_cpu_desocupada/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            f"{tiempo_cpu_so} ({tiempo_cpu_so/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            f"{tiempo_cpu_procesos} ({tiempo_cpu_procesos/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)"
        )
    
    def _limpiar_resultados(self):
        """Limpia todos los resultados."""
        self.pestaña_resultados.limpiar_resultados()
        self.pestaña_gantt.limpiar_gantt()
