"""
Implementacion del algoritmo de Prioridad Externa.

Este algoritmo debe hacer lo siguiente:
- Primero debe mirar los arribos de los procesos nuevos
- Si un proceso arribo y no hay ningun proceso para hacer una comparacion de prioridades entre procesos, y la cpu esta libre, ese proceso
arranca a ejecutar.
- Si hay mas de un proceso al mismo tiempo listo para ejecutar (es decir no esta bloqueado y ya arribo), se debe fijar la prioridad del procesos
y elegir el proceso con mayor prioridad (la prioridad va del 1 al 100, siendo 100 la prioridad mas alta).
- Al igual que todos los algoritmos no apropiativos: Para ejecutarlo primero debe consumir el TIP (este atributo va a ser puesto por el usuario), el TIP es el tiempo de ingreso del proceso,
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

from planificador import Planificador
from cola import Cola
from pcb import PCB
from estado_proceso import EstadoProceso
from evento import Evento, TipoEvento

class PrioridadExterna(Planificador):
    """
    Implementacion del algoritmo de Prioridad Externa.
    
    Este algoritmo selecciona procesos basandose en su prioridad externa.
    Es un algoritmo no apropiativo, por lo que no interrumpe procesos
    en ejecucion.
    """
    
    def __init__(self, procesos, tip, tcp, tfp):
        """
        Inicializa el planificador de Prioridad Externa.
        
        Args:
            procesos: Lista de procesos a planificar
            tip: Tiempo de ingreso del proceso
            tcp: Tiempo de conmutacion entre procesos
            tfp: Tiempo de finalizacion del proceso
        """
        super().__init__(procesos, tip, tcp, tfp, 0)
    
    def _seleccionar_siguiente_proceso(self):
        """
        Selecciona el siguiente proceso segun Prioridad Externa.
        
        Selecciona el proceso con mayor prioridad de los que estan listos
        para ejecutar. Es un algoritmo no apropiativo, por lo que no
        interrumpe procesos en ejecucion.
        """
        # Verificar si hay procesos en la cola de listos
        if self.cola_listos.esta_vacia():
            self.proceso_actual = None
            return
        
        # Obtener el proceso con mayor prioridad
        proceso_seleccionado = self.cola_listos.obtener_siguiente_prioridad()
        
        if proceso_seleccionado is not None:
            # Asignar el proceso seleccionado
            self.proceso_actual = proceso_seleccionado
            
            # Registrar evento de despacho
            evento_despacho = Evento(
                TipoEvento.DESPACHO,
                self.tiempo_actual,
                proceso_seleccionado,
                f"Despacho del proceso {proceso_seleccionado.proceso.nombre} por prioridad {proceso_seleccionado.proceso.prioridad}"
            )
            self.eventos.append(evento_despacho)
            
            # Consumir TCP si no es el primer proceso
            if len(self.procesos_terminados) > 0 or self.tiempo_actual > 0:
                self.tiempo_actual += self.tcp
                self.tiempo_so += self.tcp
        else:
            self.proceso_actual = None