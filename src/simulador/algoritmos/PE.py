class PE:
    def __init__(self, procesos, tiempo_tip, tiempo_tcp, tiempo_tfp):
        self.procesos = procesos
        
        # Instante del tiempo actual
        self.tiempo_actual = 0
        
        # No hay procesos ejecutandose en la primera instancia de tiempo
        self.proceso_actual = None
        
        # Colas vacias
        self.cola_listos = []
        self.procesos_bloqueados = []
        self.procesos_terminados = []
        
        # Lista para guardar los eventos que fueron sucediendo
        self.resultados = []

        # Tiempos del SO
        self.tiempo_tip = tiempo_tip
        self.tiempo_tcp = tiempo_tcp
        self.tiempo_tfp = tiempo_tfp

        self.tiempo_restante_bloqueo = 0
        
        # TIP, TCP O TFP
        self.tipo_bloqueo = None
        
        # Flag para indicar si se debe aplicar TCP después del TIP actual
        self.aplicar_tcp_despues_tip = False
        
        # Flag para indicar si el TCP actual es después de un TIP
        self.tcp_despues_tip_activo = False
        
        # Flag para indicar si se debe registrar fin_tcp después de TIP
        self.registrar_fin_tcp_despues_tip = False
        
        
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
        
        # Lista de procesos que terminaron I/O en el tiempo actual
        # No pueden ser seleccionados hasta el siguiente tiempo
        self.procesos_recien_terminaron_io = []

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
        Inserta el proceso en la cola de listos manteniendo el orden de prioridad externa.
        Para PE, el orden se basa en la prioridad externa (mayor prioridad primero).
        """
        if len(self.cola_listos) == 0:
            self.cola_listos.append(proceso)
            return

        # Ordenar por prioridad externa (mayor prioridad primero)
        prioridad_proceso = proceso.get_prioridad()
        
        for i, proceso_en_cola in enumerate(self.cola_listos):
            prioridad_en_cola = proceso_en_cola.get_prioridad()
            
            if prioridad_proceso > prioridad_en_cola:
                # Insertar antes del proceso actual (mayor prioridad)
                self.cola_listos.insert(i, proceso)
                return

        self.cola_listos.append(proceso)

    def verificar_preemption(self):
        """
        Verifica si el proceso actual debe ser preemptado por un proceso
        con mayor prioridad externa.
        En PE, los procesos que terminan I/O SÍ pueden preemptar inmediatamente.
        """
        if self.proceso_actual is None or len(self.cola_listos) == 0:
            return False
            
        # Ordenar la cola por prioridad externa (mayor primero)
        self.cola_listos.sort(key=lambda p: p.get_prioridad(), reverse=True)
        
        # Para preemption, SÍ considerar procesos que acaban de terminar I/O
        # porque deben poder preemptar inmediatamente si tienen mayor prioridad
        proceso_mas_prioritario = self.cola_listos[0]
        
        # Si hay un proceso con mayor prioridad que el actual
        if proceso_mas_prioritario.get_prioridad() > self.proceso_actual.get_prioridad():
            return True
            
        return False

    def preemptar_proceso_actual(self):
        """
        Preempta el proceso actual y lo devuelve a la cola de listos
        con su duración restante de ráfaga.
        """
        if self.proceso_actual is None or len(self.cola_listos) == 0:
            return
            
        # Ordenar la cola para obtener el proceso de mayor prioridad
        self.cola_listos.sort(key=lambda p: p.get_prioridad(), reverse=True)
        
        # Para preemption, tomar el proceso más prioritario directamente
        # (incluso si acaba de terminar I/O, porque debe poder preemptar)
        proceso_mayor_prioridad = self.cola_listos[0]
        indice_mayor_prioridad = 0
        
        # Registrar evento de fin de ejecución
        self.resultados.append({
            'tiempo': self.tiempo_actual - 1,
            'proceso': self.proceso_actual.nombre,
            'evento': 'fin_ejecucion',
            'estado': 'ejecutando'
        })
        
        # El proceso actual vuelve a la cola de listos con su duración restante
        self.proceso_actual.estado = "listo"
        self.insertar_ordenado(self.proceso_actual)
        
        # Registrar evento de preemption
        self.resultados.append({
            'tiempo': self.tiempo_actual,
            'proceso': self.proceso_actual.nombre,
            'evento': 'preemption',
            'estado': 'listo'
        })
        
        # El proceso de mayor prioridad toma la CPU
        self.proceso_actual = self.cola_listos.pop(indice_mayor_prioridad)
        
        # Determinar qué tiempos del sistema aplicar para el proceso que preempta
        if self.proceso_actual.proceso_nuevo:
            # Proceso nuevo: aplicar TIP + TCP
            self.aplicar_tip()
            self.proceso_actual.proceso_nuevo = False
            # Marcar que después del TIP se debe aplicar TCP
            self.aplicar_tcp_despues_tip = True
        else:
            # Proceso que vuelve: solo TCP
            self.aplicar_tcp()
        
        # Si este proceso acaba de terminar I/O, removerlo de la lista de recién terminados
        # porque ya está siendo usado para preemptar
        if self.proceso_actual.nombre in self.procesos_recien_terminaron_io:
            self.procesos_recien_terminaron_io.remove(self.proceso_actual.nombre)

    def ejecutar(self):
        # Límite de seguridad para evitar bucles infinitos
        tiempo_maximo = 1000
        iteraciones = 0

        while self.hay_procesos_pendientes() and iteraciones < tiempo_maximo:
            iteraciones += 1

            # Verificar si se debe registrar fin_tcp después de TIP
            if self.registrar_fin_tcp_despues_tip and self.proceso_actual is not None:
                self.resultados.append({
                    'tiempo': self.tiempo_actual,
                    'proceso': self.proceso_actual.nombre,
                    'evento': 'fin_tcp',
                    'estado': 'sistema_libre'
                })
                # Iniciar ejecución inmediatamente después del fin_tcp
                self.proceso_actual.estado = "ejecutando"
                self.resultados.append({
                    'tiempo': self.tiempo_actual,
                    'proceso': self.proceso_actual.nombre,
                    'evento': 'inicio ejecucion',
                    'estado': 'ejecutando'
                })
                self.registrar_fin_tcp_despues_tip = False

            self.procesar_llegadas()

            # Procesar tiempo de TIP/TCP/TFP
            if self.procesar_tiempo_bloqueo():
                # Procesar procesos bloqueados incluso si hay TIP/TCP/TFP activo
                self.procesar_procesos_bloqueados()
                self.tiempo_actual += 1
                continue

            # PRIMERO: Procesar procesos bloqueados para que puedan preemptar inmediatamente
            self.procesar_procesos_bloqueados()

            # SEGUNDO: Verificar preemption DESPUÉS de procesar procesos bloqueados
            if self.proceso_actual is not None and self.tiempo_restante_bloqueo == 0:
                # ¿Hay alguien más prioritario en cola_listos?
                if self.verificar_preemption():
                    # tie-break: si el proceso actual va a TERMINAR su ráfaga en ESTE tick,
                    # permitile ejecutar (porque debe poder iniciar su I/O inmediatamente).
                    # Observá que miramos la duracion _antes_ de ejecutar.
                    if getattr(self.proceso_actual, 'duracion_rafagas_cpu', None) == 1:
                        # dejar que ejecute su último unit, no preempuar
                        pass
                    else:
                        # preemptar ahora, no ejecuta este tick
                        self.preemptar_proceso_actual()

            # Incrementar tiempo de espera para procesos en cola de listos
            for proceso in self.cola_listos:
                proceso.tiempo_en_listo += 1
                # Acumular tiempo en estado listo (solo después de pagar TIP)
                if proceso.nombre in self.t_listo_por_proceso:
                    self.t_listo_por_proceso[proceso.nombre] += 1

            # Si no hay proceso ejecutandose, selecciona uno
            if self.proceso_actual is None:
                self.seleccionar_siguiente_proceso()

            # Ahora, si aún hay proceso en CPU y no hay bloqueo, ejecuta UNA sola unidad
            if self.proceso_actual is not None and self.tiempo_restante_bloqueo == 0:
                self.ejecutar_proceso_actual()





            # Calcular CPU_idle: si no hay proceso ejecutándose ni labores del SO
            if (self.proceso_actual is None and 
                self.tiempo_restante_bloqueo == 0 and 
                len(self.cola_listos) == 0):
                self.cpu_idle += 1

            # Limpiar la lista de procesos que terminaron I/O en este tiempo
            # Ahora pueden ser seleccionados en el siguiente tiempo
            self.procesos_recien_terminaron_io.clear()
            
            # Avanzar una unidad de tiempo
            self.tiempo_actual += 1
        
        if iteraciones >= tiempo_maximo:
            print(f"Advertencia: Simulación terminada por límite de tiempo ({tiempo_maximo} iteraciones)")
            print(f"Estado final - Tiempo: {self.tiempo_actual}, Iteraciones: {iteraciones}")
    
    def obtener_estadisticas_cpu(self):
        """Retorna las estadísticas de CPU."""
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
            print(f"Advertencia: CPU_idle calculado es negativo: {cpu_idle_calculado}")
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
        """
        Selecciona el proceso con mayor prioridad externa.
        La cola ya está ordenada por PE, por lo que solo se toma el primero.
        """
        if len(self.cola_listos) > 0:
            # Buscar el primer proceso que no haya terminado I/O en este tiempo
            proceso_seleccionado = None
            indice_seleccionado = -1
            
            for i, proceso in enumerate(self.cola_listos):
                if proceso.nombre not in self.procesos_recien_terminaron_io:
                    proceso_seleccionado = proceso
                    indice_seleccionado = i
                    break
            
            # Si no hay procesos disponibles (todos terminaron I/O en este tiempo), no seleccionar ninguno
            if proceso_seleccionado is None:
                return
                
            # Seleccionar el proceso encontrado
            self.proceso_actual = self.cola_listos.pop(indice_seleccionado)
            
            # Determinar qué tiempos del sistema aplicar
            if self.proceso_actual.proceso_nuevo:
                # Proceso nuevo: siempre aplicar TIP
                self.aplicar_tip()
                self.proceso_actual.proceso_nuevo = False
            else:
                # Proceso que vuelve de I/O: aplicar TCP
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

                    # Insertar el proceso en la cola de listos manteniendo el orden PE
                    self.insertar_ordenado(proceso)
                    
                    # Marcar que este proceso acaba de terminar I/O en este tiempo
                    # No puede ser seleccionado hasta el siguiente tiempo
                    self.procesos_recien_terminaron_io.append(proceso.nombre)

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
            # Si TIP = 0, verificar si se necesita TCP después
            if self.aplicar_tcp_despues_tip:
                # Aplicar TCP directamente
                self.aplicar_tcp_despues_tip = False
                self.aplicar_tcp()
            else:
                # Si no se necesita TCP, pasar directamente a ejecutándose
                self.tipo_bloqueo = None
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
                # GUARDAR el tipo de bloqueo original: importantísimo
                tipo_original = self.tipo_bloqueo

                # Determinar el nombre del proceso para el evento de fin
                nombre_proceso = None

                if tipo_original == 'tfp':
                    # Para TFP, buscar el proceso que está terminando
                    for proceso in self.procesos_terminados:
                        if proceso.estado == "terminando":
                            nombre_proceso = proceso.nombre
                            break
                    # Finaliza el proceso completamente (esto puede sobrescribir self.tipo_bloqueo)
                    self.finalizar_proceso_completamente()

                elif tipo_original in ['tip', 'tcp'] and self.proceso_actual is not None:
                    # Para TIP y TCP, usar el proceso actual
                    nombre_proceso = self.proceso_actual.nombre

                    # Verificar si después del TIP se debe aplicar TCP
                    if tipo_original == 'tip' and self.aplicar_tcp_despues_tip:
                        # Registrar fin del TIP primero (usa tipo_original seguro)
                        self.resultados.append({
                            'tiempo': self.tiempo_actual,
                            'proceso': self.proceso_actual.nombre,
                            'evento': 'fin_tip',
                            'estado': 'sistema_libre'
                        })
                        # Aplicar TCP después del TIP
                        self.aplicar_tcp_despues_tip = False
                        self.tcp_despues_tip_activo = True
                        self.aplicar_tcp()
                        # No cambiar estado a ejecutando aún, esperar a que termine el TCP
                        nombre_proceso = None
                    else:
                        # Verificar si hay un proceso más prioritario en la cola de listos
                        # (Lógica para evitar TCP duplicado, similar a SRTN)
                        if len(self.cola_listos) > 0:
                            # Ordenar la cola por prioridad externa (mayor primero)
                            self.cola_listos.sort(key=lambda p: p.get_prioridad(), reverse=True)
                            
                            # Verificar si el primer proceso en la cola es más prioritario
                            proceso_mas_prioritario = self.cola_listos[0]
                            if (proceso_mas_prioritario.get_prioridad() > 
                                self.proceso_actual.get_prioridad()):
                                
                                # El proceso actual debe volver a la cola de listos
                                # Mantener la duración restante de la ráfaga de CPU
                                self.proceso_actual.estado = "listo"
                                # Restar 1 al contador de CPU del proceso que cede la CPU
                                self.cpu_proc -= 1
                                self.cpu_proc_por_proceso[self.proceso_actual.nombre] -= 1
                                self.insertar_ordenado(self.proceso_actual)
                                self.proceso_actual = None
                                
                                # El proceso más prioritario debe ejecutarse directamente
                                # (sin ejecutar TCP ya que el TCP ya fue consumido)
                                self.proceso_actual = self.cola_listos.pop(0)
                                self.proceso_actual.estado = "ejecutando"
                                
                                # Registrar evento de cambio de proceso
                                self.resultados.append({
                                    'tiempo': self.tiempo_actual,
                                    'proceso': self.proceso_actual.nombre,
                                    'evento': 'cambio_proceso_pe',
                                    'estado': 'ejecutando'
                                })
                                
                                # Registrar evento de inicio de ejecución
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
                                        'evento': f'fin_{tipo_original}',
                                        'estado': 'sistema_libre'
                                    })
                                self.tipo_bloqueo = None
                                return False  # No está bloqueado, el proceso puede ejecutarse
                        
                        # Si no hay proceso más prioritario, continuar con el proceso actual
                        self.proceso_actual.estado = "ejecutando"
                        self.resultados.append({
                            'tiempo': self.tiempo_actual,
                            'proceso': self.proceso_actual.nombre,
                            'evento': 'inicio ejecucion',
                            'estado': 'ejecutando'
                        })
                        # Ejecutar inmediatamente después de que termine el TIP/TCP
                        # NOTA: ejecutar_proceso_actual() puede terminar el proceso e invocar aplicar_tfp(),
                        # lo cual puede cambiar self.tipo_bloqueo. Por eso usamos tipo_original para registrar el fin.
                        self.ejecutar_proceso_actual()

                # Registrar evento de fin con el tipo ORIGINAL del bloqueo
                if nombre_proceso:
                    self.resultados.append({
                        'tiempo': self.tiempo_actual,
                        'proceso': nombre_proceso,
                        'evento': f'fin_{tipo_original}',
                        'estado': 'sistema_libre'
                    })
                elif self.tcp_despues_tip_activo and tipo_original == 'tcp':
                    # Si es TCP después de TIP, marcar que se debe registrar fin_tcp en el siguiente ciclo
                    self.tcp_despues_tip_activo = False
                    self.registrar_fin_tcp_despues_tip = True

                # IMPORTANTE: Solo limpiar el tipo de bloqueo si NO fue cambiado por una nueva operación.
                # Si durante la ejecución se aplicó un nuevo bloqueo (p.ej. aplicar_tfp()) entonces
                # self.tipo_bloqueo ya apunta al nuevo bloqueo y self.tiempo_restante_bloqueo fue inicializado.
                # Aquí simplemente ponemos None **solo** si el tipo era el que acabamos de terminar y
                # no se reaplicó otro inmediatamente.
                # Para simplificar y evitar perder el nuevo bloqueo, hacemos:
                if self.tipo_bloqueo == tipo_original:
                    self.tipo_bloqueo = None

            return True  # Aun esta bloqueado
        return False  # Ya terminó el bloqueo
    
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
