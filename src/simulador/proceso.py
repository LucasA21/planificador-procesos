class Proceso:

    def __init__(self, nombre, tiempo_arrivo, cantidad_rafagas_cpu, duracion_rafagas_cpu, duracion_rafagas_io, prioridad):
        self.nombre = nombre
        self.tiempo_arrivo = int(tiempo_arrivo)
        self.cantidad_rafagas_cpu = int(cantidad_rafagas_cpu)
        self.duracion_rafagas_cpu = int(duracion_rafagas_cpu)
        self.duracion_rafagas_io = int(duracion_rafagas_io)
        self.prioridad = prioridad
        self.estado = "nuevo"
        
        # Guardar valores originales para cálculos
        self.duracion_rafagas_cpu_original = int(duracion_rafagas_cpu)
        self.duracion_rafagas_io_original = int(duracion_rafagas_io)
        self.cantidad_rafagas_cpu_original = int(cantidad_rafagas_cpu)
        
        # Atributos de control
        self.tiempo_retorno = 0
        self.tiempo_retorno_normalizado = 0
        self.tiempo_en_listo = 0
        self.tiempo_bloqueado = 0
        self.tiempo_espera = 0
        self.tiempo_rafaga_cpu = 0
        self.proceso_nuevo = True




    def get_tiempo_arribo(self):
        return self.tiempo_arrivo
    
    def get_cantidad_rafagas_cpu(self):
        return self.cantidad_rafagas_cpu
    
    def get_duracion_rafagas_cpu(self):
        return self.duracion_rafagas_cpu_original
    
    def get_duracion_rafagas_io(self):
        return self.duracion_rafagas_io_original
    
    def get_prioridad(self):
        return self.prioridad
    
    def get_tiempo_en_listo(self):
        return self.tiempo_en_listo
    
    def get_tiempo_bloqueado(self):
        return self.tiempo_bloqueado
    
    def get_tiempo_espera(self):
        return self.tiempo_espera
    
    def get_tiempo_rafaga_cpu(self):
        return self.tiempo_rafaga_cpu
    
    def get_estado(self):
        return self.estado
    
    def set_estado(self, estado):
        self.estado = estado

    def calcular_tiempo_retorno(self, tiempo_finalizacion):
        self.tiempo_retorno = tiempo_finalizacion - self.tiempo_arrivo
        # Usar los valores originales para el cálculo
        if self.duracion_rafagas_cpu_original > 0 and self.cantidad_rafagas_cpu_original > 0:
            self.tiempo_retorno_normalizado = self.tiempo_retorno / (self.cantidad_rafagas_cpu_original * self.duracion_rafagas_cpu_original)
        else:
            self.tiempo_retorno_normalizado = 0

    def __str__(self):
        return f"Proceso {self.nombre}" 

    def __repr__(self):
        return f"Proceso '{self.nombre}', arribo: {self.tiempo_arrivo}"