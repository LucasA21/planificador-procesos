"""
Módulo para exportar resultados de simulación a PDF usando ReportLab.
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF


class ExportadorPDF:
    """Clase para exportar resultados de simulación a PDF."""
    
    def __init__(self, factor_escala=1.0):
        self.factor_escala = factor_escala
        self.estilos = getSampleStyleSheet()
        self._configurar_estilos()
    
    def _configurar_estilos(self):
        """Configura los estilos personalizados para el PDF."""
        # Estilo para títulos principales
        self.estilos.add(ParagraphStyle(
            name='TituloPrincipal',
            parent=self.estilos['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2B2B2B')
        ))
        
        # Estilo para subtítulos
        self.estilos.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.estilos['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#404040')
        ))
        
        # Estilo para texto normal
        self.estilos.add(ParagraphStyle(
            name='TextoNormal',
            parent=self.estilos['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=colors.HexColor('#666666')
        ))
        
        # Estilo para texto de código
        self.estilos.add(ParagraphStyle(
            name='Codigo',
            parent=self.estilos['Code'],
            fontSize=9,
            fontName='Courier',
            textColor=colors.HexColor('#333333')
        ))
    
    def exportar_simulacion(self, datos_simulacion, ruta_archivo=None):
        """
        Exporta los resultados de la simulación a un archivo PDF.
        
        Args:
            datos_simulacion: Diccionario con los datos de la simulación
            ruta_archivo: Ruta donde guardar el PDF (opcional)
            
        Returns:
            str: Ruta del archivo generado
        """
        if ruta_archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta_archivo = f"reporte_simulacion_{timestamp}.pdf"
        
        # Crear directorio si no existe
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        # Crear documento PDF
        doc = SimpleDocTemplate(
            ruta_archivo,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Construir contenido
        contenido = []
        contenido.extend(self._crear_portada(datos_simulacion))
        contenido.append(PageBreak())
        contenido.extend(self._crear_tabla_eventos(datos_simulacion))
        contenido.append(PageBreak())
        contenido.extend(self._crear_estadisticas_procesos(datos_simulacion))
        contenido.append(PageBreak())
        contenido.extend(self._crear_diagrama_gantt(datos_simulacion))
        
        # Generar PDF
        doc.build(contenido)
        
        return ruta_archivo
    
    def _crear_portada(self, datos):
        """Crea la portada del reporte."""
        contenido = []
        
        # Título principal
        titulo = Paragraph("Reporte de Simulación", self.estilos['TituloPrincipal'])
        contenido.append(titulo)
        contenido.append(Spacer(1, 30))
        
        # Información de la simulación
        info_data = [
            ['Fecha de Simulación', datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
            ['Tiempo Total', f"{datos.get('tiempo_total', 0)} unidades de tiempo"],
            ['Procesos Simulados', f"{len(datos.get('procesos', []))} procesos"],
            ['TR Medio', f"{datos.get('tiempo_medio_retorno', 0):.2f}"],
            ['TIP', f"{datos.get('tip', 0)}"],
            ['TCP', f"{datos.get('tcp', 0)}"],
            ['TFP', f"{datos.get('tfp', 0)}"],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F5F5')),
        ]))
        
        contenido.append(info_table)
        
        return contenido
    
    
    def _crear_tabla_eventos(self, datos):
        """Crea la tabla de eventos de la simulación."""
        contenido = []
        
        # Título de sección
        titulo = Paragraph("Cronología de Eventos", self.estilos['Subtitulo'])
        contenido.append(titulo)
        contenido.append(Spacer(1, 20))
        
        # Obtener eventos
        eventos = datos.get('eventos', [])
        if not eventos:
            contenido.append(Paragraph("No hay eventos registrados.", self.estilos['TextoNormal']))
            return contenido
        
        # Crear tabla de eventos
        headers = ['Tiempo', 'Proceso', 'Evento', 'Estado']
        tabla_data = [headers]
        
        for evento in eventos:
            fila = [
                str(evento.get('tiempo', '')),
                evento.get('proceso', ''),
                evento.get('evento', ''),
                evento.get('estado', '')
            ]
            tabla_data.append(fila)
        
        # Crear tabla
        tabla = Table(tabla_data, colWidths=[0.8*inch, 1*inch, 2*inch, 1.5*inch])
        
        # Estilos de la tabla
        estilos_tabla = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E9ECEF')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ]
        
        # Aplicar colores según el tipo de evento (coincidiendo con el Gantt)
        for i, evento in enumerate(eventos, 1):
            tipo_evento = evento.get('evento', '')
            
            # Colores que coinciden con el diagrama de Gantt
            if tipo_evento == 'llegada':
                estilos_tabla.append(('TEXTCOLOR', (0, i), (3, i), colors.HexColor('#17A2B8')))  # Azul claro
            elif tipo_evento == 'listo':
                estilos_tabla.append(('TEXTCOLOR', (0, i), (3, i), colors.HexColor('#20C997')))  # Verde claro
            elif tipo_evento in ['inicio ejecucion', 'inicio_ejecucion', 'fin ejecucion', 'fin_ejecucion']:
                estilos_tabla.append(('TEXTCOLOR', (0, i), (3, i), colors.HexColor('#28A745')))  # Verde
            elif tipo_evento == 'inicio_io':
                estilos_tabla.append(('TEXTCOLOR', (0, i), (3, i), colors.HexColor('#DC3545')))  # Rojo
            elif tipo_evento == 'fin_io':
                estilos_tabla.append(('TEXTCOLOR', (0, i), (3, i), colors.HexColor('#B02A37')))  # Rojo más oscuro
            elif tipo_evento in ['inicio_tip', 'fin_tip']:
                estilos_tabla.append(('TEXTCOLOR', (0, i), (3, i), colors.HexColor('#6C757D')))  # Gris
            elif tipo_evento in ['inicio_tcp', 'fin_tcp']:
                estilos_tabla.append(('TEXTCOLOR', (0, i), (3, i), colors.HexColor('#E83E8C')))  # Magenta
            elif tipo_evento in ['inicio_tfp', 'fin_tfp']:
                estilos_tabla.append(('TEXTCOLOR', (0, i), (3, i), colors.HexColor('#FFC107')))  # Amarillo
            elif tipo_evento == 'bloqueo':
                estilos_tabla.append(('TEXTCOLOR', (0, i), (3, i), colors.HexColor('#DC3545')))  # Rojo (mismo que I/O)
            elif tipo_evento == 'terminacion':
                estilos_tabla.append(('TEXTCOLOR', (0, i), (3, i), colors.HexColor('#28A745')))  # Verde (mismo que ejecución)
        
        tabla.setStyle(TableStyle(estilos_tabla))
        contenido.append(tabla)
        
        return contenido
    
    def _crear_estadisticas_procesos(self, datos):
        """Crea la tabla de estadísticas por proceso."""
        contenido = []
        
        # Título de sección
        titulo = Paragraph("Estadísticas por Proceso", self.estilos['Subtitulo'])
        contenido.append(titulo)
        contenido.append(Spacer(1, 20))
        
        # Obtener procesos
        procesos = datos.get('procesos', [])
        if not procesos:
            contenido.append(Paragraph("No hay procesos para mostrar.", self.estilos['TextoNormal']))
            return contenido
        
        # Crear tabla de procesos
        headers = ['Proceso', 'Tiempo Retorno', 'T. Retorno Norm.', 'Tiempo en Listo']
        tabla_data = [headers]
        
        for proceso in procesos:
            fila = [
                proceso.get('nombre', ''),
                str(proceso.get('tiempo_retorno', 0)),
                f"{proceso.get('tiempo_retorno_normalizado', 0):.2f}",
                str(proceso.get('tiempo_estado_listo', 0))
            ]
            tabla_data.append(fila)
        
        # Crear tabla
        tabla = Table(tabla_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        
        # Estilos de la tabla
        estilos_tabla = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E9ECEF')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ]
        
        tabla.setStyle(TableStyle(estilos_tabla))
        contenido.append(tabla)
        
        return contenido
    
    def _crear_diagrama_gantt(self, datos):
        """Crea un diagrama de Gantt de la simulación."""
        contenido = []
        
        # Título de sección
        titulo = Paragraph("Diagrama de Gantt", self.estilos['Subtitulo'])
        contenido.append(titulo)
        contenido.append(Spacer(1, 20))
        
        # Obtener eventos
        eventos = datos.get('eventos', [])
        if not eventos:
            contenido.append(Paragraph("No hay eventos para mostrar en el diagrama de Gantt.", self.estilos['TextoNormal']))
            return contenido
        
        # Procesar eventos para crear el diagrama
        procesos_gantt = self._procesar_eventos_gantt(eventos)
        
        if not procesos_gantt:
            contenido.append(Paragraph("No se pudieron procesar los eventos para el diagrama de Gantt.", self.estilos['TextoNormal']))
            return contenido
        
        # Crear el diagrama de Gantt (dividido en segmentos de 30 unidades)
        gantt_tables = self._construir_tabla_gantt(procesos_gantt, datos.get('tiempo_total', 0))
        
        # Agregar cada segmento
        for i, tabla in enumerate(gantt_tables):
            if i > 0:  # Agregar espacio entre segmentos
                contenido.append(Spacer(1, 20))
            
            # Calcular rango del segmento
            inicio = i * 30
            fin = min(inicio + 29, datos.get('tiempo_total', 0))
            
            contenido.append(Paragraph("Segmento {} ({}-{})".format(i + 1, inicio, fin), self.estilos['Subtitulo']))
            contenido.append(Spacer(1, 10))
            contenido.append(tabla)
        
        # Agregar leyenda
        contenido.append(Spacer(1, 20))
        contenido.extend(self._crear_leyenda_gantt())
        
        return contenido
    
    def _procesar_eventos_gantt(self, eventos):
        """Procesa los eventos para crear el diagrama de Gantt según las especificaciones del usuario."""
        procesos = {}
        primer_proceso = None
        tiempo_primer_llegada = float('inf')
        
        # Primera pasada: identificar todos los procesos y sus llegadas
        for evento in eventos:
            proceso_nombre = evento.get('proceso', '')
            tiempo = evento.get('tiempo', 0)
            tipo_evento = evento.get('evento', '')
            
            if proceso_nombre != 'SISTEMA' and tipo_evento == 'llegada':
                if proceso_nombre not in procesos:
                    procesos[proceso_nombre] = {
                        'llegada': tiempo,
                        'segmentos': []
                    }
                    # Identificar el primer proceso que llega
                    if tiempo < tiempo_primer_llegada:
                        tiempo_primer_llegada = tiempo
                        primer_proceso = proceso_nombre
        
        # Segunda pasada: procesar eventos de TIP, TCP, TFP (ahora con nombres de procesos correctos)
        eventos_sistema = {}
        
        for evento in eventos:
            proceso_nombre = evento.get('proceso', '')
            tiempo = evento.get('tiempo', 0)
            tipo_evento = evento.get('evento', '')
            
            # Procesar eventos de TIP, TCP, TFP (ya no son del sistema, sino del proceso específico)
            if tipo_evento in ['inicio_tip', 'inicio_tcp', 'inicio_tfp']:
                if proceso_nombre in procesos:
                    eventos_sistema[tipo_evento] = {
                        'tiempo': tiempo,
                        'proceso': proceso_nombre
                    }
            elif tipo_evento in ['fin_tip', 'fin_tcp', 'fin_tfp']:
                # Buscar el evento de inicio correspondiente
                evento_inicio = tipo_evento.replace('fin_', 'inicio_')
                if evento_inicio in eventos_sistema:
                    evento_sistema = eventos_sistema[evento_inicio]
                    proceso_destino = evento_sistema['proceso']
                    
                    if proceso_destino and proceso_destino in procesos:
                        if tipo_evento == 'fin_tfp':
                            # Para TFP: pintar desde inicio_tfp+1 hasta fin_tfp
                            inicio = evento_sistema['tiempo'] + 1
                            fin = tiempo
                            
                            # Solo pintar si hay duración
                            if inicio <= fin:
                                procesos[proceso_destino]['segmentos'].append({
                                    'inicio': inicio,
                                    'tipo': evento_inicio,
                                    'fin': fin
                                })
                        else:
                            # Para TIP y TCP: pintar desde inicio hasta fin-1
                            inicio = evento_sistema['tiempo']
                            fin = tiempo - 1  # fin_tip en tiempo X significa que dura hasta X-1
                            
                            # Solo pintar si hay duración
                            if inicio <= fin:
                                procesos[proceso_destino]['segmentos'].append({
                                    'inicio': inicio,
                                    'tipo': evento_inicio,
                                    'fin': fin
                                })
                    
                    # Limpiar el evento del sistema
                    del eventos_sistema[evento_inicio]
        
        # Tercera pasada: procesar eventos de procesos
        for evento in eventos:
            proceso_nombre = evento.get('proceso', '')
            tiempo = evento.get('tiempo', 0)
            tipo_evento = evento.get('evento', '')
            
            # Saltar eventos del sistema y eventos de TIP, TCP, TFP (ya procesados)
            if proceso_nombre == 'SISTEMA' or tipo_evento in ['inicio_tip', 'inicio_tcp', 'inicio_tfp', 'fin_tip', 'fin_tcp', 'fin_tfp']:
                continue
            
            if proceso_nombre not in procesos:
                procesos[proceso_nombre] = {
                    'llegada': None,
                    'segmentos': []
                }
            
            if tipo_evento == 'llegada':
                procesos[proceso_nombre]['llegada'] = tiempo
            elif tipo_evento == 'inicio ejecucion':
                procesos[proceso_nombre]['segmentos'].append({
                    'inicio': tiempo,
                    'tipo': tipo_evento,
                    'fin': None
                })
            elif tipo_evento in ['fin ejecucion', 'fin_ejecucion']:
                # Buscar el segmento de ejecución para cerrarlo
                for segmento in reversed(procesos[proceso_nombre]['segmentos']):
                    if segmento['fin'] is None and segmento['tipo'] == 'inicio ejecucion':
                        segmento['fin'] = tiempo
                        break
            elif tipo_evento == 'inicio_io':
                # Agregar segmento de I/O que empieza en inicio_io
                procesos[proceso_nombre]['segmentos'].append({
                    'inicio': tiempo,  # I/O empieza en inicio_io
                    'tipo': 'inicio_io',
                    'fin': None
                })
            elif tipo_evento == 'fin_io':
                # Buscar el segmento de I/O para cerrarlo
                for segmento in reversed(procesos[proceso_nombre]['segmentos']):
                    if segmento['fin'] is None and segmento['tipo'] == 'inicio_io':
                        segmento['fin'] = tiempo  # I/O termina en fin_io (inclusive)
                        break
            elif tipo_evento == 'terminacion':
                # Buscar el segmento de ejecución para cerrarlo (usando fin ejecucion)
                for segmento in reversed(procesos[proceso_nombre]['segmentos']):
                    if segmento['fin'] is None and segmento['tipo'] == 'inicio ejecucion':
                        segmento['fin'] = tiempo
                        break
                # Marcar que el proceso terminó en este tiempo
                if proceso_nombre not in procesos:
                    procesos[proceso_nombre] = {'llegada': None, 'segmentos': []}
                procesos[proceso_nombre]['terminacion'] = tiempo
        
        return procesos
    
    def _encontrar_proceso_destino(self, eventos, tiempo_inicio):
        """Encuentra el proceso que va a ejecutarse después de un evento del sistema."""
        for evento in eventos:
            if (evento.get('tiempo', 0) >= tiempo_inicio and 
                evento.get('evento') in ['inicio ejecucion', 'inicio_ejecucion']):
                return evento.get('proceso', '')
        return None
    
    def _construir_tabla_gantt(self, procesos_gantt, tiempo_total):
        """Construye la tabla del diagrama de Gantt dividida en segmentos de 30 unidades."""
        tablas = []
        segmento_size = 30
        
        # Calcular cuántos segmentos necesitamos
        num_segmentos = (tiempo_total // segmento_size) + 1
        
        for i in range(num_segmentos):
            inicio = i * segmento_size
            fin = min(inicio + segmento_size - 1, tiempo_total)
            
            if inicio <= tiempo_total:  # Solo crear segmento si hay tiempo que mostrar
                titulo = "Segmento {} ({}-{})".format(i + 1, inicio, fin)
                tabla = self._crear_tabla_gantt_parte(procesos_gantt, inicio, fin, titulo)
                tablas.append(tabla)
        
        return tablas
    
    def _crear_tabla_gantt_parte(self, procesos_gantt, inicio_tiempo, fin_tiempo, titulo):
        """Crea una parte del diagrama de Gantt."""
        # Crear filas del diagrama
        filas = []
        
        # Encabezado con números de tiempo
        encabezado = ['Proceso'] + [str(i) for i in range(inicio_tiempo, fin_tiempo + 1)]
        filas.append(encabezado)
        
        # Ordenar procesos por nombre
        procesos_ordenados = sorted(procesos_gantt.items())
        
        for proceso_nombre, datos_proceso in procesos_ordenados:
            if proceso_nombre == 'SISTEMA':
                continue
                
            fila = [proceso_nombre]
            
            # Crear la fila de tiempo para este proceso
            for tiempo in range(inicio_tiempo, fin_tiempo + 1):
                celda = self._determinar_contenido_celda_gantt(tiempo, datos_proceso)
                # Solo mostrar texto si es 'F' de terminación, sino mostrar vacío
                if celda == 'F':
                    fila.append(celda)
                else:
                    fila.append('')
            
            filas.append(fila)
        
        # Crear tabla con anchos ajustados
        ancho_proceso = 0.8*inch
        ancho_tiempo = 0.15*inch  # Ancho fijo para cada columna de tiempo (30 columnas máximo)
        tabla = Table(filas, colWidths=[ancho_proceso] + [ancho_tiempo] * (fin_tiempo - inicio_tiempo + 1))
        
        # Estilos de la tabla
        estilos = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E9ECEF')),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#F8F9FA')),
        ]
        
        # Aplicar colores a las celdas según el contenido (sin texto)
        for i, fila in enumerate(filas[1:], 1):  # Saltar encabezado
            proceso_nombre = fila[0]
            datos_proceso = procesos_gantt[proceso_nombre]
            
            for j, tiempo in enumerate(range(inicio_tiempo, fin_tiempo + 1), 1):
                celda_tipo = self._determinar_contenido_celda_gantt(tiempo, datos_proceso)
                
                if celda_tipo == 'CPU':
                    estilos.append(('BACKGROUND', (j, i), (j, i), colors.HexColor('#28A745')))  # Verde
                elif celda_tipo == 'I/O':
                    estilos.append(('BACKGROUND', (j, i), (j, i), colors.HexColor('#DC3545')))  # Rojo
                elif celda_tipo == 'TIP':
                    estilos.append(('BACKGROUND', (j, i), (j, i), colors.HexColor('#6C757D')))  # Gris
                elif celda_tipo == 'TCP':
                    estilos.append(('BACKGROUND', (j, i), (j, i), colors.HexColor('#E83E8C')))  # Magenta
                elif celda_tipo == 'TFP':
                    estilos.append(('BACKGROUND', (j, i), (j, i), colors.HexColor('#FFC107')))  # Amarillo
                elif celda_tipo == 'F':
                    estilos.append(('BACKGROUND', (j, i), (j, i), colors.HexColor('#28A745')))  # Verde (mismo que CPU)
        
        tabla.setStyle(TableStyle(estilos))
        return tabla
    
    def _determinar_contenido_celda_gantt(self, tiempo, datos_proceso):
        """Determina qué mostrar en cada celda del diagrama de Gantt."""
        # Verificar segmentos activos en este tiempo
        for segmento in datos_proceso['segmentos']:
            # Si el segmento no tiene fin definido, solo verificar si el tiempo es >= inicio
            if segmento['fin'] is None:
                if tiempo >= segmento['inicio']:
                    tipo = segmento['tipo']
                    if tipo == 'inicio ejecucion':
                        return 'CPU'
                    elif tipo == 'inicio_tip':
                        return 'TIP'
                    elif tipo == 'inicio_tcp':
                        return 'TCP'
                    elif tipo == 'inicio_tfp':
                        return 'TFP'
                    elif tipo == 'bloqueo' or tipo == 'inicio_io':
                        return 'I/O'
            else:
                # Si el segmento tiene fin definido, verificar si el tiempo está en el rango
                if segmento['inicio'] <= tiempo <= segmento['fin']:
                    tipo = segmento['tipo']
                    # Verificar si es el último tiempo de un segmento de ejecución y hay terminación
                    if (tipo == 'inicio ejecucion' and 
                        'terminacion' in datos_proceso and 
                        datos_proceso['terminacion'] == tiempo):
                        return 'F'
                    elif tipo == 'inicio ejecucion':
                        return 'CPU'
                    elif tipo == 'inicio_tip':
                        return 'TIP'
                    elif tipo == 'inicio_tcp':
                        return 'TCP'
                    elif tipo == 'inicio_tfp':
                        return 'TFP'
                    elif tipo == 'bloqueo' or tipo == 'inicio_io':
                        return 'I/O'
        
        return ''
    
    def _crear_leyenda_gantt(self):
        """Crea la leyenda para el diagrama de Gantt."""
        contenido = []
        
        # Título de la leyenda
        titulo_leyenda = Paragraph("Leyenda:", self.estilos['Subtitulo'])
        contenido.append(titulo_leyenda)
        contenido.append(Spacer(1, 10))
        
        # Datos de la leyenda
        leyenda_data = [
            ['Símbolo', 'Descripción'],
            ['*', 'Llegada del proceso'],
            ['CPU', 'Ejecución de CPU'],
            ['I/O', 'Operación de Entrada/Salida'],
            ['TIP', 'Tiempo de Inicio de Proceso'],
            ['TCP', 'Tiempo de Cambio de Proceso'],
            ['TFP', 'Tiempo de Finalización de Proceso'],
            ['F', 'Proceso terminado'],
        ]
        
        leyenda_table = Table(leyenda_data, colWidths=[0.8*inch, 3*inch])
        leyenda_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E9ECEF')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
            # Colores para los símbolos
            ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#17A2B8')),  # Azul claro para *
            ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#28A745')),  # Verde para CPU
            ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#DC3545')),  # Rojo para I/O
            ('BACKGROUND', (0, 4), (0, 4), colors.HexColor('#6C757D')),  # Gris para TIP
            ('BACKGROUND', (0, 5), (0, 5), colors.HexColor('#E83E8C')),  # Magenta para TCP
            ('BACKGROUND', (0, 6), (0, 6), colors.HexColor('#FFC107')),  # Amarillo para TFP
            ('BACKGROUND', (0, 7), (0, 7), colors.HexColor('#28A745')),  # Verde para F
        ]))
        
        contenido.append(leyenda_table)
        
        return contenido
