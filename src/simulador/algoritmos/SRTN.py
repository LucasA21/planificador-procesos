class SRTN:
    def __init__(self, procesos, tiempo_tip, tiempo_tcp, tiempo_tfp):
        
        # Lista de procesos
        self.procesos = procesos
        # Instante de tiempo actual
        self.tiempo_actual = 0
        # Proceso ejectuando tiempo actual
        self.proceso_actual = None

        # Colas
        self.cola_listos = []
        self.procesos_bloqueados = []
        self.procesos_terminados = []

        # Lista de eventos
        self.resultados = []

        # Tiempos consumidos por el Sistema Operativo
        self.tiempo_tip = tiempo_tip
        self.tiempo_tcp = tiempo_tcp
        self.tiempo_tfp = tiempo_tfp
        self.tipo_bloqueo = None
        self.tiempo_restante_bloqueo = 0

        # Contadores de CPU
        self.cpu_proc = 0 # Tiempo CPU ejecutando procesos
        self.cpu_so = 0   # Tiempo CPU consumido por el SO
        self.cpu_idle = 0 # Tiempo CPU desocupada

        # Contadores por proceso
        self.cpu_proc_por_proceso = {}
        self.t_arribo_por_proceso = {}
        self.t_fin_por_proceso = {}
        self.t_listo_por_proceso = {}

        # Tiempos para calculos
        self.t_primer_arribo = None
        self.t_ultimo_tfp = None



    def insertar_ordenado(self,proceso):
        # Si la cola esta vacia metemos
        if len(self.cola_listos) == 0:
            self.cola_listos.append(proceso)
            return
        
        # Ordenar por duracion de rafaga (menor primero)
        duracion_proceso = proceso.get_duracion_rafagas_cpu()

        for i, proceso_en_cola in enumerate(self.cola_listos):
            duracion_en_cola = proceso_en_cola.get_duracion_rafagas_cpu()

            if duracion_proceso < duracion_en_cola:
                # Insertar antes del proceso actual
                self.cola_listos.insert(i,proceso)
                return

        self.cola_listos.append(proceso)





    def procesar_llegadas(self):
        # Recorrer lista de procesos arrivados y los inserta en la lista
        for proceso in self.procesos:
            if proceso.tiempo_arrivo == self.tiempo_actual:
                self.insertar_ordenado(proceso)
                proceso.estado = "listo"

                # Registrar el primer arrivo
                if self.t_primer_arribo is None:
                    self.t_primer_arribo = self.tiempo_actual

                # Registrar tiempo de arribo
                self.t_arribo_por_proceso[proceso.nombre] = self.tiempo_actual
                self.cpu_proc_por_proceso[proceso.nombre] = 0
                self.t_listo_por_proceso[proceso.nombre] = 0

                # Registrar evento arrivo
                self.resultados.append({
                    'tiempo': self.tiempo_actual,
                    'proceso': proceso.nombre,
                    'evento': 'llegada',
                    'estado': 'arrivo'
                }) 

    '''
    Mientras queden procesos pendientes:
        - Procesar nuevos arrivos
        - Procesar tiempos de TIP/TCP/TFP
        - Incrementar tiempo espera de procesos listos no ejecutados
        - Ejecutar un proceso
        - Registrar cpu desocupada (si es el caso)
        - Avanzar un tiempo
    '''
    def ejecutar(self):
        
        while self.hay_procesos_pendientes():
            
            self.procesar_llegadas()

            # Procesar tiempo de TIP/TCP/TFP
            if self.procesar_tiempo_bloqueo():
                self.procesar_procesos_bloqueados()
                self.tiempo_actual +=1
                continue

            # Incrementar tiempo espera a procesos en cola de listos
            for proceso in self.cola_listos:
                proceso.tiempo_en_listo += 1

                if proceso.nombre in self.t_listo_por_proceso:
                    self.t_listo_por_proceso[proceso.nombre] =+ 1

            # Ejecutar un proceso, si no hay ningun ejecutandose
            if self.proceso_actual is None:
                self.seleccionar_siguiente_proceso()

            # Si hay proceso ejecutandose
            if self.proceso_actual is not None:
                self.ejecutar_proceso_actual()

            self.procesar_procesos_bloqueados()

            # Cpu desocupada
            if (self.proceso_actual is None and 
                self.tiempo_restante_bloqueo == 0 and
                len(self.cola_listos) == 0):

                self.cpu_idle += 1

            # Avanzar un tiempo
            self.tiempo_actual += 1

    def ejecutar_proceso_actual(self):
        if self.proceso_actual is None:
            return
        
        self.proceso_actual.duracion_rafagas_cpu -= 1
        self.cpu_proc += 1
        self.cpu_proc_por_proceso[self.proceso_actual.nombre] += 1

        if self.proceso_actual.duracion_rafagas_cpu == 0:
            self.proceso_actual.cantidad_rafagas_cpu -= 1
        
            if self.proceso_actual.cantidad_rafagas_cpu == 0:
                self.terminar_proceso()
            else:
                self.bloquear_proceso()

    def seleccionar_siguiente_proceso(self):
        if len(self.cola_listos) > 0:
            self.proceso_actual = self.cola_listos.pop(0)

            if self.proceso_actual.proceso_nuevo:
                self.aplicar_tip()
                self.proceso_actual.proceso_nuevo = False
            else:
                self.aplicar_tcp()

    def hay_procesos_pendientes(self):
        resultado = (len(self.cola_listos) > 0 
        or len(self.procesos_bloqueados) > 0 
        or (self.proceso_actual is not None)
        or (any(p.tiempo_arrivo > self.tiempo_actual for p in self.procesos))
        or (any(p.estado == "terminado" for p in self.procesos)))

        return resultado

    def bloquear_proceso(self):
        # Guardar tiempo de bloqueo y duracion original de I/O
        self.proceso_actual.tiempo_bloqueo = self.tiempo_actual
                
        # Reiniciar duracion rafaga de I/O para la siguiente vez
        self.proceso_actual.duracion_rafagas_io_original = self.proceso_actual.get_duracion_rafagas_io()
        self.proceso_actual.duracion_rafagas_io = self.proceso_actual.duracion_rafagas_io_original

        self.proceso_actual.estado = "bloqueado"
        self.procesos_bloqueados.append(self.proceso_actual)

        # Registrar evento de fin de ejecución
        self.resultados.append({
            'tiempo': self.tiempo_actual,
            'proceso': self.proceso_actual.nombre,
            'evento': 'fin_ejecucion',
            'estado': 'ejecutando'
        })

        # Registrar evento de bloqueo
        self.resultados.append({
            'tiempo': self.tiempo_actual,
            'proceso': self.proceso_actual.nombre,
            'evento': 'bloqueo',
            'estado': 'bloqueado'
        })

        # Registrar evento de inicio de I/O en el siguiente tiempo (si hay duración de I/O)
        if self.proceso_actual.duracion_rafagas_io > 0:
            self.resultados.append({
                'tiempo': self.tiempo_actual + 1,
                'proceso': self.proceso_actual.nombre,
                'evento': 'inicio_io',
                'estado': 'bloqueado'
            })

        self.proceso_actual = None


    def procesar_procesos_bloqueados(self):
        procesos_que_terminarion_io = []

        for proceso in self.procesos_bloqueados:
            if proceso.tiempo_bloqueo < self.tiempo_actual:
                proceso.duracion_rafaga_io -= 1

                if proceso.duracion_rafaga_io == 0:
                    pass


    def obtener_estadisticas_cpu(self):
        # Calcular T_total = t_ultimo_TFP - t_primer_arribo
        if (self.t_primer_arribo is not None) and (self.t_ultimo_tfp is not None):
            t_total = self.t_ultimo_tfp - self.t_primer_arribo
        elif self.t_primer_arribo is not None:
            t_total = self.tiempo_actual - self.t_primer_arribo
        else:
            t_total = 0

        # Calcular CPU_idle
        cpu_idle_calculado = t_total - (self.cpu_proc + self.cpu_so)

        return {
            'cpu_proc': self.cpu_proc,
            'cpu_so': self.cpu_so,
            'cpu_idle': max(0, cpu_idle_calculado),
            't_total': t_total,
            't_primer_arribo': self.t_primer_arribo,
            't_ultimo_tfp': self.t_ultimo_tfp,
            'cpu_proc_por_proceso': self.cpu_proc_por_proceso,
            't_arribo_por_proceso': self.t_arribo_por_proceso,
            't_fin_por_proceso': self.t_fin_por_proceso,
            't_listo_por_proceso': self.t_listo_por_proceso
        }