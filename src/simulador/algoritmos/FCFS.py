"""
Implementacion del algoritmo FCFS (First Come First Served).

Este algoritmo es el mas sencillo:
- Debe fijarse en la cola de listos cual es el proceso que arribo primero
- Una vez se selecciona el proceso puede largarlo a ejecutar
- Para ejecutarlo primero debe consumir el TIP (este atributo va a ser puesto por el usuario), el TIP es el tiempo de ingreso del proceso,
se va a consumir solo la primera vez que un proceso pasa de nuevo a listo, si el proceso se bloquea y vuelve a entrar a la cola de listos no se consume
- Luego se va a ejecutar la rafaga de cpu pertinente (tambien puesto por el usuario)
- Cuando termine de ejecutarse la rafaga, se va a ejecutar la rafaga de I/O (tambien proporcionada por el usuario), la rafaga de I/O se va a ejecutar
siempre mientras el valor de la rafaga de I/O sea mayor que 0 y se haya terminado de ejecutar la rafaga.
- El proceso se va a ejecutar hasta que termine su tiempo total de cpu (tambien introducido por el usuario), este tiempo total no es lo mismo que la rafaga
de cpu, ejemplo: un proceso puede ejecutar a la vez 3 rafagas de cpu y el tiempo total para que finalize es de 12 rafagas, por lo cual debera ejecutarse
4 veces para terminar, y cada vez que se bloquee por que su burst time(rafagas que puede hacer) se termine, se bloquea haciendo las rafagas de I/O
- Cada vez que se se ejecute un proceso, se debe consumir el TCP, esto se consume cada vez que el planificador cambia de un proceso a otro (al principio, 
cuando un proceso es nuevo es decir pasa de nuevo a listo, el tcp no se consume, si no que se consume el tip).
"""
from ..proceso import Proceso


class FCFS:
    def __init__(self, procesos, tiempo_tip, tiempo_tcp, tiempo_tfp):
        self.procesos = procesos
        # Instante de tiempo actual del puntero
        self.tiempo_actual = 0
        # No hay procesos ejecutandose en la primera instancia de tiempo
        self.proceso_actual = None
        # Colas vacias
        self.cola_listos = []
        self.procesos_bloqueados = []
        self.procesos_terminados = []
        # Lista para guardar los eventos que fueron sucediendo
        self.resultados = []

        self.tiempo_tip = tiempo_tip
        self.tiempo_tcp = tiempo_tcp
        self.tiempo_tfp = tiempo_tfp

        self.tiempo_restante_bloqueo = 0
        self.tipo_bloqueo = None
        
        # Contadores de CPU para mediciones correctas
        self.cpu_proc = 0  # Tiempo real de CPU ejecutando procesos
        self.cpu_so = 0    # Tiempo real de CPU en labores del SO
        self.cpu_idle = 0  # Tiempo real de CPU desocupada
        
        # Tiempos de referencia para cálculos
        self.t_primer_arribo = None
        self.t_ultimo_tfp = None
        
        # Contadores por proceso
        self.cpu_proc_por_proceso = {}
        self.t_arribo_por_proceso = {}
        self.t_fin_por_proceso = {}
        self.t_listo_por_proceso = {}

    def procesar_llegadas(self):
        for proceso in self.procesos:
            if proceso.tiempo_arrivo == self.tiempo_actual:
                self.insertar_ordenado(proceso)
                proceso.estado = "listo"
                
                # Registrar primer arribo
                if self.t_primer_arribo is None:
                    self.t_primer_arribo = self.tiempo_actual
                
                # Registrar tiempo de arribo del proceso
                self.t_arribo_por_proceso[proceso.nombre] = self.tiempo_actual
                self.cpu_proc_por_proceso[proceso.nombre] = 0
                self.t_listo_por_proceso[proceso.nombre] = 0

                # Registrar eventos
                self.resultados.append({
                    'tiempo': self.tiempo_actual,
                    'proceso': proceso.nombre,
                    'evento': 'llegada',
                    'estado': 'arrivo'
                })

    def insertar_ordenado(self, proceso):
        """
        Inserta el proceso en la cola de listos, manteniendo el orden
        de arrivo de FCFS
        """
        if len(self.cola_listos) == 0:
            self.cola_listos.append(proceso)
            return

        for i, proceso_en_cola in enumerate(self.cola_listos):
            if proceso.tiempo_arrivo < proceso_en_cola.tiempo_arrivo:
                # Insertar antes del proceso actual
                self.cola_listos.insert(i, proceso)
                return

        self.cola_listos.append(proceso)


    def ejecutar(self):
        # Límite de seguridad para evitar bucles infinitos
        tiempo_maximo = 1000
        iteraciones = 0

        while self.hay_procesos_pendientes() and iteraciones < tiempo_maximo:
            iteraciones += 1

            self.procesar_llegadas()

            # Procesar tiempo de TIP/TCP/TFP
            if self.procesar_tiempo_bloqueo():
                # Procesar procesos bloqueados incluso si hay TIP/TCP/TFP activo
                self.procesar_procesos_bloqueados()
                self.tiempo_actual += 1
                continue

            # Incrementar tiempo de espera para procesos en cola de listos
            for proceso in self.cola_listos:
                proceso.tiempo_en_listo += 1
                # Acumular tiempo en estado listo (solo después de pagar TIP)
                if proceso.nombre in self.t_listo_por_proceso:
                    self.t_listo_por_proceso[proceso.nombre] += 1

            # Si no hay proceso ejecutandose, selecciona uno
            if self.proceso_actual is None:
                self.seleccionar_siguiente_proceso()

            # Si hay proceso ejecutandose, ejecutarlo
            if self.proceso_actual is not None:
                self.ejecutar_proceso_actual()

            # Procesar procesos bloqueados
            self.procesar_procesos_bloqueados()

            # Calcular CPU_idle: si no hay proceso ejecutándose ni labores del SO
            if (self.proceso_actual is None and 
                self.tiempo_restante_bloqueo == 0 and 
                len(self.cola_listos) == 0):
                self.cpu_idle += 1

            # Avanzar una unidad de tiempo
            self.tiempo_actual += 1
        
        if iteraciones >= tiempo_maximo:
            print(f"⚠️ Advertencia: Simulación terminada por límite de tiempo ({tiempo_maximo} iteraciones)")
            print(f"Estado final - Tiempo: {self.tiempo_actual}, Iteraciones: {iteraciones}")
    
    def obtener_estadisticas_cpu(self):
        """Retorna las estadísticas de CPU calculadas correctamente."""
        # Calcular T_total = t_ultimo_TFP - t_primer_arribo
        if self.t_primer_arribo is not None and self.t_ultimo_tfp is not None:
            # Si hay TFP, usar t_ultimo_tfp directamente
            t_total = self.t_ultimo_tfp - self.t_primer_arribo
        elif self.t_primer_arribo is not None:
            # Si no hay TFP pero hay procesos, usar tiempo_actual
            t_total = self.tiempo_actual - self.t_primer_arribo
        else:
            t_total = 0
        
        # Verificar que CPU_idle sea correcto
        cpu_idle_calculado = t_total - (self.cpu_proc + self.cpu_so)
        if cpu_idle_calculado < 0:
            print(f"⚠️ Advertencia: CPU_idle calculado es negativo: {cpu_idle_calculado}")
            print(f"CPU_proc: {self.cpu_proc}, CPU_SO: {self.cpu_so}, T_total: {t_total}")
        
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


    def ejecutar_proceso_actual(self):
        if self.proceso_actual is None:
            return

        # Se consume una unidad de tiempo de CPU ejecutando proceso
        self.proceso_actual.duracion_rafagas_cpu -= 1
        self.cpu_proc += 1  # Acumular tiempo real de CPU ejecutando procesos
        self.cpu_proc_por_proceso[self.proceso_actual.nombre] += 1  # Acumular por proceso

        if self.proceso_actual.duracion_rafagas_cpu == 0:
            self.proceso_actual.cantidad_rafagas_cpu -= 1

            if self.proceso_actual.cantidad_rafagas_cpu == 0:
                self.terminar_proceso()
            else:
                self.bloquear_proceso()

    def seleccionar_siguiente_proceso(self):
        if len(self.cola_listos) > 0:
            # Agarrar el primer proceso de la cola
            self.proceso_actual = self.cola_listos.pop(0)
            # Aplicar TIP o TCP segun corresponda
            if self.proceso_actual.proceso_nuevo:
                self.aplicar_tip()
                self.proceso_actual.proceso_nuevo = False
            else:
                self.aplicar_tcp()
            
            # NO cambiar estado a "ejecutando" ni registrar evento aquí
            # El proceso solo empezará a ejecutarse después de que termine TIP/TCP

    
    def hay_procesos_pendientes(self):
        """
        Verifica si quedan trabajos por hacer:
            - hay procesos en cola de listos
            - hay procesos bloqueados
            - hay procesos ejecutandose
            - hay procesos que aun no llegaron a su tiempo total
            de ejecucion
        """
        resultado = (len(self.cola_listos) > 0 or 
        len(self.procesos_bloqueados) > 0 or (self.proceso_actual is not None) or
        (any(p.tiempo_arrivo > self.tiempo_actual for p in self.procesos)) or
        (any(p.estado == "terminando" for p in self.procesos)))
        
        
        return resultado


    def bloquear_proceso(self):
        # Guardar tiempo de bloqueo y duración original de I/O
        self.proceso_actual.tiempo_bloqueo = self.tiempo_actual
        self.proceso_actual.duracion_rafagas_io_original = self.proceso_actual.get_duracion_rafagas_io()
        
        # Reiniciar duracion rafaga de I/O para la siguiente vez
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

    def terminar_proceso(self):
        # Registrar evento de fin de ejecución
        self.resultados.append({
            'tiempo': self.tiempo_actual,
            'proceso': self.proceso_actual.nombre,
            'evento': 'fin_ejecucion',
            'estado': 'ejecutando'
        })

        if self.tiempo_tfp > 0:
            self.aplicar_tfp()
            self.proceso_actual.estado = "terminando"
            self.procesos_terminados.append(self.proceso_actual)
        else: 
            # Registrar tiempo de finalización (sin TFP)
            self.t_fin_por_proceso[self.proceso_actual.nombre] = self.tiempo_actual
            # Para TFP = 0, no hay TFP real, por lo que no registramos t_ultimo_tfp
            # El T_total se calculará usando tiempo_actual - 1
            
            self.proceso_actual.calcular_tiempo_retorno(self.tiempo_actual)
            self.proceso_actual.estado = "terminado"
            self.procesos_terminados.append(self.proceso_actual)
            self.resultados.append({
                'tiempo': self.tiempo_actual,
                'proceso': self.proceso_actual.nombre,
                'evento': 'terminacion',
                'estado': 'terminado'
            })

        self.proceso_actual = None

    def procesar_procesos_bloqueados(self):
        """
        Procesa todos los procesos que estan haciendo I/O
        cuando terminan de ejecutar entrada salida los mueve otra vez
        a la cola de listos
        """
        
        procesos_que_terminaron_io = []

        for proceso in self.procesos_bloqueados:
            # Solo procesar procesos que no se bloquearon en este tiempo
            if proceso.tiempo_bloqueo < self.tiempo_actual:
                # Decrementar la duración de I/O
                proceso.duracion_rafagas_io -= 1
                
                if proceso.duracion_rafagas_io == 0:
                    procesos_que_terminaron_io.append(proceso)
                    proceso.estado = "listo"
                    
                    # Reiniciar duracion de CPU para la siguiente ejecución
                    proceso.duracion_rafagas_cpu = proceso.get_duracion_rafagas_cpu()

                    # IMPORTANTE: Los procesos que vuelven de I/O van al FINAL de la cola
                    self.cola_listos.append(proceso)

                    # Registrar evento de fin de I/O en el tiempo actual del simulador
                    self.resultados.append({
                        'tiempo': self.tiempo_actual,
                        'proceso': proceso.nombre,
                        'evento': 'fin_io',
                        'estado': 'listo'
                    })
        for proceso in procesos_que_terminaron_io:
            self.procesos_bloqueados.remove(proceso)

    def aplicar_tip(self):
        if self.tiempo_tip > 0:
            self.tiempo_restante_bloqueo = self.tiempo_tip
            self.tipo_bloqueo = "tip"
            
            # Registrar evento solo si TIP > 0
            self.resultados.append({
                'tiempo': self.tiempo_actual,
                'proceso': self.proceso_actual.nombre,
                'evento': 'inicio_tip',
                'estado': 'bloqueado_sistema'
            })
        else:
            self.tipo_bloqueo = None
            # Si TIP = 0, el proceso pasa directamente a ejecutándose
            self.proceso_actual.estado = "ejecutando"
            self.resultados.append({
                'tiempo': self.tiempo_actual,
                'proceso': self.proceso_actual.nombre,
                'evento': 'inicio ejecucion',
                'estado': 'ejecutando'
            })

    def aplicar_tcp(self):
        if self.tiempo_tcp > 0:
            self.tiempo_restante_bloqueo = self.tiempo_tcp
            self.tipo_bloqueo = "tcp"
            
            # Registrar evento solo si TCP > 0
            self.resultados.append({
                'tiempo': self.tiempo_actual,
                'proceso': self.proceso_actual.nombre,
                'evento': 'inicio_tcp',
                'estado': 'bloqueado_sistema'
            })
        else:
            self.tipo_bloqueo = None
            # Si TCP = 0, el proceso pasa directamente a ejecutando
            self.proceso_actual.estado = "ejecutando"
            self.resultados.append({
                'tiempo': self.tiempo_actual,
                'proceso': self.proceso_actual.nombre,
                'evento': 'inicio ejecucion',
                'estado': 'ejecutando'
            })

    def aplicar_tfp(self):
        if self.tiempo_tfp > 0:
            self.tiempo_restante_bloqueo = self.tiempo_tfp
            self.tipo_bloqueo = "tfp"
            
            # Registrar evento solo si TFP > 0
            self.resultados.append({
                'tiempo': self.tiempo_actual,
                'proceso': self.proceso_actual.nombre,
                'evento': 'inicio_tfp',
                'estado': 'bloqueado_sistema'
            })
        else:
            self.tipo_bloqueo = None
            # Si TFP = 0, el proceso termina inmediatamente
            self.proceso_actual.calcular_tiempo_retorno(self.tiempo_actual)
            self.proceso_actual.estado = "terminado"
            self.procesos_terminados.append(self.proceso_actual)
            self.t_fin_por_proceso[self.proceso_actual.nombre] = self.tiempo_actual
            self.t_ultimo_tfp = self.tiempo_actual
            
            self.resultados.append({
                'tiempo': self.tiempo_actual,
                'proceso': self.proceso_actual.nombre,
                'evento': 'terminacion',
                'estado': 'terminado'
            })

    
    def procesar_tiempo_bloqueo(self):
        if self.tiempo_restante_bloqueo > 0:
            self.tiempo_restante_bloqueo -= 1
            # Acumular tiempo de CPU en labores del SO
            self.cpu_so += 1

            if self.tiempo_restante_bloqueo == 0:
                # Determinar el nombre del proceso para el evento de fin
                nombre_proceso = None
                if self.tipo_bloqueo == 'tfp':
                    # Para TFP, buscar el proceso que está terminando
                    for proceso in self.procesos_terminados:
                        if proceso.estado == "terminando":
                            nombre_proceso = proceso.nombre
                            break
                    self.finalizar_proceso_completamente()
                elif self.tipo_bloqueo in ['tip', 'tcp'] and self.proceso_actual is not None:
                    # Para TIP y TCP, usar el proceso actual
                    nombre_proceso = self.proceso_actual.nombre
                    
                    # Si es TIP, el proceso pasa a estado listo
                    if self.tipo_bloqueo == 'tip':
                        # Después del TIP, el proceso pasa directamente a ejecutarse
                        self.proceso_actual.estado = "ejecutando"
                        self.resultados.append({
                            'tiempo': self.tiempo_actual,
                            'proceso': self.proceso_actual.nombre,
                            'evento': 'inicio ejecucion',
                            'estado': 'ejecutando'
                        })
                    else:
                        # Si es TCP, el proceso puede empezar a ejecutarse
                        self.proceso_actual.estado = "ejecutando"
                        self.resultados.append({
                            'tiempo': self.tiempo_actual,
                            'proceso': self.proceso_actual.nombre,
                            'evento': 'inicio ejecucion',
                            'estado': 'ejecutando'
                        })

                # Registrar evento de fin con el nombre del proceso correcto
                if nombre_proceso:
                    self.resultados.append({
                        'tiempo': self.tiempo_actual,
                        'proceso': nombre_proceso,
                        'evento': f'fin_{self.tipo_bloqueo}',
                        'estado': 'sistema_libre'
                    })
                self.tipo_bloqueo = None
            
            return True # Aun esta bloqueado
        return False # Ya termin0 el bloqueo
    
    def finalizar_proceso_completamente(self):
        """Finaliza completamente un proceso después del TFP."""
        # Buscar el proceso que estaba terminando
        for proceso in self.procesos_terminados:
            if proceso.estado == "terminando":
                # Registrar tiempo de finalización (con TFP)
                self.t_fin_por_proceso[proceso.nombre] = self.tiempo_actual
                self.t_ultimo_tfp = self.tiempo_actual
                
                proceso.calcular_tiempo_retorno(self.tiempo_actual)
                proceso.estado = "terminado"
                
                self.resultados.append({
                    'tiempo': self.tiempo_actual,
                    'proceso': proceso.nombre,
                    'evento': 'terminacion',
                    'estado': 'terminado'
                })
                break