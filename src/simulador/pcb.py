'''
Esta clase representa el PCB (Process Control Block) de un proceso en el simulador. 
Registra informacion dinamica del proceso durante la simulacion.
'''

from proceso import Proceso
from estado_proceso import EstadoProceso

class PCB:

    def __init__(self, proceso: Proceso):
        self.proceso = proceso
        self.estado = EstadoProceso.NUEVO

        # Control de ejecucion
        self.rafaga_actual = 0
        self.rafaga_cpu_restante = proceso.tiempo_cpu_total
        self.rafaga_actual_duracion = 0
        self.quantum_restante = 0
        
        # Control de E/S
        self.tiempo_io_restante = 0
        self.rafaga_io_restantes = proceso.rafagas_io

        # Metricas

        self.tiempo_retorno = 0
        self.tiempo_en_listo = 0
        self.tiempo_en_corriendo = 0
        self.tiempo_en_bloqueado = 0

        def iniciar_rafaga(self):
            # Inicia una nueva rafaga de CPU
            self.rafaga_actual += 1
            self.rafaga_actual_duracion = self.proceso.duracion_rafagas_cpu

        def terminar_rafaga(self):
            # Termina la rafaga actual de CPU y prepara la E/S si es necesario
            if self.rafagas_io > 0:
                self.tiempo_io_restante = self.proceso.duracion_rafagas_io
                self.rafaga_io_restantes -= 1

        def actualizar_metricas(self, tiempo_transcurrido):
            # Actualiza las metricas segun el estado actual
            if self.estado == EstadoProceso.LISTO:
                self.tiempo_en_listo += tiempo_transcurrido
            elif self.estado == EstadoProceso.CORRIENDO:
                self.tiempo_en_corriendo += tiempo_transcurrido
            elif self.estado == EstadoProceso.BLOQUEADO:
                self.tiempo_en_bloqueado += tiempo_transcurrido

        def __str__(self):
            return f"PCB del proceso {self.proceso.nombre}"

        def __repr__(self):
            return f"PCB del proceso {self.proceso.nombre}"