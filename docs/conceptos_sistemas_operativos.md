# Conceptos de Sistemas Operativos para el Simulador de Planificación

## 1. Procesos y Hilos

### ¿Qué es un Proceso?
Un **proceso** es un programa en ejecución. Tiene:
- **Código**: Las instrucciones del programa
- **Datos**: Variables y estructuras de datos
- **Estado**: Información sobre su ejecución actual
- **Recursos**: Memoria, archivos abiertos, etc.

### Estados de un Proceso
```
NUEVO → LISTO → CORRIENDO → TERMINADO
         ↑         ↓
         ← BLOQUEADO ←
```

- **NUEVO**: El proceso se está creando
- **LISTO**: El proceso está listo para ejecutarse, esperando la CPU
- **CORRIENDO**: El proceso se está ejecutando en la CPU
- **BLOQUEADO**: El proceso está esperando un evento (I/O, semáforo, etc.)
- **TERMINADO**: El proceso ha terminado su ejecución

### PCB (Process Control Block)
Es la estructura de datos que contiene toda la información del proceso:
- **Identificación**: PID, nombre
- **Estado**: Estado actual del proceso
- **Contadores**: Contador de programa, registros de CPU
- **Información de planificación**: Prioridad, tiempo de CPU usado
- **Información de memoria**: Punteros a tablas de memoria
- **Información de I/O**: Lista de dispositivos asignados

## 2. Planificación de Procesos

### ¿Por qué necesitamos planificación?
En un sistema multiprogramado, varios procesos comparten la CPU. El **planificador** decide:
- **Cuándo** ejecutar cada proceso
- **Por cuánto tiempo** ejecutar cada proceso
- **En qué orden** ejecutar los procesos

### Objetivos de la Planificación
- **Utilización de CPU**: Mantener la CPU ocupada
- **Rendimiento**: Maximizar el throughput (procesos por unidad de tiempo)
- **Tiempo de respuesta**: Minimizar el tiempo de espera
- **Tiempo de retorno**: Minimizar el tiempo total de ejecución
- **Equidad**: Tratar a todos los procesos de manera justa

### Métricas de Rendimiento

#### Tiempo de Retorno (Turnaround Time)
**TR = Tiempo de finalización - Tiempo de llegada**
- Tiempo total que tarda un proceso desde que llega hasta que termina
- Incluye tiempo de espera, tiempo de ejecución y tiempo de I/O

#### Tiempo de Retorno Normalizado
**TRN = Tiempo de Retorno / Tiempo de CPU usado**
- Mide la "eficiencia" del proceso
- Un proceso que usa mucha CPU debería tener un TRN menor

#### Tiempo de Espera (Waiting Time)
**Tiempo que el proceso pasa en estado LISTO**
- No incluye tiempo de ejecución ni tiempo de I/O
- Solo tiempo esperando por la CPU

#### Tiempo de Respuesta (Response Time)
**Tiempo desde que llega hasta que se ejecuta por primera vez**
- Importante para sistemas interactivos

## 3. Algoritmos de Planificación

### FCFS (First Come First Served)
**Características**:
- No expropiativo
- Procesos se ejecutan en orden de llegada
- Simple de implementar

**Ventajas**:
- Simple y justo
- No hay inanición (starvation)

**Desventajas**:
- Puede tener convoy effect (proceso largo bloquea a todos)
- No es óptimo para tiempo de respuesta

### Round Robin
**Características**:
- Expropativo
- Cada proceso tiene un quantum de tiempo
- Si no termina en el quantum, se va a la cola de listos

**Ventajas**:
- Bueno para sistemas interactivos
- Tiempo de respuesta predecible
- No hay inanición

**Desventajas**:
- El quantum debe ser cuidadosamente elegido
- Muchos cambios de contexto si el quantum es muy pequeño

### Prioridad Externa
**Características**:
- Cada proceso tiene una prioridad
- Se ejecuta el de mayor prioridad
- Puede ser expropiativo o no

**Ventajas**:
- Permite dar preferencia a procesos importantes
- Flexible

**Desventajas**:
- Puede causar inanición de procesos de baja prioridad
- Necesita mecanismo de envejecimiento (aging)

### SPN (Shortest Process Next)
**Características**:
- No expropiativo
- Se ejecuta el proceso con menor tiempo de CPU restante
- Requiere conocimiento previo del tiempo de ejecución

**Ventajas**:
- Óptimo para tiempo de retorno promedio
- Minimiza tiempo de espera

**Desventajas**:
- Puede causar inanición de procesos largos
- Requiere estimación del tiempo de ejecución

### SRTN (Shortest Remaining Time Next)
**Características**:
- Expropativo
- Se ejecuta el proceso con menor tiempo restante
- Si llega un proceso con menos tiempo restante, expropia la CPU

**Ventajas**:
- Óptimo para tiempo de retorno promedio
- Mejor que SPN porque es expropiativo

**Desventajas**:
- Puede causar inanición
- Requiere estimación del tiempo de ejecución

## 4. Cambio de Contexto

### ¿Qué es el Cambio de Contexto?
Es el proceso de guardar el estado de un proceso y cargar el estado de otro proceso.

**Pasos**:
1. Guardar estado del proceso actual (registros, contador de programa)
2. Cargar estado del nuevo proceso
3. Cambiar a modo usuario y saltar a la dirección del nuevo proceso

### Overhead del Cambio de Contexto
- **Tiempo de conmutación (TCP)**: Tiempo que toma el cambio de contexto
- **Overhead**: Tiempo "perdido" que no se usa para ejecutar procesos
- **Frecuencia**: Afecta el rendimiento del sistema

## 5. Multiprogramación

### ¿Qué es la Multiprogramación?
Técnica que permite que varios procesos estén en memoria al mismo tiempo y compartan la CPU.

**Ventajas**:
- Mejor utilización de la CPU
- Mejor utilización de recursos
- Mejor rendimiento del sistema

**Desventajas**:
- Mayor complejidad
- Necesidad de sincronización
- Posibles problemas de concurrencia

### Grado de Multiprogramación
- **Alto**: Muchos procesos en memoria
- **Bajo**: Pocos procesos en memoria
- **Óptimo**: Balance entre utilización y overhead

## 6. I/O y Bloqueo

### Operaciones de I/O
- **Síncronas**: El proceso se bloquea hasta que termina la I/O
- **Asíncronas**: El proceso continúa ejecutándose

### Estados de I/O
- **Solicitud**: El proceso pide una operación de I/O
- **Ejecución**: El dispositivo ejecuta la operación
- **Completado**: La operación termina y el proceso se desbloquea

### Tiempo de I/O
- **Tiempo de servicio**: Tiempo que toma la operación de I/O
- **Tiempo de espera**: Tiempo que el proceso pasa bloqueado
- **Tiempo de cola**: Tiempo esperando en la cola del dispositivo

## 7. Simulación de Sistemas

### ¿Por qué simular?
- **Control**: Podemos controlar todos los parámetros
- **Reproducibilidad**: Mismos resultados con mismos datos
- **Análisis**: Podemos medir exactamente qué pasa
- **Comparación**: Podemos comparar diferentes algoritmos

### Componentes de una Simulación
1. **Modelo**: Representación del sistema real
2. **Datos de entrada**: Procesos, parámetros del sistema
3. **Motor de simulación**: Lógica que ejecuta la simulación
4. **Métricas**: Medidas de rendimiento
5. **Salida**: Resultados y reportes

### Tipos de Simulación
- **Discreta**: Eventos ocurren en momentos específicos
- **Continua**: Variables cambian continuamente
- **Estocástica**: Incluye elementos aleatorios
- **Determinística**: Sin elementos aleatorios

## 8. Métricas de Rendimiento del Sistema

### Utilización de CPU
**Porcentaje de tiempo que la CPU está ocupada**
- **CPU utilizada por procesos**: Tiempo ejecutando procesos
- **CPU utilizada por SO**: Tiempo en cambio de contexto, etc.
- **CPU desocupada**: Tiempo sin hacer nada

### Throughput
**Número de procesos completados por unidad de tiempo**
- Medida de productividad del sistema
- Depende del algoritmo de planificación

### Tiempo de Retorno de la Tanda
**Tiempo desde que llega el primer proceso hasta que termina el último**
- Medida del tiempo total de ejecución
- Incluye todos los overheads del sistema

## 9. Consideraciones de Implementación

### Cola de Eventos
- **Estructura**: Lista ordenada por tiempo
- **Operaciones**: Insertar, extraer mínimo
- **Eficiencia**: Usar heap o lista ordenada

### Manejo de Estados
- **Transiciones**: Seguir el orden especificado
- **Validación**: Verificar que las transiciones sean válidas
- **Consistencia**: Mantener consistencia entre PCB y colas

### Cálculo de Métricas
- **Tiempo real**: Durante la simulación
- **Tiempo final**: Al terminar la simulación
- **Precisión**: Usar números de punto flotante

### Archivos de Salida
- **Eventos**: Registrar cada cambio de estado
- **Métricas**: Calcular y guardar estadísticas
- **Formato**: JSON para facilitar el análisis

## 10. Errores Comunes y Cómo Evitarlos

### Errores de Implementación
- **Orden de eventos**: Procesar en el orden correcto
- **Cálculo de tiempo**: Sumar correctamente los tiempos
- **Transiciones de estado**: Seguir las reglas especificadas
- **Métricas**: Calcular en el momento correcto

### Errores de Lógica
- **Quantum**: Manejar correctamente el agotamiento de quantum
- **Expropiación**: Implementar correctamente la expropiación
- **I/O**: Manejar correctamente las operaciones de I/O
- **Prioridades**: Implementar correctamente el ordenamiento

### Errores de Medición
- **Tiempo de retorno**: Incluir todos los tiempos necesarios
- **Tiempo de espera**: Solo tiempo en estado LISTO
- **Utilización**: Calcular correctamente los porcentajes
- **Normalización**: Dividir por el tiempo correcto

## 11. Consejos para el Desarrollo

### Fase de Diseño
1. **Entender los requisitos**: Leer cuidadosamente la consigna
2. **Diseñar la estructura**: Planificar las clases y relaciones
3. **Definir interfaces**: Especificar cómo se comunican las clases
4. **Planificar las pruebas**: Preparar casos de prueba

### Fase de Implementación
1. **Implementar paso a paso**: Una clase a la vez
2. **Probar frecuentemente**: Verificar que cada parte funcione
3. **Mantener consistencia**: Seguir el diseño original
4. **Documentar**: Comentar el código

### Fase de Pruebas
1. **Casos simples**: Probar con pocos procesos
2. **Casos complejos**: Probar con muchos procesos
3. **Casos límite**: Probar situaciones especiales
4. **Comparar resultados**: Verificar con cálculos manuales

### Fase de Optimización
1. **Identificar cuellos de botella**: Encontrar partes lentas
2. **Optimizar algoritmos**: Mejorar la eficiencia
3. **Mejorar la interfaz**: Hacer el programa más usable
4. **Pulir la presentación**: Mejorar la salida y reportes

## 12. Python para el Simulador - Sintaxis y Conceptos Específicos

### Diferencias principales con Java/Pascal

#### 1. **Indentación en lugar de llaves**
```python
# Python usa indentación (4 espacios) en lugar de {}
if condicion:
    print("Esto está dentro del if")
    if otra_condicion:
        print("Esto está anidado")
else:
    print("Esto está en el else")
```

#### 2. **No hay declaración de tipos explícita**
```python
# Python infiere el tipo automáticamente
nombre = "P1"  # str
tiempo = 5.0   # float
prioridad = 50 # int
activo = True  # bool
```

#### 3. **Tipos de datos dinámicos**
```python
# Las variables pueden cambiar de tipo
variable = 5      # int
variable = "hola" # str
variable = [1,2,3] # list
```

### Estructuras de datos esenciales

#### **Listas (equivalente a arrays dinámicos)**
```python
# Crear listas
procesos = []  # Lista vacía
procesos = ["P1", "P2", "P3"]  # Lista con elementos
procesos = list()  # Otra forma de crear lista vacía

# Acceder a elementos
primer_proceso = procesos[0]  # Primer elemento
ultimo_proceso = procesos[-1]  # Último elemento

# Agregar elementos
procesos.append("P4")  # Al final
procesos.insert(0, "P0")  # En posición específica

# Eliminar elementos
procesos.remove("P2")  # Por valor
procesos.pop(0)  # Por índice
procesos.pop()  # Último elemento

# Recorrer listas
for proceso in procesos:
    print(proceso)

# Con índice
for i, proceso in enumerate(procesos):
    print(f"Posición {i}: {proceso}")

# Lista de comprensión (muy útil)
tiempos = [p.tiempo_arribo for p in procesos]
```

#### **Diccionarios (equivalente a HashMap en Java)**
```python
# Crear diccionarios
proceso_info = {}  # Diccionario vacío
proceso_info = {"nombre": "P1", "tiempo": 5, "prioridad": 50}

# Acceder a valores
nombre = proceso_info["nombre"]
tiempo = proceso_info.get("tiempo", 0)  # Con valor por defecto

# Agregar/modificar
proceso_info["estado"] = "LISTO"

# Recorrer diccionarios
for clave, valor in proceso_info.items():
    print(f"{clave}: {valor}")

# Solo claves
for clave in proceso_info.keys():
    print(clave)

# Solo valores
for valor in proceso_info.values():
    print(valor)
```

#### **Tuplas (inmutables)**
```python
# Crear tuplas
coordenadas = (10, 20)
proceso_data = ("P1", 0, 5, 50)

# Acceder a elementos
x, y = coordenadas  # Desempaquetado
nombre, tiempo, duracion, prioridad = proceso_data
```

#### **Sets (conjuntos)**
```python
# Crear sets
estados = {"NUEVO", "LISTO", "CORRIENDO"}
estados = set()  # Set vacío

# Operaciones
estados.add("BLOQUEADO")
estados.remove("NUEVO")
estados.discard("TERMINADO")  # No da error si no existe

# Operaciones de conjuntos
estados_activos = {"LISTO", "CORRIENDO"}
estados_inactivos = {"BLOQUEADO", "TERMINADO"}
todos = estados_activos.union(estados_inactivos)
```

### Programación Orientada a Objetos en Python

#### **Definición de clases**
```python
class Proceso:
    # Atributos de clase (compartidos por todas las instancias)
    contador_procesos = 0
    
    def __init__(self, nombre, tiempo_arribo, rafagas_cpu, duracion_rafaga_cpu, 
                 duracion_rafaga_io, prioridad):
        # Atributos de instancia
        self.nombre = nombre
        self.tiempo_arribo = tiempo_arribo
        self.rafagas_cpu = rafagas_cpu
        self.duracion_rafaga_cpu = duracion_rafaga_cpu
        self.duracion_rafaga_io = duracion_rafaga_io
        self.prioridad = prioridad
        
        # Calcular atributos derivados
        self.tiempo_cpu_total = rafagas_cpu * duracion_rafaga_cpu
        self.rafagas_io = rafagas_cpu - 1
        
        # Incrementar contador
        Proceso.contador_procesos += 1
    
    def __str__(self):
        return f"Proceso {self.nombre} (arribo: {self.tiempo_arribo})"
    
    def __repr__(self):
        return f"Proceso('{self.nombre}', {self.tiempo_arribo}, {self.rafagas_cpu})"
    
    def calcular_tiempo_total(self):
        return self.tiempo_cpu_total + (self.rafagas_io * self.duracion_rafaga_io)
```

#### **Herencia**
```python
class AlgoritmoPlanificacion:
    def __init__(self, nombre):
        self.nombre = nombre
    
    def seleccionar_siguiente(self, cola_listos):
        raise NotImplementedError("Debe implementarse en subclase")

class FCFS(AlgoritmoPlanificacion):
    def __init__(self):
        super().__init__("FCFS")
    
    def seleccionar_siguiente(self, cola_listos):
        if cola_listos:
            return cola_listos.pop(0)  # FIFO
        return None
```

#### **Enums (desde Python 3.4)**
```python
from enum import Enum

class EstadoProceso(Enum):
    NUEVO = "NUEVO"
    LISTO = "LISTO"
    CORRIENDO = "CORRIENDO"
    BLOQUEADO = "BLOQUEADO"
    TERMINADO = "TERMINADO"

# Uso
estado = EstadoProceso.LISTO
if estado == EstadoProceso.CORRIENDO:
    print("El proceso está corriendo")
```

### Manejo de archivos

#### **Lectura de archivos**
```python
# Leer archivo completo
with open("procesos.txt", "r") as archivo:
    contenido = archivo.read()

# Leer línea por línea
with open("procesos.txt", "r") as archivo:
    for linea in archivo:
        print(linea.strip())  # strip() quita \n

# Leer todas las líneas en una lista
with open("procesos.txt", "r") as archivo:
    lineas = archivo.readlines()
```

#### **Escritura de archivos**
```python
# Escribir archivo
with open("resultados.txt", "w") as archivo:
    archivo.write("Resultado de la simulación\n")
    archivo.write(f"Tiempo total: {tiempo_total}\n")

# Escribir JSON
import json
datos = {"procesos": [{"nombre": "P1", "tiempo": 5}]}
with open("resultados.json", "w") as archivo:
    json.dump(datos, archivo, indent=2)
```

### Funciones y métodos útiles

#### **Funciones lambda (funciones anónimas)**
```python
# Ordenar lista por prioridad
procesos.sort(key=lambda p: p.prioridad, reverse=True)

# Filtrar procesos
procesos_listos = list(filter(lambda p: p.estado == EstadoProceso.LISTO, procesos))

# Mapear transformaciones
nombres = list(map(lambda p: p.nombre, procesos))
```

#### **Funciones de ordenamiento**
```python
# Ordenar lista in-place
procesos.sort(key=lambda p: p.tiempo_arribo)

# Crear nueva lista ordenada
procesos_ordenados = sorted(procesos, key=lambda p: p.prioridad)

# Ordenar por múltiples criterios
procesos.sort(key=lambda p: (p.prioridad, p.tiempo_arribo))
```

#### **Funciones de agregación**
```python
# Sumar tiempos
tiempo_total = sum(p.tiempo_cpu_total for p in procesos)

# Encontrar máximo/mínimo
proceso_mas_largo = max(procesos, key=lambda p: p.tiempo_cpu_total)
proceso_mas_corto = min(procesos, key=lambda p: p.tiempo_cpu_total)

# Contar elementos
cantidad_listos = sum(1 for p in procesos if p.estado == EstadoProceso.LISTO)
```

### Manejo de errores

#### **Try-except**
```python
try:
    tiempo = float(input("Ingrese tiempo: "))
except ValueError:
    print("Error: debe ingresar un número")
    tiempo = 0.0
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    print("Siempre se ejecuta")
```

### Módulos y paquetes

#### **Importar módulos**
```python
# Importar módulo completo
import json
import os

# Importar funciones específicas
from datetime import datetime
from typing import List, Dict

# Importar con alias
import numpy as np
import pandas as pd

# Importar desde paquete local
from src.dispatcher.proceso import Proceso
from src.dispatcher.algoritmos.fcfs import FCFS
```

#### **Crear módulos**
```python
# En archivo proceso.py
class Proceso:
    pass

# En archivo main.py
from proceso import Proceso
```

### Decoradores (concepto único de Python)

#### **@property (getters/setters automáticos)**
```python
class PCB:
    def __init__(self, proceso):
        self._tiempo_cpu_restante = proceso.tiempo_cpu_total
    
    @property
    def tiempo_cpu_restante(self):
        return self._tiempo_cpu_restante
    
    @tiempo_cpu_restante.setter
    def tiempo_cpu_restante(self, valor):
        if valor < 0:
            raise ValueError("No puede ser negativo")
        self._tiempo_cpu_restante = valor
```

### F-strings (formateo de strings)

```python
# Formateo moderno (Python 3.6+)
nombre = "P1"
tiempo = 5.5
print(f"Proceso {nombre} tiene tiempo {tiempo:.2f}")

# Con expresiones
print(f"Total: {sum(p.tiempo_cpu_total for p in procesos)}")

# Con alineación
print(f"{'Nombre':<10} {'Tiempo':>8}")
print(f"{proceso.nombre:<10} {proceso.tiempo:>8.2f}")
```

### Generadores (eficiencia de memoria)

```python
# Función generadora
def leer_procesos(archivo):
    with open(archivo, 'r') as f:
        for linea in f:
            if linea.strip() and not linea.startswith('#'):
                yield linea.strip().split(',')

# Uso
for datos_proceso in leer_procesos("procesos.txt"):
    proceso = Proceso(*datos_proceso)
    print(proceso)
```

### Type hints (opcional pero recomendado)

```python
from typing import List, Dict, Optional, Union

def procesar_eventos(eventos: List[Evento]) -> Dict[str, float]:
    """Procesa una lista de eventos y retorna métricas"""
    pass

def buscar_proceso(nombre: str, procesos: List[Proceso]) -> Optional[Proceso]:
    """Busca un proceso por nombre, retorna None si no existe"""
    pass
```

## 13. Guía Práctica para Implementar cada Clase

### **Paso 1: Clase `Proceso` (Datos estáticos)**

#### **¿Qué hace?**
Almacena la información que NO cambia durante la simulación.

#### **¿Qué atributos necesita?**
```python
class Proceso:
    def __init__(self, nombre, tiempo_arribo, rafagas_cpu, duracion_rafaga_cpu, 
                 duracion_rafaga_io, prioridad):
        # Datos del archivo (no cambian)
        self.nombre = nombre
        self.tiempo_arribo = tiempo_arribo
        self.rafagas_cpu = rafagas_cpu
        self.duracion_rafaga_cpu = duracion_rafaga_cpu
        self.duracion_rafaga_io = duracion_rafaga_io
        self.prioridad = prioridad
        
        # Cálculos derivados (no cambian)
        self.tiempo_cpu_total = rafagas_cpu * duracion_rafaga_cpu
        self.rafagas_io = rafagas_cpu - 1
```

#### **¿Qué métodos necesita?**
```python
    def __str__(self):
        return f"Proceso {self.nombre}"
    
    def __repr__(self):
        return f"Proceso('{self.nombre}', {self.tiempo_arribo})"
```

### **Paso 2: Clase `PCB` (Datos dinámicos)**

#### **¿Qué hace?**
Almacena la información que SÍ cambia durante la simulación.

#### **¿Qué atributos necesita?**
```python
class PCB:
    def __init__(self, proceso):
        # Referencia al proceso original
        self.proceso = proceso
        
        # Estado actual (cambia)
        self.estado = EstadoProceso.NUEVO
        
        # Control de ejecución (cambia)
        self.rafaga_actual = 0
        self.tiempo_cpu_restante = proceso.tiempo_cpu_total
        self.rafaga_actual_duracion = 0
        self.quantum_restante = 0
        
        # Control de I/O (cambia)
        self.tiempo_io_restante = 0
        self.rafagas_io_restantes = proceso.rafagas_io
        
        # Métricas (se van calculando)
        self.tiempo_retorno = 0
        self.tiempo_en_listo = 0
        self.tiempo_en_corriendo = 0
        self.tiempo_en_bloqueado = 0
```

#### **¿Qué métodos necesita?**
```python
    def iniciar_rafaga(self):
        """Inicia una nueva ráfaga de CPU"""
        self.rafaga_actual += 1
        self.rafaga_actual_duracion = self.proceso.duracion_rafaga_cpu
    
    def terminar_rafaga(self):
        """Termina la ráfaga actual y prepara I/O si es necesario"""
        if self.rafagas_io_restantes > 0:
            self.tiempo_io_restante = self.proceso.duracion_rafaga_io
            self.rafagas_io_restantes -= 1
    
    def actualizar_metricas(self, tiempo_transcurrido):
        """Actualiza las métricas según el estado actual"""
        if self.estado == EstadoProceso.LISTO:
            self.tiempo_en_listo += tiempo_transcurrido
        elif self.estado == EstadoProceso.CORRIENDO:
            self.tiempo_en_corriendo += tiempo_transcurrido
        elif self.estado == EstadoProceso.BLOQUEADO:
            self.tiempo_en_bloqueado += tiempo_transcurrido
```

### **Paso 3: Clase `Evento` (Coordinación temporal)**

#### **¿Qué hace?**
Representa algo que ocurre en un momento específico.

#### **¿Qué atributos necesita?**
```python
class Evento:
    def __init__(self, tipo, tiempo, proceso=None, descripcion=""):
        self.tipo = tipo  # ARRIBO, TERMINO_CPU, TERMINO_IO, etc.
        self.tiempo = tiempo
        self.proceso = proceso
        self.descripcion = descripcion
```

#### **¿Qué métodos necesita?**
```python
    def __lt__(self, other):
        """Para ordenar eventos por tiempo"""
        return self.tiempo < other.tiempo
    
    def __str__(self):
        return f"[{self.tiempo}] {self.tipo}: {self.descripcion}"
```

### **Paso 4: Clase `ColaListos` (Gestión de procesos listos)**

#### **¿Qué hace?**
Maneja los procesos que están listos para ejecutarse.

#### **¿Qué atributos necesita?**
```python
class ColaListos:
    def __init__(self, politica):
        self.politica = politica
        self.procesos = []
```

#### **¿Qué métodos necesita?**
```python
    def agregar_proceso(self, pcb):
        """Agrega un proceso según la política"""
        if self.politica == "FCFS":
            self.procesos.append(pcb)
        elif self.politica == "PRIORIDAD":
            self.procesos.append(pcb)
            self.procesos.sort(key=lambda p: p.proceso.prioridad, reverse=True)
        # ... otras políticas
    
    def obtener_siguiente(self):
        """Obtiene el siguiente proceso según la política"""
        if not self.procesos:
            return None
        
        if self.politica == "FCFS":
            return self.procesos.pop(0)
        elif self.politica == "PRIORIDAD":
            return self.procesos.pop(0)
        # ... otras políticas
    
    def esta_vacia(self):
        return len(self.procesos) == 0
```

### **Paso 5: Clase `Simulador` (Motor principal)**

#### **¿Qué hace?**
Coordina toda la simulación.

#### **¿Qué atributos necesita?**
```python
class Simulador:
    def __init__(self):
        self.tiempo_actual = 0
        self.cola_eventos = []
        self.procesos = []
        self.cola_listos = None
        self.proceso_actual = None
        
        # Métricas globales
        self.tiempo_cpu_total = 0
        self.tiempo_so_total = 0
        self.tiempo_desocupada = 0
        self.eventos = []
```

#### **¿Qué métodos necesita?**
```python
    def cargar_procesos(self, archivo):
        """Carga procesos desde archivo"""
        pass
    
    def configurar_parametros(self, tip, tfp, tcp, quantum):
        """Configura parámetros del sistema"""
        pass
    
    def agregar_evento(self, evento):
        """Agrega un evento a la cola"""
        self.cola_eventos.append(evento)
        self.cola_eventos.sort()  # Ordenar por tiempo
    
    def procesar_evento(self, evento):
        """Procesa un evento específico"""
        pass
    
    def ejecutar_simulacion(self):
        """Ejecuta la simulación completa"""
        while self.cola_eventos:
            evento = self.cola_eventos.pop(0)
            self.tiempo_actual = evento.tiempo
            self.procesar_evento(evento)
    
    def calcular_metricas(self):
        """Calcula métricas finales"""
        pass
```

### **Paso 6: Algoritmos de Planificación**

#### **Patrón común para todos los algoritmos:**
```python
class AlgoritmoBase:
    def __init__(self, nombre):
        self.nombre = nombre
    
    def seleccionar_siguiente(self, cola_listos):
        raise NotImplementedError
    
    def necesita_expropiacion(self, proceso_actual, proceso_nuevo):
        return False

class FCFS(AlgoritmoBase):
    def __init__(self):
        super().__init__("FCFS")
    
    def seleccionar_siguiente(self, cola_listos):
        if cola_listos:
            return cola_listos.pop(0)
        return None
```

### **Orden de implementación recomendado:**

1. **`Proceso`** - Más simple, solo datos
2. **`Evento`** - Simple, solo para ordenar
3. **`PCB`** - Más complejo, pero necesario
4. **`ColaListos`** - Intermedio
5. **`Simulador`** - Más complejo, coordina todo
6. **Algoritmos** - Uno por uno, empezando por FCFS

### **Consejos para cada paso:**

#### **Para `Proceso`:**
- Solo getters, no setters
- Calcular atributos derivados en `__init__`
- Implementar `__str__` y `__repr__`

#### **Para `PCB`:**
- Muchos setters para cambiar estado
- Métodos para actualizar métricas
- Validar transiciones de estado

#### **Para `Evento`:**
- Implementar `__lt__` para ordenar
- Descriptores claros para debugging

#### **Para `ColaListos`:**
- Un método por política
- Manejar casos especiales (quantum, expropiación)

#### **Para `Simulador`:**
- Separar lógica de eventos
- Calcular métricas en tiempo real
- Manejar archivos de salida

#### **Para Algoritmos:**
- Patrón común para todos
- Casos especiales en subclases
- Testing individual de cada uno

### **Testing recomendado:**

```python
# Test básico para cada clase
def test_proceso():
    p = Proceso("P1", 0, 3, 5, 2, 50)
    assert p.tiempo_cpu_total == 15
    assert p.rafagas_io == 2

def test_pcb():
    p = Proceso("P1", 0, 3, 5, 2, 50)
    pcb = PCB(p)
    assert pcb.estado == EstadoProceso.NUEVO
    assert pcb.tiempo_cpu_restante == 15
```

