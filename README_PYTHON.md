# 🐍 Guía de Python para el Proyecto de Planificación de Procesos

## 📚 Introducción

Esta guía está diseñada específicamente para ayudarte a aprender Python desde cero hasta el nivel necesario para implementar el simulador de planificación de procesos. Está organizada de manera progresiva, empezando con conceptos básicos y avanzando hacia técnicas más complejas.

## 🎯 Objetivos de Aprendizaje

Al final de esta guía serás capaz de:
- **Escribir código Python** estructurado y legible
- **Implementar algoritmos** de planificación de procesos
- **Manejar estructuras de datos** complejas
- **Crear clases y objetos** para modelar el sistema
- **Gestionar archivos** y generar reportes
- **Integrar tu código** con la interfaz gráfica existente

## 🚀 Conceptos Básicos (Semana 1)

### 1. Variables y Tipos de Datos

#### Variables
```python
# Asignación de variables
nombre = "Proceso1"
tiempo_arribo = 0
rafagas_cpu = 3
duracion_rafaga = 5
prioridad = 50
es_activo = True

# Imprimir variables
print(f"Proceso: {nombre}, Arribo: {tiempo_arribo}")
print("Ráfagas de CPU:", rafagas_cpu)
```

#### Tipos de Datos Fundamentales
```python
# Enteros (int)
tiempo_total = 100
quantum = 2

# Flotantes (float)
tiempo_promedio = 15.5
porcentaje_cpu = 75.8

# Cadenas (str)
nombre_proceso = "P1"
estado = "ejecutando"

# Booleanos (bool)
proceso_terminado = False
cpu_disponible = True

# Verificar tipos
print(type(tiempo_total))      # <class 'int'>
print(type(tiempo_promedio))   # <class 'float'>
print(type(nombre_proceso))    # <class 'str'>
```

### 2. Operadores

#### Operadores Aritméticos
```python
# Operaciones básicas
tiempo_inicio = 10
tiempo_fin = 25
duracion = tiempo_fin - tiempo_inicio  # 15

# Operaciones con procesos
tiempo_total_cpu = rafagas_cpu * duracion_rafaga  # 3 * 5 = 15
tiempo_restante = tiempo_total_cpu - tiempo_ya_ejecutado

# División
tiempo_promedio = tiempo_total / cantidad_procesos
tiempo_medio = tiempo_total // cantidad_procesos  # División entera
```

#### Operadores de Comparación
```python
# Comparaciones para planificación
if prioridad > 50:
    print("Proceso de alta prioridad")
elif prioridad == 50:
    print("Prioridad media")
else:
    print("Prioridad baja")

# Comparaciones múltiples
if 1 <= prioridad <= 100:
    print("Prioridad válida")
```

#### Operadores Lógicos
```python
# Lógica para decisiones de planificación
if proceso_activo and cpu_disponible:
    print("Proceso puede ejecutar")

if not proceso_bloqueado:
    print("Proceso no está bloqueado")

# Combinaciones lógicas
if (prioridad > 50) or (tiempo_restante < 2):
    print("Proceso debe ejecutar pronto")
```

### 3. Estructuras de Control

#### Condicionales (if/elif/else)
```python
def determinar_proximo_proceso(procesos_listos):
    if not procesos_listos:
        return None
    elif len(procesos_listos) == 1:
        return procesos_listos[0]
    else:
        # Lógica para seleccionar entre múltiples procesos
        return seleccionar_por_politica(procesos_listos)

def seleccionar_por_politica(procesos):
    politica = obtener_politica_actual()
    
    if politica == "FCFS":
        return procesos[0]  # Primero en llegar
    elif politica == "SPN":
        return min(procesos, key=lambda p: p.tiempo_total_cpu)
    elif politica == "Prioridad":
        return max(procesos, key=lambda p: p.prioridad)
    else:
        return procesos[0]  # Default
```

#### Bucles (for/while)
```python
# Bucle for para procesar lista de procesos
def procesar_todos_procesos(procesos):
    for proceso in procesos:
        print(f"Procesando: {proceso.nombre}")
        tiempo_procesamiento = calcular_tiempo(proceso)
        print(f"Tiempo requerido: {tiempo_procesamiento}")

# Bucle while para simulación temporal
def simular_tiempo(tiempo_maximo):
    tiempo_actual = 0
    while tiempo_actual < tiempo_maximo:
        print(f"Tiempo actual: {tiempo_actual}")
        ejecutar_ciclo_simulacion()
        tiempo_actual += 1

# Bucle con enumerate para índices
def listar_procesos_con_indice(procesos):
    for i, proceso in enumerate(procesos):
        print(f"{i+1}. {proceso.nombre} - Prioridad: {proceso.prioridad}")
```

### 4. Listas y Manipulación Básica

#### Crear y Manipular Listas
```python
# Lista de procesos
procesos = ["P1", "P2", "P3", "P4"]

# Lista de tiempos
tiempos_arribo = [0, 2, 4, 6]

# Lista mixta
datos_proceso = ["P1", 0, 3, 5, 2, 50]

# Acceder a elementos
primer_proceso = procesos[0]      # "P1"
ultimo_proceso = procesos[-1]     # "P4"
procesos_rango = procesos[1:3]    # ["P2", "P3"]

# Agregar elementos
procesos.append("P5")
procesos.insert(1, "P1.5")

# Eliminar elementos
procesos.remove("P2")
proceso_eliminado = procesos.pop(0)
```

#### Operaciones con Listas
```python
# Longitud de la lista
cantidad_procesos = len(procesos)

# Verificar si existe
if "P1" in procesos:
    print("P1 está en la lista")

# Ordenar listas
procesos_ordenados = sorted(procesos)
tiempos_ordenados = sorted(tiempos_arribo, reverse=True)

# Encontrar elementos
indice_p1 = procesos.index("P1")
if "P5" in procesos:
    indice_p5 = procesos.index("P5")

# Contar ocurrencias
cantidad_p1 = procesos.count("P1")
```

## 🔧 Conceptos Intermedios (Semana 2)

### 1. Funciones

#### Definición y Uso Básico
```python
def saludar():
    print("¡Hola desde Python!")

def saludar_proceso(nombre_proceso):
    print(f"¡Hola proceso {nombre_proceso}!")

def calcular_tiempo_total(rafagas, duracion):
    return rafagas * duracion

# Llamadas a funciones
saludar()
saludar_proceso("P1")
tiempo_total = calcular_tiempo_total(3, 5)  # 15
```

#### Parámetros y Retorno
```python
def procesar_proceso(nombre, tiempo_arribo, prioridad, rafagas_cpu=1):
    """
    Procesa un proceso con sus parámetros.
    
    Args:
        nombre: Nombre del proceso
        tiempo_arribo: Momento de llegada
        prioridad: Prioridad del proceso (1-100)
        rafagas_cpu: Cantidad de ráfagas (default: 1)
    
    Returns:
        dict: Información del proceso procesado
    """
    proceso = {
        'nombre': nombre,
        'tiempo_arribo': tiempo_arribo,
        'prioridad': prioridad,
        'rafagas_cpu': rafagas_cpu,
        'estado': 'nuevo'
    }
    
    return proceso

# Uso de la función
proceso1 = procesar_proceso("P1", 0, 50, 3)
proceso2 = procesar_proceso("P2", 2, 30)  # rafagas_cpu = 1 por defecto
```

#### Funciones con Múltiples Retornos
```python
def analizar_proceso(proceso):
    tiempo_total = proceso['rafagas_cpu'] * proceso['duracion_rafaga']
    es_prioritario = proceso['prioridad'] > 50
    categoria = "alta" if es_prioritario else "baja"
    
    return tiempo_total, es_prioritario, categoria

# Desempaquetar múltiples valores
tiempo, es_prio, cat = analizar_proceso(proceso1)
print(f"Tiempo: {tiempo}, Prioritario: {es_prio}, Categoría: {cat}")
```

### 2. Diccionarios

#### Crear y Manipular Diccionarios
```python
# Diccionario de proceso
proceso = {
    'nombre': 'P1',
    'tiempo_arribo': 0,
    'rafagas_cpu': 3,
    'duracion_rafaga': 5,
    'duracion_io': 2,
    'prioridad': 50,
    'estado': 'nuevo'
}

# Acceder a valores
nombre = proceso['nombre']
prioridad = proceso.get('prioridad', 0)  # Con valor por defecto

# Modificar valores
proceso['estado'] = 'listo'
proceso['tiempo_restante'] = 15

# Agregar nuevas claves
proceso['tiempo_inicio'] = 0
proceso['tiempo_fin'] = None

# Verificar si existe una clave
if 'estado' in proceso:
    print(f"Estado: {proceso['estado']}")
```

#### Operaciones con Diccionarios
```python
# Obtener todas las claves y valores
claves = proceso.keys()
valores = proceso.values()
items = proceso.items()

# Iterar sobre diccionario
for clave, valor in proceso.items():
    print(f"{clave}: {valor}")

# Copiar diccionario
proceso_copia = proceso.copy()
proceso_copia_profunda = copy.deepcopy(proceso)

# Combinar diccionarios
configuracion_base = {'tip': 1, 'tfp': 1, 'tcp': 1}
configuracion_personalizada = {'tip': 2, 'quantum': 3}
configuracion_final = {**configuracion_base, **configuracion_personalizada}
```

### 3. Manejo de Archivos

#### Lectura de Archivos
```python
def leer_archivo_procesos(ruta_archivo):
    """Lee un archivo de procesos y retorna una lista de diccionarios"""
    procesos = []
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for numero_linea, linea in enumerate(archivo, 1):
                linea = linea.strip()
                
                # Ignorar líneas vacías y comentarios
                if not linea or linea.startswith('#'):
                    continue
                
                try:
                    # Parsear línea CSV
                    campos = linea.split(',')
                    if len(campos) != 6:
                        print(f"Error en línea {numero_linea}: formato incorrecto")
                        continue
                    
                    proceso = {
                        'nombre': campos[0].strip(),
                        'tiempo_arribo': int(campos[1].strip()),
                        'rafagas_cpu': int(campos[2].strip()),
                        'duracion_rafaga': int(campos[3].strip()),
                        'duracion_io': int(campos[4].strip()),
                        'prioridad': int(campos[5].strip())
                    }
                    
                    # Validar datos
                    if not validar_proceso(proceso):
                        print(f"Error en línea {numero_linea}: datos inválidos")
                        continue
                    
                    procesos.append(proceso)
                    
                except ValueError as e:
                    print(f"Error en línea {numero_linea}: {e}")
                    continue
                    
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_archivo}")
    except Exception as e:
        print(f"Error al leer archivo: {e}")
    
    return procesos

def validar_proceso(proceso):
    """Valida que los datos del proceso sean correctos"""
    if proceso['prioridad'] < 1 or proceso['prioridad'] > 100:
        return False
    if proceso['tiempo_arribo'] < 0:
        return False
    if proceso['rafagas_cpu'] <= 0:
        return False
    if proceso['duracion_rafaga'] <= 0:
        return False
    if proceso['duracion_io'] < 0:
        return False
    return True
```

#### Escritura de Archivos
```python
def escribir_log_eventos(eventos, ruta_archivo):
    """Escribe un log de eventos en un archivo"""
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write("# Log de Eventos de la Simulación\n")
            archivo.write("# Formato: [Tiempo] Tipo de Evento - Proceso\n")
            archivo.write("=" * 50 + "\n\n")
            
            for evento in eventos:
                linea = f"[{evento['tiempo']}] {evento['tipo']} - {evento['proceso']}\n"
                archivo.write(linea)
                
        print(f"Log guardado en: {ruta_archivo}")
        
    except Exception as e:
        print(f"Error al escribir archivo: {e}")

def escribir_metricas(metricas, ruta_archivo):
    """Escribe métricas de la simulación en formato JSON"""
    import json
    
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(metricas, archivo, indent=2, ensure_ascii=False)
            
        print(f"Métricas guardadas en: {ruta_archivo}")
        
    except Exception as e:
        print(f"Error al escribir métricas: {e}")
```

### 4. Manejo de Excepciones

#### Try/Except Básico
```python
def procesar_entrada_usuario(valor):
    try:
        numero = int(valor)
        if numero < 0:
            raise ValueError("El número debe ser positivo")
        return numero
    except ValueError as e:
        print(f"Error de conversión: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

# Uso
tip = procesar_entrada_usuario("2")      # 2
tfp = procesar_entrada_usuario("-1")     # None, muestra error
quantum = procesar_entrada_usuario("abc") # None, muestra error
```

#### Try/Except Avanzado
```python
def cargar_configuracion(ruta_archivo):
    """Carga configuración del sistema con manejo robusto de errores"""
    configuracion_default = {
        'tip': 1,
        'tfp': 1,
        'tcp': 1,
        'quantum': 2
    }
    
    try:
        with open(ruta_archivo, 'r') as archivo:
            configuracion = json.load(archivo)
            
        # Validar configuración cargada
        for clave, valor in configuracion.items():
            if clave not in configuracion_default:
                print(f"Clave desconocida ignorada: {clave}")
                continue
            if not isinstance(valor, (int, float)) or valor < 0:
                print(f"Valor inválido para {clave}: {valor}")
                configuracion[clave] = configuracion_default[clave]
                
        return configuracion
        
    except FileNotFoundError:
        print(f"Archivo de configuración no encontrado, usando valores por defecto")
        return configuracion_default
    except json.JSONDecodeError as e:
        print(f"Error en formato JSON: {e}")
        return configuracion_default
    except Exception as e:
        print(f"Error inesperado: {e}")
        return configuracion_default
```

## 🏗️ Conceptos Avanzados (Semana 3)

### 1. Clases y Objetos

#### Clase Básica
```python
class Proceso:
    """Clase que representa un proceso en el sistema"""
    
    def __init__(self, nombre, tiempo_arribo, rafagas_cpu, duracion_rafaga, 
                 duracion_io, prioridad):
        self.nombre = nombre
        self.tiempo_arribo = tiempo_arribo
        self.rafagas_cpu = rafagas_cpu
        self.duracion_rafaga = duracion_rafaga
        self.duracion_io = duracion_io
        self.prioridad = prioridad
        
        # Estado del proceso
        self.estado = 'nuevo'
        self.tiempo_restante = rafagas_cpu * duracion_rafaga
        self.tiempo_inicio = None
        self.tiempo_fin = None
        self.tiempo_estado_listo = 0
        self.tiempo_estado_ejecutando = 0
        self.tiempo_estado_bloqueado = 0
    
    def calcular_tiempo_total_cpu(self):
        """Calcula el tiempo total de CPU necesario"""
        return self.rafagas_cpu * self.duracion_rafaga
    
    def calcular_tiempo_total_io(self):
        """Calcula el tiempo total de I/O necesario"""
        return (self.rafagas_cpu - 1) * self.duracion_io
    
    def esta_terminado(self):
        """Verifica si el proceso ha terminado"""
        return self.tiempo_restante <= 0
    
    def ejecutar_cpu(self, tiempo):
        """Ejecuta el proceso en CPU por un tiempo determinado"""
        if self.estado != 'listo':
            raise ValueError(f"Proceso {self.nombre} no está listo para ejecutar")
        
        tiempo_ejecutado = min(tiempo, self.tiempo_restante)
        self.tiempo_restante -= tiempo_ejecutado
        self.tiempo_estado_ejecutando += tiempo_ejecutado
        
        if self.tiempo_restante <= 0:
            self.estado = 'terminado'
            self.tiempo_fin = self.tiempo_inicio + self.tiempo_estado_ejecutando
        else:
            self.estado = 'bloqueado'
        
        return tiempo_ejecutado
    
    def __str__(self):
        """Representación en string del proceso"""
        return (f"Proceso {self.nombre} (Estado: {self.estado}, "
                f"Prioridad: {self.prioridad}, Tiempo Restante: {self.tiempo_restante})")
    
    def __repr__(self):
        """Representación técnica del proceso"""
        return f"Proceso('{self.nombre}', {self.tiempo_arribo}, {self.rafagas_cpu}, {self.duracion_rafaga}, {self.duracion_io}, {self.prioridad})"

# Uso de la clase
proceso1 = Proceso("P1", 0, 3, 5, 2, 50)
print(proceso1)
print(f"Tiempo total CPU: {proceso1.calcular_tiempo_total_cpu()}")
```

#### Métodos Especiales y Propiedades
```python
class Proceso:
    def __init__(self, nombre, tiempo_arribo, rafagas_cpu, duracion_rafaga, 
                 duracion_io, prioridad):
        # ... código anterior ...
        self._tiempo_restante = rafagas_cpu * duracion_rafaga
    
    @property
    def tiempo_restante(self):
        """Propiedad para acceder al tiempo restante"""
        return self._tiempo_restante
    
    @tiempo_restante.setter
    def tiempo_restante(self, valor):
        """Setter para el tiempo restante con validación"""
        if valor < 0:
            raise ValueError("El tiempo restante no puede ser negativo")
        self._tiempo_restante = valor
    
    def __lt__(self, otro):
        """Comparación para ordenamiento por prioridad"""
        return self.prioridad > otro.prioridad  # Mayor prioridad primero
    
    def __eq__(self, otro):
        """Comparación de igualdad"""
        return (self.nombre == otro.nombre and 
                self.tiempo_arribo == otro.tiempo_arribo)
    
    def __hash__(self):
        """Hash para usar en sets y diccionarios"""
        return hash((self.nombre, self.tiempo_arribo))

# Uso de comparaciones
proceso1 = Proceso("P1", 0, 3, 5, 2, 50)
proceso2 = Proceso("P2", 2, 2, 3, 1, 80)

if proceso1 < proceso2:  # Usa __lt__
    print(f"{proceso2.nombre} tiene mayor prioridad que {proceso1.nombre}")
```

### 2. Herencia y Polimorfismo

#### Clase Base y Herencia
```python
class Planificador:
    """Clase base para todos los algoritmos de planificación"""
    
    def __init__(self, nombre):
        self.nombre = nombre
        self.procesos_listos = []
        self.proceso_actual = None
        self.tiempo_actual = 0
    
    def agregar_proceso(self, proceso):
        """Agrega un proceso a la cola de listos"""
        self.procesos_listos.append(proceso)
        proceso.estado = 'listo'
    
    def obtener_proximo_proceso(self):
        """Método abstracto que debe ser implementado por subclases"""
        raise NotImplementedError("Subclase debe implementar este método")
    
    def ejecutar_ciclo(self):
        """Ejecuta un ciclo de planificación"""
        if not self.proceso_actual and self.procesos_listos:
            self.proceso_actual = self.obtener_proximo_proceso()
            self.procesos_listos.remove(self.proceso_actual)
            self.proceso_actual.estado = 'ejecutando'
        
        if self.proceso_actual:
            tiempo_ejecutado = self.proceso_actual.ejecutar_cpu(1)
            self.tiempo_actual += 1
            
            if self.proceso_actual.estado == 'terminado':
                self.proceso_actual = None
            elif self.proceso_actual.estado == 'bloqueado':
                self.proceso_actual = None

class PlanificadorFCFS(Planificador):
    """Planificador First Come First Served"""
    
    def __init__(self):
        super().__init__("FCFS")
    
    def obtener_proximo_proceso(self):
        """Retorna el primer proceso que llegó (FIFO)"""
        if self.procesos_listos:
            return self.procesos_listos[0]
        return None

class PlanificadorPrioridad(Planificador):
    """Planificador por Prioridad Externa"""
    
    def __init__(self):
        super().__init__("Prioridad")
    
    def obtener_proximo_proceso(self):
        """Retorna el proceso con mayor prioridad"""
        if self.procesos_listos:
            return max(self.procesos_listos, key=lambda p: p.prioridad)
        return None
    
    def agregar_proceso(self, proceso):
        """Agrega proceso y verifica si debe expropiar"""
        super().agregar_proceso(proceso)
        
        # Expropiación si el nuevo proceso tiene mayor prioridad
        if (self.proceso_actual and 
            proceso.prioridad > self.proceso_actual.prioridad):
            self.procesos_listos.append(self.proceso_actual)
            self.proceso_actual.estado = 'listo'
            self.proceso_actual = None

# Uso de herencia
planificador_fcfs = PlanificadorFCFS()
planificador_prioridad = PlanificadorPrioridad()

# Ambos pueden usar métodos de la clase base
planificador_fcfs.agregar_proceso(proceso1)
planificador_prioridad.agregar_proceso(proceso2)
```

### 3. List Comprehensions y Expresiones Lambda

#### List Comprehensions
```python
# Crear lista de procesos activos
procesos_activos = [p for p in procesos if p.estado != 'terminado']

# Crear lista de nombres de procesos
nombres_procesos = [p.nombre for p in procesos]

# Crear lista de procesos con prioridad alta
procesos_altos = [p for p in procesos if p.prioridad > 50]

# Crear lista de tuplas (nombre, prioridad)
info_procesos = [(p.nombre, p.prioridad) for p in procesos]

# List comprehension con condición
tiempos_arribo = [p.tiempo_arribo for p in procesos if p.tiempo_arribo > 0]

# List comprehension anidada
procesos_por_estado = {
    estado: [p.nombre for p in procesos if p.estado == estado]
    for estado in ['nuevo', 'listo', 'ejecutando', 'bloqueado', 'terminado']
}
```

#### Expresiones Lambda
```python
# Ordenar procesos por prioridad
procesos_ordenados = sorted(procesos, key=lambda p: p.prioridad, reverse=True)

# Ordenar por tiempo de arribo
procesos_por_arribo = sorted(procesos, key=lambda p: p.tiempo_arribo)

# Ordenar por tiempo restante (para SRTN)
procesos_por_tiempo = sorted(procesos, key=lambda p: p.tiempo_restante)

# Filtrar procesos con filter
procesos_listos = list(filter(lambda p: p.estado == 'listo', procesos))

# Mapear procesos a tiempos totales
tiempos_totales = list(map(lambda p: p.calcular_tiempo_total_cpu(), procesos))

# Encontrar proceso con mayor prioridad
proceso_max_prioridad = max(procesos, key=lambda p: p.prioridad)

# Encontrar proceso con menor tiempo restante
proceso_min_tiempo = min(procesos, key=lambda p: p.tiempo_restante)
```

### 4. Generadores y Iteradores

#### Generadores Básicos
```python
def generar_eventos_simulacion(procesos, tiempo_maximo):
    """Genera eventos de simulación uno por uno"""
    tiempo_actual = 0
    
    while tiempo_actual < tiempo_maximo:
        # Generar eventos para este tiempo
        for proceso in procesos:
            if proceso.tiempo_arribo == tiempo_actual:
                yield {
                    'tiempo': tiempo_actual,
                    'tipo': 'arribo',
                    'proceso': proceso.nombre
                }
        
        tiempo_actual += 1

# Uso del generador
for evento in generar_eventos_simulacion(procesos, 100):
    print(f"[{evento['tiempo']}] {evento['tipo']} - {evento['proceso']}")
```

#### Generadores de Expresión
```python
# Generar tiempos de arribo
tiempos_arribo = (p.tiempo_arribo for p in procesos)

# Generar nombres de procesos activos
nombres_activos = (p.nombre for p in procesos if p.estado != 'terminado')

# Generar pares (nombre, prioridad) para procesos listos
info_listos = ((p.nombre, p.prioridad) for p in procesos if p.estado == 'listo')
```

## 🔌 Integración con la Interfaz (Semana 4)

### 1. Estructura de Datos para la Interfaz

#### Formato de Datos Esperado
```python
def preparar_datos_para_interfaz(resultados_simulacion):
    """Prepara los datos del simulador para la interfaz"""
    
    datos_interfaz = {
        'eventos': [],
        'metricas_procesos': {},
        'metricas_tanda': {},
        'uso_cpu': {},
        'diagrama_gantt': {
            'procesos': [],
            'inicios': [],
            'duraciones': [],
            'colores': []
        }
    }
    
    # Convertir eventos
    for evento in resultados_simulacion.eventos:
        datos_interfaz['eventos'].append({
            'tiempo': evento.tiempo,
            'tipo': evento.tipo,
            'proceso': evento.proceso.nombre
        })
    
    # Convertir métricas de procesos
    for proceso in resultados_simulacion.procesos:
        datos_interfaz['metricas_procesos'][proceso.nombre] = {
            'tiempo_retorno': proceso.tiempo_fin - proceso.tiempo_arribo,
            'tiempo_retorno_normalizado': (proceso.tiempo_fin - proceso.tiempo_arribo) / proceso.tiempo_estado_ejecutando,
            'tiempo_estado_listo': proceso.tiempo_estado_listo
        }
    
    # Calcular métricas de la tanda
    tiempos_retorno = [m['tiempo_retorno'] for m in datos_interfaz['metricas_procesos'].values()]
    datos_interfaz['metricas_tanda'] = {
        'tiempo_retorno_total': max(tiempos_retorno),
        'tiempo_medio_retorno': sum(tiempos_retorno) / len(tiempos_retorno)
    }
    
    # Calcular uso de CPU
    tiempo_total = resultados_simulacion.tiempo_final
    tiempo_cpu_procesos = sum(p.tiempo_estado_ejecutando for p in resultados_simulacion.procesos)
    tiempo_cpu_so = resultados_simulacion.tiempo_tip + resultados_simulacion.tiempo_tfp + resultados_simulacion.tiempo_tcp
    
    datos_interfaz['uso_cpu'] = {
        'desocupada': tiempo_total - tiempo_cpu_procesos - tiempo_cpu_so,
        'por_so': tiempo_cpu_so,
        'por_procesos': tiempo_cpu_procesos
    }
    
    # Preparar diagrama de Gantt
    for proceso in resultados_simulacion.procesos:
        if proceso.tiempo_inicio is not None:
            datos_interfaz['diagrama_gantt']['procesos'].append(proceso.nombre)
            datos_interfaz['diagrama_gantt']['inicios'].append(proceso.tiempo_inicio)
            datos_interfaz['diagrama_gantt']['duraciones'].append(proceso.tiempo_estado_ejecutando)
            datos_interfaz['diagrama_gantt']['colores'].append(f'#{hash(proceso.nombre) % 0xFFFFFF:06x}')
    
    return datos_interfaz
```

### 2. Conectar Simulador con Interfaz

#### Método Principal de Conexión
```python
def conectar_simulador_con_interfaz(self, resultados_simulacion):
    """Conecta los resultados del simulador con la interfaz"""
    
    # Preparar datos para la interfaz
    datos_interfaz = preparar_datos_para_interfaz(resultados_simulacion)
    
    # Actualizar interfaz
    self._actualizar_log_eventos(datos_interfaz['eventos'])
    self._actualizar_estadisticas(
        datos_interfaz['metricas_procesos'],
        datos_interfaz['metricas_tanda'],
        datos_interfaz['uso_cpu']
    )
    self._actualizar_diagrama_gantt(datos_interfaz['diagrama_gantt'])
    
    # Cambiar a pestaña de resultados
    self._cambiar_tab("resultados")
    
    # Actualizar estado
    self.label_estado.configure(
        text="Estado: Simulación completada exitosamente",
        text_color="lightgreen"
    )
```

## 📚 Ejercicios Prácticos

### Ejercicio 1: Crear Clase Proceso
```python
# Implementa la clase Proceso completa con todos los métodos necesarios
# Prueba creando varios procesos y ejecutándolos

procesos_ejemplo = [
    Proceso("P1", 0, 3, 5, 2, 50),
    Proceso("P2", 2, 2, 3, 1, 80),
    Proceso("P3", 4, 1, 8, 0, 30)
]

for proceso in procesos_ejemplo:
    print(proceso)
    print(f"Tiempo total CPU: {proceso.calcular_tiempo_total_cpu()}")
    print(f"Tiempo total I/O: {proceso.calcular_tiempo_total_io()}")
    print()
```

### Ejercicio 2: Implementar Planificador FCFS
```python
# Implementa el planificador FCFS y prueba con los procesos de ejemplo
planificador = PlanificadorFCFS()

for proceso in procesos_ejemplo:
    planificador.agregar_proceso(proceso)

# Simula algunos ciclos
for _ in range(10):
    planificador.ejecutar_ciclo()
    print(f"Tiempo: {planificador.tiempo_actual}")
    if planificador.proceso_actual:
        print(f"Ejecutando: {planificador.proceso_actual.nombre}")
    print()
```

### Ejercicio 3: Leer y Validar Archivo
```python
# Crea un archivo de procesos y prueba la función de lectura
procesos_leidos = leer_archivo_procesos("data/procesos_ejemplo.txt")
print(f"Procesos leídos: {len(procesos_leidos)}")

for proceso in procesos_leidos:
    print(proceso)
```

## 🎯 Próximos Pasos

1. **Practica** todos los conceptos básicos hasta que te sientas cómodo
2. **Implementa** las clases Proceso y Planificador paso a paso
3. **Prueba** cada componente individualmente antes de integrar
4. **Conecta** tu simulador con la interfaz existente
5. **Optimiza** y mejora el código continuamente

## 📖 Recursos Adicionales

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python Tutorials](https://realpython.com/)
- [Python for Everybody](https://www.py4e.com/)
- [Python Crash Course](https://ehmatthes.github.io/pcc/)

---

**💡 Consejo**: La mejor manera de aprender Python es practicando. Implementa cada concepto en pequeños programas antes de integrarlo en el proyecto principal. ¡No te desanimes si algo no funciona al principio, es parte del aprendizaje!
