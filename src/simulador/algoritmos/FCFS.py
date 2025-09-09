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

    def procesar_llegadas(self):
        for proceso in self.procesos:
            if proceso.tiempo_arrivo == self.tiempo_actual:
                self.insertar_ordenado(proceso)
                proceso.estado = "listo"

                # Registrar eventos
                self.resultados.append({
                    'tiempo': self.tiempo_actual,
                    'proceso': proceso.nombre,
                    'evento': 'llegada',
                    'estado': 'listo'
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
                self.tiempo_actual += 1
                continue

            # Incrementar tiempo de espera para procesos en cola de listos
            for proceso in self.cola_listos:
                proceso.tiempo_en_listo += 1

            # Si no hay proceso ejecutandose, selecciona uno
            if self.proceso_actual is None:
                self.seleccionar_siguiente_proceso()

            # Si hay proceso ejecutandose, ejecutarlo
            if self.proceso_actual is not None:
                self.ejecutar_proceso_actual()

            # Procesar procesos bloqueados
            self.procesar_procesos_bloqueados()

            # Avanzar una unidad de tiempo
            self.tiempo_actual += 1
        
        if iteraciones >= tiempo_maximo:
            print(f"⚠️ Advertencia: Simulación terminada por límite de tiempo ({tiempo_maximo} iteraciones)")
            print(f"Estado final - Tiempo: {self.tiempo_actual}, Iteraciones: {iteraciones}")


    def ejecutar_proceso_actual(self):
        if self.proceso_actual is None:
            return

        # Se consume una unidad de tiempo
        self.proceso_actual.duracion_rafagas_cpu -= 1

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
        # Reiniciar duracion rafaga de I/O para la siguiente vez
        self.proceso_actual.duracion_rafagas_io = self.proceso_actual.get_duracion_rafagas_io()
        
        self.proceso_actual.estado = "bloqueado"

        self.procesos_bloqueados.append(self.proceso_actual)

        # Registrar evento
        self.resultados.append({
            'tiempo': self.tiempo_actual,
            'proceso': self.proceso_actual.nombre,
            'evento': 'bloqueo',
            'estado': 'bloqueado'
        })

        self.proceso_actual = None

    def terminar_proceso(self):
        if self.tiempo_tfp > 0:
            self.aplicar_tfp()
            self.proceso_actual.estado = "terminando"
            self.procesos_terminados.append(self.proceso_actual)
        else: 
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
            proceso.duracion_rafagas_io -= 1

            if proceso.duracion_rafagas_io == 0:
                procesos_que_terminaron_io.append(proceso)
                proceso.estado = "listo"
                
                # Reiniciar duracion de CPU para la siguiente ejecución
                proceso.duracion_rafagas_cpu = proceso.get_duracion_rafagas_cpu()

                # IMPORTANTE: Los procesos que vuelven de I/O van al FINAL de la cola
                self.cola_listos.append(proceso)

                # Registrar evento
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
        else:
            self.tipo_bloqueo = None

        # Registrar evento
        self.resultados.append({
            'tiempo': self.tiempo_actual,
            'proceso': 'SISTEMA',
            'evento': 'inicio_tip',
            'estado': 'bloqueado_sistema'
            
        })

    def aplicar_tcp(self):
        if self.tiempo_tcp > 0:
            self.tiempo_restante_bloqueo = self.tiempo_tcp
            self.tipo_bloqueo = "tcp"
        else:
            self.tipo_bloqueo = None

        # Registrar evento
        self.resultados.append({
            'tiempo': self.tiempo_actual,
            'proceso': 'SISTEMA',
            'evento': 'inicio_tcp',
            'estado': 'bloqueado_sistema'
        })

    def aplicar_tfp(self):
        if self.tiempo_tfp > 0:
            self.tiempo_restante_bloqueo = self.tiempo_tfp
            self.tipo_bloqueo = "tfp"
        else:
            self.tipo_bloqueo = None

        # Registrar evento
        self.resultados.append({
            'tiempo': self.tiempo_actual,
            'proceso': 'SISTEMA',
            'evento': 'inicio_tfp',
            'estado': 'bloqueado_sistema'
        })

    
    def procesar_tiempo_bloqueo(self):
        if self.tiempo_restante_bloqueo > 0:
            self.tiempo_restante_bloqueo -= 1

            if self.tiempo_restante_bloqueo == 0:
                if self.tipo_bloqueo == 'tfp':
                    self.finalizar_proceso_completamente()
                elif self.tipo_bloqueo in ['tip', 'tcp'] and self.proceso_actual is not None:
                    # Cuando termina TIP o TCP, el proceso puede empezar a ejecutarse
                    self.proceso_actual.estado = "ejecutando"
                    self.resultados.append({
                        'tiempo': self.tiempo_actual,
                        'proceso': self.proceso_actual.nombre,
                        'evento': 'inicio ejecucion',
                        'estado': 'ejecutando'
                    })

                self.resultados.append({
                    'tiempo': self.tiempo_actual,
                    'proceso': 'SISTEMA',
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
                proceso.calcular_tiempo_retorno(self.tiempo_actual)
                proceso.estado = "terminado"
                
                self.resultados.append({
                    'tiempo': self.tiempo_actual,
                    'proceso': proceso.nombre,
                    'evento': 'terminacion',
                    'estado': 'terminado'
                })
                break