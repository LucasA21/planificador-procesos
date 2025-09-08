'''
Esta clase representa un proceso en el simulador. Almacena informacion estatica del proceso (No se modifica durante la simulacion).
'''

class Proceso:

    def __init__(self, nombre, tiempo_arribo, rafagas_cpu, duracion_rafagas_cpu, duracion_rafagas_io, prioridad):
        self.nombre = nombre
        self.tiempo_arribo = tiempo_arribo
        self.rafagas_cpu = rafagas_cpu
        self.duracion_rafagas_cpu = duracion_rafagas_cpu
        self.duracion_rafagas_io = duracion_rafagas_io
        self.prioridad = prioridad

        self.tiempo_cpu_total = rafagas_cpu * duracion_rafagas_cpu
        self.rafagas_io = rafagas_cpu - 1

    def __str__(self):
        return f"Proceso {self.nombre}"

    def __repr__(self):
        return f"Proceso '{self.nombre}', arribo: {self.tiempo_arribo}"