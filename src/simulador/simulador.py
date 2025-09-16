"""
Módulo de integración entre la lógica de algoritmos y la interfaz de usuario.
"""

import os
import sys
from datetime import datetime
from .proceso import Proceso
from .algoritmos.FCFS import FCFS
from .algoritmos.SPN import SPN
from .algoritmos.SRTN import SRTN
from .algoritmos.RR import RR
from .algoritmos.PE import PE
from .exportador_pdf import ExportadorPDF

class Simulador:
    """Clase que integra los algoritmos de planificación con la interfaz."""
    
    def __init__(self):
        self.algoritmo_actual = None
        self.procesos = []
        self.resultados = {}
    
    def crear_procesos_desde_datos(self, datos_json):
        """
        Convierte los datos JSON de la interfaz en instancias de Proceso.
        
        Args:
            datos_json: Lista de diccionarios con datos de procesos desde la interfaz
            
        Returns:
            Lista de instancias de Proceso
        """
        procesos = []
        
        for proceso_data in datos_json:
            # Mapear los nombres de campos de la interfaz a los de la clase Proceso
            proceso = Proceso(
                nombre=proceso_data['nombre'],
                tiempo_arrivo=proceso_data['tiempo_arribo'],
                cantidad_rafagas_cpu=proceso_data['cantidad_rafagas_cpu'],
                duracion_rafagas_cpu=proceso_data['duracion_rafaga_cpu'],
                duracion_rafagas_io=proceso_data['duracion_rafaga_es'],
                prioridad=proceso_data['prioridad_externa']
            )
            procesos.append(proceso)
        
        return procesos
    
    def ejecutar_fcfs(self, procesos_datos, tiempo_tip, tiempo_tcp, tiempo_tfp):
        """
        Ejecuta el algoritmo FCFS con los datos proporcionados.
        
        Args:
            procesos_datos: Lista de diccionarios con datos de procesos
            tiempo_tip: Tiempo de ingreso de proceso
            tiempo_tcp: Tiempo de conmutación de proceso
            tiempo_tfp: Tiempo de finalización de proceso
            
        Returns:
            Diccionario con resultados de la simulación
        """
        # Convertir datos a instancias de Proceso
        self.procesos = self.crear_procesos_desde_datos(procesos_datos)
        
        # Crear instancia del algoritmo FCFS
        self.algoritmo_actual = FCFS(self.procesos, tiempo_tip, tiempo_tcp, tiempo_tfp)
        
        # Ejecutar la simulación
        self.algoritmo_actual.ejecutar()
        
        # Procesar resultados para la interfaz
        resultados = self._procesar_resultados_fcfs()
        
        # Agregar ruta del PDF a los resultados
        if 'ruta_pdf' not in resultados:
            resultados['ruta_pdf'] = None
        
        return resultados
    
    def ejecutar_spn(self, procesos_datos, tiempo_tip, tiempo_tcp, tiempo_tfp):
        """
        Ejecuta el algoritmo SPN con los datos proporcionados.
        
        Args:
            procesos_datos: Lista de diccionarios con datos de procesos
            tiempo_tip: Tiempo de ingreso de proceso
            tiempo_tcp: Tiempo de conmutación de proceso
            tiempo_tfp: Tiempo de finalización de proceso
            
        Returns:
            Diccionario con resultados de la simulación
        """
        # Convertir datos a instancias de Proceso
        self.procesos = self.crear_procesos_desde_datos(procesos_datos)
        
        # Crear instancia del algoritmo SPN
        self.algoritmo_actual = SPN(self.procesos, tiempo_tip, tiempo_tcp, tiempo_tfp)
        
        # Ejecutar la simulación
        self.algoritmo_actual.ejecutar()
        
        # Procesar resultados para la interfaz
        resultados = self._procesar_resultados_spn()
        
        # Agregar ruta del PDF a los resultados
        if 'ruta_pdf' not in resultados:
            resultados['ruta_pdf'] = None
        
        return resultados
    
    def ejecutar_srtn(self, procesos_datos, tiempo_tip, tiempo_tcp, tiempo_tfp):
        """
        Ejecuta el algoritmo SRTN con los datos proporcionados.
        
        Args:
            procesos_datos: Lista de diccionarios con datos de procesos
            tiempo_tip: Tiempo de ingreso de proceso
            tiempo_tcp: Tiempo de conmutación de proceso
            tiempo_tfp: Tiempo de finalización de proceso
            
        Returns:
            Diccionario con resultados de la simulación
        """
        # Convertir datos a instancias de Proceso
        self.procesos = self.crear_procesos_desde_datos(procesos_datos)
        
        # Crear instancia del algoritmo SRTN
        self.algoritmo_actual = SRTN(self.procesos, tiempo_tip, tiempo_tcp, tiempo_tfp)
        
        # Ejecutar la simulación
        self.algoritmo_actual.ejecutar()
        
        # Procesar resultados para la interfaz
        resultados = self._procesar_resultados_srtn()
        
        # Agregar ruta del PDF a los resultados
        if 'ruta_pdf' not in resultados:
            resultados['ruta_pdf'] = None
        
        return resultados
    
    def ejecutar_rr(self, procesos_datos, tiempo_tip, tiempo_tcp, tiempo_tfp, quantum):
        """
        Ejecuta el algoritmo Round Robin con los datos proporcionados.
        
        Args:
            procesos_datos: Lista de diccionarios con datos de procesos
            tiempo_tip: Tiempo de ingreso de proceso
            tiempo_tcp: Tiempo de conmutación de proceso
            tiempo_tfp: Tiempo de finalización de proceso
            quantum: Tiempo de quantum para Round Robin
            
        Returns:
            Diccionario con resultados de la simulación
        """
        # Convertir datos a instancias de Proceso
        self.procesos = self.crear_procesos_desde_datos(procesos_datos)
        
        # Crear instancia del algoritmo Round Robin
        self.algoritmo_actual = RR(self.procesos, tiempo_tip, tiempo_tcp, tiempo_tfp, quantum)
        
        # Ejecutar la simulación
        self.algoritmo_actual.ejecutar()
        
        # Procesar resultados para la interfaz
        resultados = self._procesar_resultados_rr()
        
        # Agregar ruta del PDF a los resultados
        if 'ruta_pdf' not in resultados:
            resultados['ruta_pdf'] = None
        
        return resultados
    
    def ejecutar_pe(self, procesos_datos, tiempo_tip, tiempo_tcp, tiempo_tfp):
        """
        Ejecuta el algoritmo de Prioridad Externa (PE) con los datos proporcionados.
        
        Args:
            procesos_datos: Lista de diccionarios con datos de procesos
            tiempo_tip: Tiempo de ingreso de proceso
            tiempo_tcp: Tiempo de conmutación de proceso
            tiempo_tfp: Tiempo de finalización de proceso
            
        Returns:
            Diccionario con resultados de la simulación
        """
        # Convertir datos a instancias de Proceso
        self.procesos = self.crear_procesos_desde_datos(procesos_datos)
        
        # Crear instancia del algoritmo Prioridad Externa
        self.algoritmo_actual = PrioridadExterna(self.procesos, tiempo_tip, tiempo_tcp, tiempo_tfp)
        
        # Ejecutar la simulación
        self.algoritmo_actual.ejecutar()
        
        # Procesar resultados para la interfaz
        resultados = self._procesar_resultados_pe()
        
        # Agregar ruta del PDF a los resultados
        if 'ruta_pdf' not in resultados:
            resultados['ruta_pdf'] = None
        
        return resultados
    
    def _procesar_resultados_fcfs(self):
        """
        Procesa los resultados del algoritmo FCFS para mostrarlos en la interfaz.
        
        Returns:
            Diccionario con datos formateados para la interfaz
        """
        if not self.algoritmo_actual:
            return {}
        
        # Obtener procesos terminados
        procesos_terminados = self.algoritmo_actual.procesos_terminados
        
        # Procesar datos por proceso - ordenar por nombre para mostrar P1, P2, P3, etc.
        datos_procesos = []
        for proceso in sorted(procesos_terminados, key=lambda p: p.nombre):
            datos_procesos.append({
                'nombre': proceso.nombre,
                'tiempo_retorno': proceso.tiempo_retorno,
                'tiempo_retorno_normalizado': round(proceso.tiempo_retorno_normalizado, 2),
                'tiempo_estado_listo': proceso.tiempo_en_listo
            })
        
        # Obtener estadísticas de CPU calculadas correctamente
        stats_cpu = self.algoritmo_actual.obtener_estadisticas_cpu()
        
        # Calcular estadísticas de la tanda
        if procesos_terminados:
            tiempos_retorno = [p.tiempo_retorno for p in procesos_terminados]
            tiempo_medio_retorno = sum(tiempos_retorno) / len(tiempos_retorno)
            tiempo_total = stats_cpu['t_total']
        else:
            tiempo_medio_retorno = 0
            tiempo_total = 0
        
        # Usar estadísticas calculadas correctamente
        tiempo_cpu_procesos = stats_cpu['cpu_proc']
        tiempo_cpu_so = stats_cpu['cpu_so']
        tiempo_cpu_desocupada = stats_cpu['cpu_idle']
        
        # Procesar datos para el diagrama de Gantt
        datos_gantt = self._procesar_datos_gantt()
        
        # Exportar reporte PDF y capturar la ruta
        ruta_pdf = self.exportar_pdf()

        return {
            'procesos': datos_procesos,
            'tiempo_total': tiempo_total,
            'tiempo_medio_retorno': tiempo_medio_retorno,
            'cpu_desocupada': f"{tiempo_cpu_desocupada} ({tiempo_cpu_desocupada/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'cpu_so': f"{tiempo_cpu_so} ({tiempo_cpu_so/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'cpu_procesos': f"{tiempo_cpu_procesos} ({tiempo_cpu_procesos/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'gantt': datos_gantt,
            'eventos': self.algoritmo_actual.resultados,
            'ruta_pdf': ruta_pdf
        }
    
    def _procesar_resultados_spn(self):
        """
        Procesa los resultados del algoritmo SPN para mostrarlos en la interfaz.
        
        Returns:
            Diccionario con datos formateados para la interfaz
        """
        if not self.algoritmo_actual:
            return {}
        
        # Obtener procesos terminados
        procesos_terminados = self.algoritmo_actual.procesos_terminados
        
        # Procesar datos por proceso - ordenar por nombre para mostrar P1, P2, P3, etc.
        datos_procesos = []
        for proceso in sorted(procesos_terminados, key=lambda p: p.nombre):
            datos_procesos.append({
                'nombre': proceso.nombre,
                'tiempo_retorno': proceso.tiempo_retorno,
                'tiempo_retorno_normalizado': round(proceso.tiempo_retorno_normalizado, 2),
                'tiempo_estado_listo': proceso.tiempo_en_listo
            })
        
        # Obtener estadísticas de CPU calculadas correctamente
        stats_cpu = self.algoritmo_actual.obtener_estadisticas_cpu()
        
        # Calcular estadísticas de la tanda
        if procesos_terminados:
            tiempos_retorno = [p.tiempo_retorno for p in procesos_terminados]
            tiempo_medio_retorno = sum(tiempos_retorno) / len(tiempos_retorno)
            tiempo_total = stats_cpu['t_total']
        else:
            tiempo_medio_retorno = 0
            tiempo_total = 0
        
        # Usar estadísticas calculadas correctamente
        tiempo_cpu_procesos = stats_cpu['cpu_proc']
        tiempo_cpu_so = stats_cpu['cpu_so']
        tiempo_cpu_desocupada = stats_cpu['cpu_idle']
        
        # Procesar datos para el diagrama de Gantt
        datos_gantt = self._procesar_datos_gantt()
        
        # Exportar reporte PDF y capturar la ruta
        ruta_pdf = self.exportar_pdf()

        return {
            'procesos': datos_procesos,
            'tiempo_total': tiempo_total,
            'tiempo_medio_retorno': tiempo_medio_retorno,
            'cpu_desocupada': f"{tiempo_cpu_desocupada} ({tiempo_cpu_desocupada/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'cpu_so': f"{tiempo_cpu_so} ({tiempo_cpu_so/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'cpu_procesos': f"{tiempo_cpu_procesos} ({tiempo_cpu_procesos/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'gantt': datos_gantt,
            'eventos': self.algoritmo_actual.resultados,
            'ruta_pdf': ruta_pdf
        }
    
    def _procesar_resultados_srtn(self):
        """
        Procesa los resultados del algoritmo SRTN para mostrarlos en la interfaz.
        
        Returns:
            Diccionario con datos formateados para la interfaz
        """
        if not self.algoritmo_actual:
            return {}
        
        # Obtener procesos terminados
        procesos_terminados = self.algoritmo_actual.procesos_terminados
        
        # Procesar datos por proceso - ordenar por nombre para mostrar P1, P2, P3, etc.
        datos_procesos = []
        for proceso in sorted(procesos_terminados, key=lambda p: p.nombre):
            datos_procesos.append({
                'nombre': proceso.nombre,
                'tiempo_retorno': proceso.tiempo_retorno,
                'tiempo_retorno_normalizado': round(proceso.tiempo_retorno_normalizado, 2),
                'tiempo_estado_listo': proceso.tiempo_en_listo
            })
        
        # Obtener estadísticas de CPU calculadas correctamente
        stats_cpu = self.algoritmo_actual.obtener_estadisticas_cpu()
        
        # Calcular estadísticas de la tanda
        if procesos_terminados:
            tiempos_retorno = [p.tiempo_retorno for p in procesos_terminados]
            tiempo_medio_retorno = sum(tiempos_retorno) / len(tiempos_retorno)
            tiempo_total = stats_cpu['t_total']
        else:
            tiempo_medio_retorno = 0
            tiempo_total = 0
        
        # Usar estadísticas calculadas correctamente
        tiempo_cpu_procesos = stats_cpu['cpu_proc']
        tiempo_cpu_so = stats_cpu['cpu_so']
        tiempo_cpu_desocupada = stats_cpu['cpu_idle']
        
        # Procesar datos para el diagrama de Gantt
        datos_gantt = self._procesar_datos_gantt()
        
        # Exportar reporte PDF y capturar la ruta
        ruta_pdf = self.exportar_pdf()

        return {
            'procesos': datos_procesos,
            'tiempo_total': tiempo_total,
            'tiempo_medio_retorno': tiempo_medio_retorno,
            'cpu_desocupada': f"{tiempo_cpu_desocupada} ({tiempo_cpu_desocupada/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'cpu_so': f"{tiempo_cpu_so} ({tiempo_cpu_so/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'cpu_procesos': f"{tiempo_cpu_procesos} ({tiempo_cpu_procesos/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'gantt': datos_gantt,
            'eventos': self.algoritmo_actual.resultados,
            'ruta_pdf': ruta_pdf
        }
    
    def _procesar_resultados_rr(self):
        """
        Procesa los resultados del algoritmo Round Robin para mostrarlos en la interfaz.
        
        Returns:
            Diccionario con datos formateados para la interfaz
        """
        if not self.algoritmo_actual:
            return {}
        
        # Obtener procesos terminados
        procesos_terminados = self.algoritmo_actual.procesos_terminados
        
        # Procesar datos por proceso - ordenar por nombre para mostrar P1, P2, P3, etc.
        datos_procesos = []
        for proceso in sorted(procesos_terminados, key=lambda p: p.nombre):
            datos_procesos.append({
                'nombre': proceso.nombre,
                'tiempo_retorno': proceso.tiempo_retorno,
                'tiempo_retorno_normalizado': round(proceso.tiempo_retorno_normalizado, 2),
                'tiempo_estado_listo': proceso.tiempo_en_listo
            })
        
        # Obtener estadísticas de CPU calculadas correctamente
        stats_cpu = self.algoritmo_actual.obtener_estadisticas_cpu()
        
        # Calcular estadísticas de la tanda
        if procesos_terminados:
            tiempos_retorno = [p.tiempo_retorno for p in procesos_terminados]
            tiempo_medio_retorno = sum(tiempos_retorno) / len(tiempos_retorno)
            tiempo_total = stats_cpu['t_total']
        else:
            tiempo_medio_retorno = 0
            tiempo_total = 0
        
        # Usar estadísticas calculadas correctamente
        tiempo_cpu_procesos = stats_cpu['cpu_proc']
        tiempo_cpu_so = stats_cpu['cpu_so']
        tiempo_cpu_desocupada = stats_cpu['cpu_idle']
        
        # Procesar datos para el diagrama de Gantt
        datos_gantt = self._procesar_datos_gantt()
        
        # Exportar reporte PDF y capturar la ruta
        ruta_pdf = self.exportar_pdf()

        return {
            'procesos': datos_procesos,
            'tiempo_total': tiempo_total,
            'tiempo_medio_retorno': tiempo_medio_retorno,
            'cpu_desocupada': f"{tiempo_cpu_desocupada} ({tiempo_cpu_desocupada/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'cpu_so': f"{tiempo_cpu_so} ({tiempo_cpu_so/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'cpu_procesos': f"{tiempo_cpu_procesos} ({tiempo_cpu_procesos/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'gantt': datos_gantt,
            'eventos': self.algoritmo_actual.resultados,
            'ruta_pdf': ruta_pdf
        }
    
    def _procesar_resultados_pe(self):
        """
        Procesa los resultados del algoritmo PE para mostrarlos en la interfaz.
        
        Returns:
            Diccionario con datos formateados para la interfaz
        """
        if not self.algoritmo_actual:
            return {}
        
        # Obtener procesos terminados
        procesos_terminados = self.algoritmo_actual.procesos_terminados
        
        # Procesar datos por proceso - ordenar por nombre para mostrar P1, P2, P3, etc.
        datos_procesos = []
        for proceso in sorted(procesos_terminados, key=lambda p: p.nombre):
            datos_procesos.append({
                'nombre': proceso.nombre,
                'tiempo_retorno': proceso.tiempo_retorno,
                'tiempo_retorno_normalizado': round(proceso.tiempo_retorno_normalizado, 2),
                'tiempo_estado_listo': proceso.tiempo_en_listo
            })
        
        # Obtener estadísticas de CPU calculadas correctamente
        stats_cpu = self.algoritmo_actual.obtener_estadisticas_cpu()
        
        # Calcular estadísticas de la tanda
        if procesos_terminados:
            tiempos_retorno = [p.tiempo_retorno for p in procesos_terminados]
            tiempo_medio_retorno = sum(tiempos_retorno) / len(tiempos_retorno)
            tiempo_total = stats_cpu['t_total']
        else:
            tiempo_medio_retorno = 0
            tiempo_total = 0
        
        # Usar estadísticas calculadas correctamente
        tiempo_cpu_procesos = stats_cpu['cpu_proc']
        tiempo_cpu_so = stats_cpu['cpu_so']
        tiempo_cpu_desocupada = stats_cpu['cpu_idle']
        
        # Procesar datos para el diagrama de Gantt
        datos_gantt = self._procesar_datos_gantt()
        
        # Exportar reporte PDF y capturar la ruta
        ruta_pdf = self.exportar_pdf()

        return {
            'procesos': datos_procesos,
            'tiempo_total': tiempo_total,
            'tiempo_medio_retorno': tiempo_medio_retorno,
            'cpu_desocupada': f"{tiempo_cpu_desocupada} ({tiempo_cpu_desocupada/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'cpu_so': f"{tiempo_cpu_so} ({tiempo_cpu_so/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'cpu_procesos': f"{tiempo_cpu_procesos} ({tiempo_cpu_procesos/tiempo_total*100:.1f}%)" if tiempo_total > 0 else "0 (0%)",
            'gantt': datos_gantt,
            'eventos': self.algoritmo_actual.resultados,
            'ruta_pdf': ruta_pdf
        }
    
    def _procesar_datos_gantt(self):
        """
        Procesa los datos para el diagrama de Gantt.
        
        Returns:
            Diccionario con datos del diagrama de Gantt
        """
        if not self.algoritmo_actual:
            return {'procesos': [], 'inicios': [], 'duraciones': []}
        
        # Procesar eventos para crear el diagrama de Gantt
        eventos_ejecucion = []
        
        for evento in self.algoritmo_actual.resultados:
            if evento['evento'] == 'inicio_ejecucion':
                eventos_ejecucion.append({
                    'proceso': evento['proceso'],
                    'inicio': evento['tiempo'],
                    'fin': None  # Se completará cuando termine
                })
            elif evento['evento'] == 'terminacion':
                # Buscar el evento de inicio correspondiente
                for evt in eventos_ejecucion:
                    if evt['proceso'] == evento['proceso'] and evt['fin'] is None:
                        evt['fin'] = evento['tiempo']
                        break
        
        # Crear datos para el diagrama
        procesos = []
        inicios = []
        duraciones = []
        
        for evento in eventos_ejecucion:
            if evento['fin'] is not None:
                procesos.append(evento['proceso'])
                inicios.append(evento['inicio'])
                duraciones.append(evento['fin'] - evento['inicio'])
        
        return {
            'procesos': procesos,
            'inicios': inicios,
            'duraciones': duraciones
        }
    
    def exportar_pdf(self):
        """
        Exporta un reporte PDF con los resultados de la simulación.
        """
        if not hasattr(self, 'algoritmo_actual') or not self.algoritmo_actual:
            return
        
        # Crear directorio de salida si no existe
        if hasattr(sys, '_MEIPASS'):
            # Ejecutable empaquetado - guardar en el directorio del ejecutable
            if hasattr(sys, 'frozen'):
                # PyInstaller
                base_dir = os.path.dirname(sys.executable)
            else:
                # Otro empaquetador
                base_dir = os.path.dirname(sys.executable)
            output_dir = os.path.join(base_dir, 'output')
        else:
            # Desarrollo normal
            output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'output')
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Generar nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_simulacion_{timestamp}.pdf"
        filepath = os.path.join(output_dir, filename)
        
        # Preparar datos para el PDF
        datos_pdf = {
            'tiempo_total': self.algoritmo_actual.tiempo_actual - 1,
            'procesos': [],
            'tiempo_medio_retorno': 0,
            'cpu_desocupada': '0 (0%)',
            'cpu_so': '0 (0%)',
            'cpu_procesos': '0 (0%)',
            'eventos': self.algoritmo_actual.resultados,
            'tip': self.algoritmo_actual.tiempo_tip,
            'tcp': self.algoritmo_actual.tiempo_tcp,
            'tfp': self.algoritmo_actual.tiempo_tfp
        }
        
        # Agregar información de procesos
        for proceso in self.algoritmo_actual.procesos:
            datos_pdf['procesos'].append({
                'nombre': proceso.nombre,
                'tiempo_retorno': proceso.tiempo_retorno,
                'tiempo_retorno_normalizado': proceso.tiempo_retorno_normalizado,
                'tiempo_estado_listo': proceso.tiempo_en_listo
            })
        
        # Calcular tiempo medio de retorno
        if datos_pdf['procesos']:
            tiempos_retorno = [p['tiempo_retorno'] for p in datos_pdf['procesos']]
            datos_pdf['tiempo_medio_retorno'] = sum(tiempos_retorno) / len(tiempos_retorno)
        
        # Obtener estadísticas de CPU calculadas correctamente
        stats_cpu = self.algoritmo_actual.obtener_estadisticas_cpu()
        
        # Usar estadísticas calculadas correctamente
        tiempo_cpu_procesos = stats_cpu['cpu_proc']
        tiempo_cpu_so = stats_cpu['cpu_so']
        tiempo_cpu_desocupada = stats_cpu['cpu_idle']
        
        if datos_pdf['tiempo_total'] > 0:
            datos_pdf['cpu_desocupada'] = f"{tiempo_cpu_desocupada} ({tiempo_cpu_desocupada/datos_pdf['tiempo_total']*100:.1f}%)"
            datos_pdf['cpu_so'] = f"{tiempo_cpu_so} ({tiempo_cpu_so/datos_pdf['tiempo_total']*100:.1f}%)"
            datos_pdf['cpu_procesos'] = f"{tiempo_cpu_procesos} ({tiempo_cpu_procesos/datos_pdf['tiempo_total']*100:.1f}%)"
        
        # Crear exportador PDF
        exportador = ExportadorPDF()
        
        # Exportar PDF
        try:
            ruta_pdf = exportador.exportar_simulacion(datos_pdf, filepath)
            print(f"✅ Reporte PDF exportado a: {ruta_pdf}")
            return ruta_pdf
        except Exception as e:
            print(f"❌ Error al exportar PDF: {e}")
            return None
