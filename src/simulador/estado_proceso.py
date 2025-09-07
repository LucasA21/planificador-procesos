'''
Esta clase representa el estado de un proceso en el simulador.
'''

from enum import Enum

class EstadoProceso(Enum):
    NUEVO = "NUEVO"
    LISTO = "LISTO"
    CORRIENDO = "CORRIENDO"
    BLOQUEADO = "BLOQUEADO"
    TERMINADO = "TERMINADO"


    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
        
        