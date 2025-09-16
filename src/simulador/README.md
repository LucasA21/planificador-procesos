# Guía Completa del Simulador de Planificación de Procesos

## Índice
1. [Introducción General](#introducción-general)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Clase Proceso](#clase-proceso)
4. [Algoritmo FCFS](#algoritmo-fcfs)
5. [Simulador Principal](#simulador-principal)
6. [Exportador PDF](#exportador-pdf)
7. [Conexión con la Interfaz de Usuario](#conexión-con-la-interfaz-de-usuario)
8. [Implementación de Nuevos Algoritmos](#implementación-de-nuevos-algoritmos)

---

## Introducción General

El simulador de planificación de procesos es una aplicación completa que permite simular diferentes algoritmos de planificación de procesos del sistema operativo. El sistema está diseñado de manera modular para facilitar la implementación de nuevos algoritmos y mantener una separación clara entre la lógica de negocio y la interfaz de usuario.

### Componentes Principales:
- **Modelo de Datos**: Clase `Proceso` que representa un proceso individual
- **Algoritmos**: Implementaciones específicas de algoritmos de planificación
- **Simulador**: Coordinador principal que ejecuta las simulaciones
- **Exportador**: Generación de reportes en PDF
- **Interfaz**: UI moderna con CustomTkinter

---

## Estructura del Proyecto

```
src/simulador/
├── __init__.py              # Módulo principal
├── proceso.py               # Clase Proceso
├── simulador.py             # Simulador principal
├── exportador_pdf.py        # Generador de PDFs
└── algoritmos/
    ├── __init__.py
    ├── FCFS.py              # Algoritmo FCFS implementado
    ├── SPN.py               # Algoritmo SPN implementado
    ├── SRTN.py              # Algoritmo SRTN implementado
    ├── RR.py                # Algoritmo Round Robin implementado
    └── PrioridadExterna.py  # Algoritmo de Prioridad Externa (por implementar)
```

---

## Clase Proceso

### Ubicación: `src/simulador/proceso.py`

La clase `Proceso` es el modelo de datos fundamental que representa un proceso individual en el sistema.

### Atributos Principales:

#### Atributos de Entrada (configurados por el usuario):
- `nombre`: Identificador único del proceso (ej: "P1", "P2")
- `tiempo_arrivo`: Momento en que el proceso llega al sistema
- `cantidad_rafagas_cpu`: Número total de ráfagas de CPU que necesita ejecutar
- `duracion_rafagas_cpu`: Duración de cada ráfaga de CPU
- `duracion_rafagas_io`: Duración de cada ráfaga de I/O
- `prioridad`: Nivel de prioridad del proceso (para algoritmos que la usen)

#### Atributos de Control Interno:
- `estado`: Estado actual del proceso ("nuevo", "listo", "ejecutando", "bloqueado", "terminado")
- `proceso_nuevo`: Flag que indica si es la primera vez que se ejecuta
- `duracion_rafagas_cpu_original`: Copia de seguridad para cálculos
- `duracion_rafagas_io_original`: Copia de seguridad para cálculos
- `cantidad_rafagas_cpu_original`: Copia de seguridad para cálculos

#### Atributos de Medición:
- `tiempo_retorno`: Tiempo total desde llegada hasta finalización
- `tiempo_retorno_normalizado`: Tiempo de retorno normalizado por el tiempo de servicio
- `tiempo_en_listo`: Tiempo total que el proceso estuvo en estado listo
- `tiempo_bloqueado`: Tiempo total que el proceso estuvo bloqueado
- `tiempo_espera`: Tiempo total de espera
- `tiempo_rafaga_cpu`: Tiempo restante de la ráfaga actual de CPU

### Métodos Principales:

#### Getters:
```python
get_tiempo_arribo()          # Retorna tiempo de llegada
get_cantidad_rafagas_cpu()   # Retorna cantidad total de ráfagas
get_duracion_rafagas_cpu()   # Retorna duración original de ráfagas CPU
get_duracion_rafagas_io()    # Retorna duración original de ráfagas I/O
get_prioridad()              # Retorna prioridad del proceso
get_estado()                 # Retorna estado actual
```

#### Control de Estado:
```python
set_estado(estado)           # Cambia el estado del proceso
```

#### Cálculos:
```python
calcular_tiempo_retorno(tiempo_finalizacion)
# Calcula:
# - tiempo_retorno = tiempo_finalizacion - tiempo_arrivo
# - tiempo_retorno_normalizado = tiempo_retorno / tiempo_servicio_total
```

### Ejemplo de Uso:
```python
proceso = Proceso(
    nombre="P1",
    tiempo_arrivo=0,
    cantidad_rafagas_cpu=3,
    duracion_rafagas_cpu=5,
    duracion_rafagas_io=2,
    prioridad=1
)
```

---

## Algoritmo FCFS

### Ubicación: `src/simulador/algoritmos/FCFS.py`

El algoritmo FCFS (First Come First Served) es el más simple de los algoritmos de planificación. Los procesos se ejecutan en el orden de llegada, sin interrupciones hasta completar su ráfaga de CPU.

### Clase FCFS

#### Atributos de Configuración:
- `procesos`: Lista de procesos a simular
- `tiempo_tip`: Tiempo de Inicio de Proceso (tiempo del SO para cargar proceso)
- `tiempo_tcp`: Tiempo de Cambio de Proceso (tiempo del SO para cambiar contexto)
- `tiempo_tfp`: Tiempo de Finalización de Proceso (tiempo del SO para terminar proceso)

#### Atributos de Estado:
- `tiempo_actual`: Contador de tiempo de la simulación
- `proceso_actual`: Proceso que está ejecutándose actualmente
- `cola_listos`: Cola FIFO de procesos listos para ejecutar
- `procesos_bloqueados`: Lista de procesos ejecutando I/O
- `procesos_terminados`: Lista de procesos que han terminado

#### Atributos de Control:
- `tiempo_restante_bloqueo`: Tiempo restante de TIP/TCP/TFP
- `tipo_bloqueo`: Tipo de bloqueo actual ("tip", "tcp", "tfp")

#### Atributos de Medición:
- `cpu_proc`: Tiempo real de CPU ejecutando procesos
- `cpu_so`: Tiempo real de CPU en labores del sistema operativo
- `cpu_idle`: Tiempo real de CPU desocupada
- `resultados`: Lista de todos los eventos de la simulación

### Métodos Principales:

#### Método Principal de Ejecución:
```python
def ejecutar(self):
    """
    Método principal que ejecuta la simulación completa.
    
    Flujo:
    1. Procesar llegadas de procesos
    2. Manejar tiempos de bloqueo (TIP/TCP/TFP)
    3. Incrementar tiempo de espera de procesos en cola
    4. Seleccionar siguiente proceso si no hay uno ejecutándose
    5. Ejecutar proceso actual
    6. Procesar procesos bloqueados (I/O)
    7. Calcular CPU idle
    8. Avanzar tiempo
    """
```

#### Gestión de Procesos:
```python
def procesar_llegadas(self):
    """Agrega procesos que llegan en el tiempo actual a la cola de listos."""

def insertar_ordenado(self, proceso):
    """Inserta proceso en la cola manteniendo orden FCFS (por tiempo de llegada)."""

def seleccionar_siguiente_proceso(self):
    """Selecciona el primer proceso de la cola y aplica TIP o TCP según corresponda."""
```

#### Ejecución de Procesos:
```python
def ejecutar_proceso_actual(self):
    """
    Ejecuta una unidad de tiempo del proceso actual.
    
    Flujo:
    1. Decrementa duración de ráfaga de CPU
    2. Incrementa contadores de CPU de procesos
    3. Si termina la ráfaga:
       - Decrementa cantidad de ráfagas restantes
       - Si no quedan ráfagas: termina proceso
       - Si quedan ráfagas: bloquea proceso para I/O
    """
```

#### Gestión de Estados:
```python
def bloquear_proceso(self):
    """
    Bloquea el proceso actual para ejecutar I/O.
    
    Flujo:
    1. Guarda tiempo de bloqueo
    2. Restaura duración original de I/O
    3. Cambia estado a "bloqueado"
    4. Agrega a lista de procesos bloqueados
    5. Registra eventos de fin de ejecución y bloqueo
    6. Programa inicio de I/O para el siguiente tiempo
    7. Libera CPU (proceso_actual = None)
    """

def terminar_proceso(self):
    """
    Termina el proceso actual.
    
    Flujo:
    1. Registra evento de fin de ejecución
    2. Si hay TFP: aplica TFP y marca como "terminando"
    3. Si no hay TFP: calcula tiempo de retorno y marca como "terminado"
    4. Agrega a lista de procesos terminados
    5. Libera CPU
    """
```

#### Gestión de I/O:
```python
def procesar_procesos_bloqueados(self):
    """
    Procesa todos los procesos ejecutando I/O.
    
    Flujo:
    1. Para cada proceso bloqueado:
       - Decrementa duración de I/O
       - Si termina I/O: lo mueve a cola de listos
       - Restaura duración original de CPU
       - Registra evento de fin de I/O
    2. Remueve procesos que terminaron I/O de la lista bloqueados
    """
```

#### Aplicación de Tiempos del Sistema:
```python
def aplicar_tip(self):
    """Aplica TIP (Tiempo de Inicio de Proceso) para procesos nuevos."""

def aplicar_tcp(self):
    """Aplica TCP (Tiempo de Cambio de Proceso) para procesos que vuelven de I/O."""

def aplicar_tfp(self):
    """Aplica TFP (Tiempo de Finalización de Proceso) al terminar un proceso."""

def procesar_tiempo_bloqueo(self):
    """
    Procesa el tiempo restante de TIP/TCP/TFP.
    
    Retorna:
    - True: Si aún está bloqueado
    - False: Si terminó el bloqueo
    
    Al terminar:
    - Registra evento de fin correspondiente
    - Para TIP/TCP: proceso pasa a "ejecutando"
    - Para TFP: proceso termina completamente
    """
```

#### Utilidades:
```python
def hay_procesos_pendientes(self):
    """Verifica si aún hay trabajo por hacer en la simulación."""

def obtener_estadisticas_cpu(self):
    """
    Retorna estadísticas calculadas de CPU.
    
    Retorna diccionario con:
    - cpu_proc: Tiempo real de CPU ejecutando procesos
    - cpu_so: Tiempo real de CPU en labores del SO
    - cpu_idle: Tiempo real de CPU desocupada (calculado)
    - t_total: Tiempo total de la simulación
    - Información detallada por proceso
    """
```

### Flujo de Ejecución Detallado:

1. **Inicialización**: Se crean las colas vacías y se inicializan contadores
2. **Bucle Principal**: Mientras haya procesos pendientes:
   - **Llegadas**: Procesos que llegan en el tiempo actual se agregan a la cola
   - **Bloqueos del SO**: Se procesan TIP/TCP/TFP si están activos
   - **Tiempo de Espera**: Se incrementa el tiempo en cola de procesos listos
   - **Selección**: Si no hay proceso ejecutándose, se selecciona el primero de la cola
   - **Ejecución**: Se ejecuta una unidad de tiempo del proceso actual
   - **I/O**: Se procesan procesos bloqueados ejecutando I/O
   - **CPU Idle**: Se calcula si la CPU está desocupada
   - **Avance**: Se incrementa el tiempo

### Eventos Registrados:
- `llegada`: Proceso llega al sistema
- `inicio_tip`: Comienza TIP para proceso nuevo
- `fin_tip`: Termina TIP, proceso pasa a ejecutándose
- `inicio ejecucion`: Proceso comienza a ejecutarse
- `fin_ejecucion`: Proceso termina su ráfaga de CPU
- `bloqueo`: Proceso se bloquea para I/O
- `inicio_io`: Proceso comienza I/O
- `fin_io`: Proceso termina I/O, vuelve a cola
- `inicio_tcp`: Comienza TCP para proceso que vuelve
- `fin_tcp`: Termina TCP, proceso pasa a ejecutándose
- `inicio_tfp`: Comienza TFP al terminar proceso
- `fin_tfp`: Termina TFP, proceso termina completamente
- `terminacion`: Proceso termina definitivamente

---

## Algoritmo SPN

### Ubicación: `src/simulador/algoritmos/SPN.py`

El algoritmo SPN (Shortest Process Next) es un algoritmo no apropiativo que selecciona el proceso con menor duración de ráfaga de CPU para ejecutar a continuación.

### Características Específicas del SPN:

#### 1. **Criterio de Selección**:
- Selecciona el proceso con **menor duración de ráfaga de CPU**
- No es apropiativo: una vez que un proceso comienza a ejecutarse, continúa hasta completar su ráfaga

#### 2. **Lógica Especial del TCP**:
- **TCP se consume solo una vez** antes de ejecutar un proceso
- Si durante el TCP aparece un proceso con menor duración, este se ejecuta directamente sin consumir TCP adicional
- Implementado con la variable `tcp_ya_aplicado` para controlar este comportamiento

#### 3. **Ordenamiento de la Cola**:
- Los procesos se ordenan por duración de ráfaga de CPU (menor primero)
- Los procesos que vuelven de I/O se agregan al final pero se reordenan automáticamente

### Diferencias Clave con FCFS:

| Aspecto | FCFS | SPN |
|---------|------|-----|
| Criterio de selección | Orden de llegada | Menor duración de ráfaga |
| Ordenamiento de cola | Por tiempo de llegada | Por duración de ráfaga |
| TCP | Se consume siempre | Se consume solo una vez |
| Eficiencia | Baja (convoy effect) | Mejor para procesos cortos |

### Ejemplo de Funcionamiento:

Con los procesos:
- P1: llegada=0, duración_cpu=3
- P2: llegada=1, duración_cpu=2  
- P3: llegada=3, duración_cpu=5

**Secuencia de ejecución SPN**:
1. Tiempo 0: P1 llega → se ejecuta P1 (duración=3)
2. Tiempo 1: P2 llega → espera (P1 ya ejecutándose)
3. Tiempo 3: P3 llega → espera (P1 aún ejecutándose)
4. Tiempo 4: P1 termina → se selecciona P2 (menor duración=2)
5. Tiempo 6: P2 termina → se ejecuta P3 (duración=5)

### Integración en el Simulador:

El algoritmo SPN está completamente integrado:

```python
# En simulador.py
def ejecutar_spn(self, procesos_datos, tiempo_tip, tiempo_tcp, tiempo_tfp):
    # Conversión de datos
    self.procesos = self.crear_procesos_desde_datos(procesos_datos)
    
    # Creación del algoritmo SPN
    self.algoritmo_actual = SPN(self.procesos, tiempo_tip, tiempo_tcp, tiempo_tfp)
    
    # Ejecución y procesamiento de resultados
    self.algoritmo_actual.ejecutar()
    resultados = self._procesar_resultados_spn()
    
    return resultados
```

### Resultados de Prueba:

Con los datos de prueba (5 procesos), el algoritmo SPN produce:
- **Tiempo total**: 78 unidades
- **Tiempo medio de retorno**: 47.20
- **CPU por procesos**: 66 (84.6%)
- **CPU por SO**: 13 (16.7%)
- **CPU desocupada**: 0 (0.0%)

Esto demuestra que SPN es más eficiente que FCFS para procesos con diferentes duraciones de ráfaga.

---

## Algoritmo Round Robin (RR)

### Ubicación: `src/simulador/algoritmos/RR.py`

El algoritmo Round Robin es un algoritmo apropiativo que asigna un tiempo fijo (quantum) a cada proceso. Si un proceso no termina su ráfaga de CPU dentro del quantum, es preemptado y vuelve a la cola de listos.

### Características Específicas del Round Robin:

#### 1. **Criterio de Selección**:
- Selecciona procesos en orden de llegada (FCFS)
- **Apropiativo**: Los procesos pueden ser interrumpidos por agotamiento del quantum
- Usa una variable `quantum` para controlar el tiempo máximo de ejecución

#### 2. **Lógica de Preemption**:
- Cada proceso tiene un contador `quantum_restante`
- Cuando el quantum se agota, el proceso es preemptado
- El proceso preemptado vuelve a la cola de listos con su duración restante de ráfaga
- Se aplica TCP al cambiar de proceso

#### 3. **Gestión del Quantum**:
- Se reinicia el quantum cada vez que se selecciona un nuevo proceso
- El quantum se decrementa en cada unidad de tiempo de ejecución
- Si un proceso termina su ráfaga antes de agotar el quantum, no se preempta

### Diferencias Clave con FCFS y SPN:

| Aspecto | FCFS | SPN | Round Robin |
|---------|------|-----|-------------|
| Criterio de selección | Orden de llegada | Menor duración de ráfaga | Orden de llegada |
| Preemption | No | No | Sí (por quantum) |
| Quantum | No aplica | No aplica | Sí (configurable) |
| Eficiencia | Baja (convoy effect) | Buena para procesos cortos | Buena para procesos interactivos |

### Atributos Específicos:

#### Variables de Control:
```python
self.quantum = quantum                    # Tiempo de quantum configurado
self.quantum_restante = 0                 # Tiempo restante del quantum actual
```

#### Métodos Específicos:
```python
def verificar_preemption_quantum(self):
    """
    Verifica si el proceso actual debe ser preemptado por agotamiento del quantum.
    
    Returns:
        bool: True si debe ser preemptado, False en caso contrario
    """

def preemptar_proceso_actual(self):
    """
    Preempta el proceso actual y lo devuelve a la cola de listos.
    
    Flujo:
    1. Cambia estado del proceso actual a "listo"
    2. Lo inserta en la cola de listos (manteniendo orden FCFS)
    3. Registra eventos de preemption y fin de ejecución
    4. Limpia el proceso actual y reinicia el quantum
    """
```

### Flujo de Ejecución Detallado:

1. **Inicialización**: Se configura el quantum y se inicializan contadores
2. **Bucle Principal**: Mientras haya procesos pendientes:
   - **Llegadas**: Procesos que llegan se agregan a la cola en orden FCFS
   - **Bloqueos del SO**: Se procesan TIP/TCP/TFP si están activos
   - **Verificación de Preemption**: Se verifica si el quantum se agotó
   - **Preemption**: Si se agotó el quantum, se preempta el proceso actual
   - **Tiempo de Espera**: Se incrementa el tiempo en cola de procesos listos
   - **Selección**: Si no hay proceso ejecutándose, se selecciona el primero de la cola
   - **Ejecución**: Se ejecuta una unidad de tiempo del proceso actual
   - **I/O**: Se procesan procesos bloqueados ejecutando I/O
   - **CPU Idle**: Se calcula si la CPU está desocupada
   - **Avance**: Se incrementa el tiempo

### Eventos Específicos de Round Robin:

- `preemption_quantum`: Proceso es preemptado por agotamiento del quantum
- `fin_ejecucion`: Proceso termina su ejecución (por preemption o fin de ráfaga)
- `inicio ejecucion`: Proceso comienza a ejecutarse (después de TIP/TCP)

### Ejemplo de Funcionamiento:

Con los procesos:
- P1: llegada=0, duración_cpu=5, quantum=3
- P2: llegada=1, duración_cpu=3, quantum=3
- P3: llegada=2, duración_cpu=4, quantum=3

**Secuencia de ejecución Round Robin**:
1. Tiempo 0: P1 llega → se ejecuta P1 (quantum=3)
2. Tiempo 1: P2 llega → espera en cola
3. Tiempo 2: P3 llega → espera en cola
4. Tiempo 3: P1 preemptado (quantum agotado) → P2 ejecuta (quantum=3)
5. Tiempo 4: P2 termina ráfaga → P3 ejecuta (quantum=3)
6. Tiempo 6: P3 preemptado (quantum agotado) → P1 ejecuta (quantum=3)
7. Tiempo 7: P1 termina ráfaga → P3 ejecuta (quantum=3)

### Integración en el Simulador:

El algoritmo Round Robin está completamente integrado:

```python
# En simulador.py
def ejecutar_rr(self, procesos_datos, tiempo_tip, tiempo_tcp, tiempo_tfp, quantum):
    # Conversión de datos
    self.procesos = self.crear_procesos_desde_datos(procesos_datos)
    
    # Creación del algoritmo Round Robin
    self.algoritmo_actual = RR(self.procesos, tiempo_tip, tiempo_tcp, tiempo_tfp, quantum)
    
    # Ejecución y procesamiento de resultados
    self.algoritmo_actual.ejecutar()
    resultados = self._procesar_resultados_rr()
    
    return resultados
```

### Configuración del Quantum:

El quantum se configura a través de la interfaz de usuario:
- Se habilita el campo "Quantum" cuando se selecciona Round Robin
- El valor por defecto debe ser configurado por el usuario
- Se valida que el quantum sea un número entero positivo

### Ventajas del Round Robin:

1. **Equidad**: Todos los procesos reciben tiempo de CPU de manera equitativa
2. **Respuesta**: Los procesos interactivos reciben respuesta rápida
3. **Simplicidad**: Fácil de implementar y entender
4. **Prevención de inanición**: No hay procesos que esperen indefinidamente

### Desventajas del Round Robin:

1. **Overhead**: El cambio frecuente de contexto puede ser costoso
2. **Quantum crítico**: Si el quantum es muy pequeño, hay mucho overhead
3. **Quantum grande**: Si el quantum es muy grande, se comporta como FCFS

### Consideraciones de Implementación:

1. **Gestión del Quantum**: Se debe decrementar en cada unidad de tiempo de ejecución
2. **Preemption**: Se debe verificar en cada iteración del bucle principal
3. **Orden de Cola**: Se mantiene el orden FCFS para la cola de listos
4. **Eventos**: Se registran eventos específicos de preemption
5. **TCP**: Se aplica TCP en cada cambio de proceso por preemption

---

## Simulador Principal

### Ubicación: `src/simulador/simulador.py`

La clase `Simulador` actúa como el coordinador principal entre los algoritmos y la interfaz de usuario. Maneja la conversión de datos, ejecuta simulaciones y procesa resultados.

### Atributos:
- `algoritmo_actual`: Instancia del algoritmo actualmente ejecutándose
- `procesos`: Lista de procesos de la simulación actual
- `resultados`: Diccionario con resultados de la última simulación

### Métodos Principales:

#### Conversión de Datos:
```python
def crear_procesos_desde_datos(self, datos_json):
    """
    Convierte datos JSON de la UI en instancias de Proceso.
    
    Args:
        datos_json: Lista de diccionarios con datos desde la interfaz
        
    Returns:
        Lista de instancias de Proceso
        
    Mapeo de campos:
    - 'tiempo_arribo' -> tiempo_arrivo
    - 'cantidad_rafagas_cpu' -> cantidad_rafagas_cpu
    - 'duracion_rafaga_cpu' -> duracion_rafagas_cpu
    - 'duracion_rafaga_es' -> duracion_rafagas_io
    - 'prioridad_externa' -> prioridad
    """
```

#### Ejecución de Simulaciones:
```python
def ejecutar_fcfs(self, procesos_datos, tiempo_tip, tiempo_tcp, tiempo_tfp):
    """
    Ejecuta simulación con algoritmo FCFS.
    
    Args:
        procesos_datos: Datos de procesos desde la UI
        tiempo_tip: Tiempo de inicio de proceso
        tiempo_tcp: Tiempo de cambio de proceso
        tiempo_tfp: Tiempo de finalización de proceso
        
    Returns:
        Diccionario con resultados formateados para la UI
        
    Flujo:
    1. Convierte datos a instancias de Proceso
    2. Crea instancia del algoritmo FCFS
    3. Ejecuta la simulación
    4. Procesa resultados para la interfaz
    5. Genera PDF si es necesario
    """
```

#### Procesamiento de Resultados:
```python
def _procesar_resultados_fcfs(self):
    """
    Procesa resultados del algoritmo FCFS para la interfaz.
    
    Returns:
        Diccionario con:
        - procesos: Lista de datos de procesos terminados
        - tiempo_total: Tiempo total de la simulación
        - tiempo_medio_retorno: Promedio de tiempos de retorno
        - cpu_desocupada: Estadísticas de CPU desocupada
        - cpu_so: Estadísticas de CPU del sistema operativo
        - cpu_procesos: Estadísticas de CPU de procesos
        - gantt: Datos para diagrama de Gantt
        - eventos: Lista de todos los eventos
        - ruta_pdf: Ruta del PDF generado
    """
```

#### Generación de Diagrama de Gantt:
```python
def _procesar_datos_gantt(self):
    """
    Procesa eventos para crear datos del diagrama de Gantt.
    
    Returns:
        Diccionario con:
        - procesos: Lista de nombres de procesos
        - inicios: Lista de tiempos de inicio de ejecución
        - duraciones: Lista de duraciones de ejecución
        
    Lógica:
    1. Busca eventos de 'inicio_ejecucion'
    2. Busca eventos de 'terminacion' correspondientes
    3. Calcula duraciones como diferencia de tiempos
    """
```

#### Exportación de PDF:
```python
def exportar_pdf(self):
    """
    Exporta reporte PDF con resultados de la simulación.
    
    Returns:
        str: Ruta del archivo PDF generado, o None si hay error
        
    Flujo:
    1. Determina directorio de salida (desarrollo vs ejecutable)
    2. Genera nombre único con timestamp
    3. Prepara datos para el PDF
    4. Crea instancia de ExportadorPDF
    5. Genera el PDF
    6. Retorna ruta del archivo
    """
```

---

## Exportador PDF

### Ubicación: `src/simulador/exportador_pdf.py`

La clase `ExportadorPDF` genera reportes detallados en formato PDF usando la librería ReportLab.

### Atributos:
- `factor_escala`: Factor de escala para elementos del PDF
- `estilos`: Diccionario de estilos personalizados para el PDF

### Métodos Principales:

#### Configuración:
```python
def _configurar_estilos(self):
    """Configura estilos personalizados para el PDF."""
    # Estilos definidos:
    # - TituloPrincipal: Para títulos principales
    # - Subtitulo: Para subtítulos de sección
    # - TextoNormal: Para texto del cuerpo
    # - Codigo: Para texto de código
```

#### Exportación Principal:
```python
def exportar_simulacion(self, datos_simulacion, ruta_archivo=None):
    """
    Exporta resultados de simulación a PDF.
    
    Args:
        datos_simulacion: Diccionario con datos de la simulación
        ruta_archivo: Ruta donde guardar el PDF (opcional)
        
    Returns:
        str: Ruta del archivo generado
        
    Secciones del PDF:
    1. Portada con información general
    2. Tabla de eventos cronológica
    3. Estadísticas por proceso
    4. Diagrama de Gantt visual
    """
```

#### Creación de Secciones:
```python
def _crear_portada(self, datos):
    """Crea la portada del reporte con información general."""

def _crear_tabla_eventos(self, datos):
    """Crea tabla cronológica de todos los eventos de la simulación."""

def _crear_estadisticas_procesos(self, datos):
    """Crea tabla con estadísticas detalladas por proceso."""

def _crear_diagrama_gantt(self, datos):
    """Crea diagrama de Gantt visual de la simulación."""
```

#### Procesamiento de Diagrama de Gantt:
```python
def _procesar_eventos_gantt(self, eventos):
    """
    Procesa eventos para crear datos del diagrama de Gantt.
    
    Returns:
        Dict: Datos estructurados para el diagrama
        
    Lógica:
    1. Identifica todos los procesos y sus llegadas
    2. Procesa eventos de TIP/TCP/TFP
    3. Procesa eventos de ejecución e I/O
    4. Crea segmentos temporales para cada proceso
    """

def _construir_tabla_gantt(self, procesos_gantt, tiempo_total):
    """Construye tabla del diagrama dividida en segmentos de 30 unidades."""

def _determinar_contenido_celda_gantt(self, tiempo, datos_proceso):
    """
    Determina qué mostrar en cada celda del diagrama.
    
    Retorna códigos:
    - 'CPU': Ejecución de proceso
    - 'I/O': Operación de entrada/salida
    - 'TIP': Tiempo de inicio de proceso
    - 'TCP': Tiempo de cambio de proceso
    - 'TFP': Tiempo de finalización de proceso
    - 'F': Proceso terminado
    - 'llegada': Llegada del proceso
    """
```

---

## Conexión con la Interfaz de Usuario

### Flujo de Datos Completo:

#### 1. Carga de Datos:
```
Archivo JSON → CargadorArchivos → VentanaPrincipal.procesos_cargados
```

#### 2. Configuración:
```
SelectorPoliticas → VentanaPrincipal.politica_seleccionada
EntradaParametros → VentanaPrincipal.parametros_sistema
```

#### 3. Ejecución de Simulación:
```
VentanaPrincipal._simular() →
    Simulador.ejecutar_fcfs() →
        FCFS.ejecutar() →
            Simulador._procesar_resultados_fcfs() →
                ExportadorPDF.exportar_simulacion()
```

#### 4. Actualización de UI:
```
Simulador retorna resultados →
    VentanaPrincipal actualiza PestañaResultados →
        Muestra datos en tablas y gráficos
```

### Componentes de la UI:

#### VentanaPrincipal (`src/ui/main_window.py`):
- **Responsabilidad**: Coordinador principal de la interfaz
- **Métodos clave**:
  - `_simular()`: Ejecuta la simulación
  - `_ejecutar_simulacion_basica()`: Coordina la ejecución
  - `_verificar_estado_simulacion()`: Habilita/deshabilita botón de simulación

#### PestañaResultados (`src/ui/components/results_tab.py`):
- **Responsabilidad**: Mostrar resultados de la simulación
- **Métodos clave**:
  - `actualizar_resultados_procesos()`: Actualiza tabla de procesos
  - `actualizar_resultados_tanda()`: Actualiza estadísticas de la tanda
  - `actualizar_resultados_cpu()`: Actualiza estadísticas de CPU
  - `mostrar_notificacion_pdf()`: Muestra botón para abrir PDF

### Integración con el Simulador:

```python
# En VentanaPrincipal._ejecutar_simulacion_basica()
from ..simulador.simulador import Simulador

simulador = Simulador()

if politica == "FCFS":
    resultados = simulador.ejecutar_fcfs(
        self.procesos_cargados,
        parametros['tip'],
        parametros['tcp'],
        parametros['tfp']
    )
elif politica == "SPN":
    resultados = simulador.ejecutar_spn(
        self.procesos_cargados,
        parametros['tip'],
        parametros['tcp'],
        parametros['tfp']
    )
elif politica == "Round Robin":
    resultados = simulador.ejecutar_rr(
        self.procesos_cargados,
        parametros['tip'],
        parametros['tcp'],
        parametros['tfp'],
        parametros['quantum']
    )

# Actualizar interfaz con resultados
if resultados:
    self.pestaña_resultados.actualizar_resultados_procesos(resultados['procesos'])
    self.pestaña_resultados.actualizar_resultados_tanda(
        resultados['tiempo_total'], 
        resultados['tiempo_medio_retorno']
    )
    self.pestaña_resultados.actualizar_resultados_cpu(
        resultados['cpu_desocupada'],
        resultados['cpu_so'],
        resultados['cpu_procesos']
    )
```

---

## Implementación de Nuevos Algoritmos

### Estructura Requerida:

Para implementar un nuevo algoritmo, debes crear un archivo en `src/simulador/algoritmos/` siguiendo esta estructura:

```python
from ..proceso import Proceso

class TuAlgoritmo:
    def __init__(self, procesos, tiempo_tip, tiempo_tcp, tiempo_tfp):
        # Atributos básicos (igual que FCFS)
        self.procesos = procesos
        self.tiempo_actual = 0
        self.proceso_actual = None
        self.cola_listos = []
        self.procesos_bloqueados = []
        self.procesos_terminados = []
        self.resultados = []
        
        # Tiempos del sistema
        self.tiempo_tip = tiempo_tip
        self.tiempo_tcp = tiempo_tcp
        self.tiempo_tfp = tiempo_tfp
        
        # Controles específicos del algoritmo
        self.tiempo_restante_bloqueo = 0
        self.tipo_bloqueo = None
        
        # Contadores de CPU (obligatorios)
        self.cpu_proc = 0
        self.cpu_so = 0
        self.cpu_idle = 0
        
        # Tiempos de referencia (obligatorios)
        self.t_primer_arribo = None
        self.t_ultimo_tfp = None
        
        # Contadores por proceso (obligatorios)
        self.cpu_proc_por_proceso = {}
        self.t_arribo_por_proceso = {}
        self.t_fin_por_proceso = {}
        self.t_listo_por_proceso = {}
    
    def ejecutar(self):
        """Método principal - implementar lógica específica del algoritmo."""
        pass
    
    def obtener_estadisticas_cpu(self):
        """Método obligatorio - retorna estadísticas de CPU."""
        pass
```

### Métodos Obligatorios:

#### 1. `ejecutar(self)`:
- Debe implementar el bucle principal de simulación
- Debe manejar llegadas, selección de procesos, ejecución, I/O
- Debe registrar eventos en `self.resultados`
- Debe actualizar contadores de CPU

#### 2. `obtener_estadisticas_cpu(self)`:
- Debe retornar diccionario con estadísticas de CPU
- Debe calcular `t_total` correctamente
- Debe verificar que `cpu_idle` no sea negativo

### Métodos Opcionales (recomendados):

```python
def procesar_llegadas(self):
    """Procesa llegadas de procesos en el tiempo actual."""

def seleccionar_siguiente_proceso(self):
    """Selecciona el siguiente proceso según el algoritmo."""

def ejecutar_proceso_actual(self):
    """Ejecuta una unidad de tiempo del proceso actual."""

def procesar_procesos_bloqueados(self):
    """Procesa procesos ejecutando I/O."""

def aplicar_tip(self):
    """Aplica TIP para procesos nuevos."""

def aplicar_tcp(self):
    """Aplica TCP para procesos que vuelven de I/O."""

def aplicar_tfp(self):
    """Aplica TFP al terminar procesos."""
```

### Integración en el Simulador:

Para integrar tu algoritmo en el simulador principal:

#### 1. Agregar método en `Simulador`:
```python
def ejecutar_tu_algoritmo(self, procesos_datos, tiempo_tip, tiempo_tcp, tiempo_tfp):
    """Ejecuta simulación con tu algoritmo."""
    # Convertir datos a instancias de Proceso
    self.procesos = self.crear_procesos_desde_datos(procesos_datos)
    
    # Crear instancia del algoritmo
    self.algoritmo_actual = TuAlgoritmo(self.procesos, tiempo_tip, tiempo_tcp, tiempo_tfp)
    
    # Ejecutar simulación
    self.algoritmo_actual.ejecutar()
    
    # Procesar resultados
    resultados = self._procesar_resultados_tu_algoritmo()
    
    # Agregar ruta del PDF
    if 'ruta_pdf' not in resultados:
        resultados['ruta_pdf'] = None
    
    return resultados
```

#### 2. Crear método de procesamiento:
```python
def _procesar_resultados_tu_algoritmo(self):
    """Procesa resultados específicos de tu algoritmo."""
    # Implementar lógica similar a _procesar_resultados_fcfs()
    # pero adaptada a las características de tu algoritmo
```

#### 3. Integrar en la UI:
```python
# En VentanaPrincipal._ejecutar_simulacion_basica()
elif politica == "Tu Algoritmo":
    resultados = simulador.ejecutar_tu_algoritmo(
        self.procesos_cargados,
        parametros['tip'],
        parametros['tcp'],
        parametros['tfp']
    )
```

### Ejemplo: Algoritmo Round Robin (RR):

```python
class RR:
    def __init__(self, procesos, tiempo_tip, tiempo_tcp, tiempo_tfp, quantum):
        # ... inicialización igual que FCFS ...
        self.quantum = quantum
        self.quantum_restante = 0
    
    def ejecutar(self):
        tiempo_maximo = 1000
        iteraciones = 0
        
        while self.hay_procesos_pendientes() and iteraciones < tiempo_maximo:
            iteraciones += 1
            
            self.procesar_llegadas()
            
            if self.procesar_tiempo_bloqueo():
                self.procesar_procesos_bloqueados()
                self.tiempo_actual += 1
                continue
            
            # Verificar preemption por quantum
            if self.verificar_preemption_quantum():
                self.preemptar_proceso_actual()
            
            # Incrementar tiempo de espera
            for proceso in self.cola_listos:
                proceso.tiempo_en_listo += 1
                if proceso.nombre in self.t_listo_por_proceso:
                    self.t_listo_por_proceso[proceso.nombre] += 1
            
            if self.proceso_actual is None:
                self.seleccionar_siguiente_proceso()
            
            if self.proceso_actual is not None:
                self.ejecutar_proceso_actual()
            
            self.procesar_procesos_bloqueados()
            
            if (self.proceso_actual is None and 
                self.tiempo_restante_bloqueo == 0 and 
                len(self.cola_listos) == 0):
                self.cpu_idle += 1
            
            self.tiempo_actual += 1
    
    def verificar_preemption_quantum(self):
        """Verifica si el proceso actual debe ser preemptado por quantum."""
        if self.proceso_actual is None:
            return False
        return self.quantum_restante <= 0
    
    def preemptar_proceso_actual(self):
        """Preempta el proceso actual y lo devuelve a la cola."""
        if self.proceso_actual is None:
            return
        
        # Devolver a la cola de listos
        self.proceso_actual.estado = "listo"
        self.insertar_ordenado(self.proceso_actual)
        
        # Registrar eventos
        self.resultados.append({
            'tiempo': self.tiempo_actual,
            'proceso': self.proceso_actual.nombre,
            'evento': 'preemption_quantum',
            'estado': 'listo'
        })
        
        # Limpiar proceso actual
        self.proceso_actual = None
        self.quantum_restante = 0
    
    def seleccionar_siguiente_proceso(self):
        """Selecciona el primer proceso de la cola (FCFS)."""
        if len(self.cola_listos) > 0:
            self.proceso_actual = self.cola_listos.pop(0)
            
            if self.proceso_actual.proceso_nuevo:
                self.aplicar_tip()
                self.proceso_actual.proceso_nuevo = False
            else:
                self.aplicar_tcp()
            
            # Reiniciar quantum
            self.quantum_restante = self.quantum
    
    def ejecutar_proceso_actual(self):
        """Ejecuta una unidad de tiempo del proceso actual."""
        if self.proceso_actual is None:
            return
        
        # Ejecutar proceso
        self.proceso_actual.duracion_rafagas_cpu -= 1
        self.cpu_proc += 1
        self.cpu_proc_por_proceso[self.proceso_actual.nombre] += 1
        
        # Decrementar quantum
        self.quantum_restante -= 1
        
        # Verificar si termina la ráfaga
        if self.proceso_actual.duracion_rafagas_cpu == 0:
            self.proceso_actual.cantidad_rafagas_cpu -= 1
            
            if self.proceso_actual.cantidad_rafagas_cpu == 0:
                self.terminar_proceso()
            else:
                self.bloquear_proceso()
    
    def obtener_estadisticas_cpu(self):
        """Implementación igual que FCFS."""
        # ... misma lógica que FCFS ...
```

### Ejemplo: Algoritmo SPN (Shortest Process Next):

```python
class SPN:
    def __init__(self, procesos, tiempo_tip, tiempo_tcp, tiempo_tfp):
        # ... inicialización igual que FCFS ...
    
    def ejecutar(self):
        tiempo_maximo = 1000
        iteraciones = 0
        
        while self.hay_procesos_pendientes() and iteraciones < tiempo_maximo:
            iteraciones += 1
            
            self.procesar_llegadas()
            
            if self.procesar_tiempo_bloqueo():
                self.procesar_procesos_bloqueados()
                self.tiempo_actual += 1
                continue
            
            # Incrementar tiempo de espera
            for proceso in self.cola_listos:
                proceso.tiempo_en_listo += 1
                if proceso.nombre in self.t_listo_por_proceso:
                    self.t_listo_por_proceso[proceso.nombre] += 1
            
            if self.proceso_actual is None:
                self.seleccionar_siguiente_proceso()  # Diferente de FCFS
            
            if self.proceso_actual is not None:
                self.ejecutar_proceso_actual()
            
            self.procesar_procesos_bloqueados()
            
            if (self.proceso_actual is None and 
                self.tiempo_restante_bloqueo == 0 and 
                len(self.cola_listos) == 0):
                self.cpu_idle += 1
            
            self.tiempo_actual += 1
    
    def seleccionar_siguiente_proceso(self):
        """Selecciona el proceso con menor tiempo de servicio restante."""
        if len(self.cola_listos) > 0:
            # Ordenar por tiempo de servicio restante
            self.cola_listos.sort(key=lambda p: p.cantidad_rafagas_cpu * p.get_duracion_rafagas_cpu())
            
            self.proceso_actual = self.cola_listos.pop(0)
            
            if self.proceso_actual.proceso_nuevo:
                self.aplicar_tip()
                self.proceso_actual.proceso_nuevo = False
            else:
                self.aplicar_tcp()
    
    def obtener_estadisticas_cpu(self):
        """Implementación igual que FCFS."""
        # ... misma lógica que FCFS ...
```

### Consideraciones Importantes:

1. **Consistencia de Eventos**: Mantén los mismos nombres de eventos que FCFS para compatibilidad con la UI
2. **Contadores de CPU**: Siempre actualiza `cpu_proc`, `cpu_so` y calcula `cpu_idle` correctamente
3. **Tiempos de Referencia**: Mantén `t_primer_arribo` y `t_ultimo_tfp` para cálculos correctos
4. **Estados de Procesos**: Usa los mismos estados que FCFS ("nuevo", "listo", "ejecutando", "bloqueado", "terminado")
5. **Manejo de I/O**: La lógica de I/O debe ser igual en todos los algoritmos
6. **Tiempos del Sistema**: TIP, TCP y TFP deben manejarse igual en todos los algoritmos

### Testing:

Para probar tu algoritmo:

1. **Usar datos de prueba**: Carga archivos JSON con datos conocidos
2. **Verificar estadísticas**: Asegúrate que las sumas de CPU sean correctas
3. **Revisar eventos**: Verifica que los eventos estén en orden cronológico
4. **Comprobar diagrama de Gantt**: El PDF debe mostrar la ejecución correcta
5. **Validar tiempos**: Los tiempos de retorno deben ser consistentes

---

## Conclusión

Este simulador está diseñado para ser extensible y mantenible. La separación clara entre componentes permite:

- **Fácil implementación** de nuevos algoritmos
- **Reutilización** de código común
- **Mantenimiento** independiente de cada componente
- **Testing** modular de cada parte

Siguiendo esta guía, podrás implementar cualquier algoritmo de planificación de procesos y integrarlo completamente con la interfaz de usuario existente.








Ya tenemos implementado y funcional el algoritmo Round Robing(RR.py), pero tengo un caso borde: cuando la duración de la ráfaga de CPU es exactamente quantum + 1, se genera un conflicto en el orden de eventos. (Ejemplo: quantum 5, duracion rafaga cpu: 6; quantum 2, duracion rafaga: 3)

En el caso de quantum 5 y duracion de rafaga 6, el proceso debería ejecutarse 5 ticks, ser preemptado, luego en el próximo tick debería volver a ejecución y terminar su ráfaga (con los eventos correspondientes inicio_tcp,fin_tcp, inicio_ejecucion y fin_ejecucion).

Pero mi implementación, cuando un proceso cun duracion de rafaga 6 (y hay un quantum 5), ejecuta correctamente los primeros 5 ticks y es premtiado, hasta aca funciona perfecto, el issue esta cuando quiero ejecutar su tick restante que le quedo (le queda 1 tick ya que duracion de rafaga 6 - quantum 5 = 1 tick restante), cuando pasa esta situacion especifica se ejecutan solo los eventos "inicio_tcp" y "fin_ejecucion", pero los eventos "inicio_ejecucion" y "fin_tcp" no aparecen. Lo que deberia pasar es lo siguiente: en el caso de que el proceso p tenga que ejecutar su tick restante y llega en el tiempo 42 deberia ejecutar inicio_tcp en tiempo 42, fin_tcp en tiempo 43, inicio_ejecucion en tiempo 43 y fin_ejecucion en tiempo 43 (ya que es un solo tick que le queda restante). Pero actualmente lo que esta pasando es que ejecuta inicio_tcp en tiempo 42 y fin_ejecucion en tiempo 42, por lo que el algoritmo da mal los resultados por este issue especifico.

Como te dije anteriormente el issue es demasiado especifico a quantum = duracion de rafaga cpu del proceso + 1, ya que con otro tipo de quantum el algoritmo funciona perfectamente, o con otra duracion de proceso tambien funciona perfecto, por lo cual la solucion debe ser especifica a este problema, no debes modificar el resto de cosas ya que puedes romper el funcionamiento del algoritmo que ya funciona bien.

Haz un debug muy pero muy detallado, para ver el flujo de por que los eventos correspondientes no se estan ejecutando (fin_tcp y fin_ejecucion), con el siguiente conjunto de procesos, con tip: 1, tcp: 1, tfp: 1 y quantum: 5 : 

{
    "nombre": "P1",
    "tiempo_arribo": 0,
    "cantidad_rafagas_cpu": 4,
    "duracion_rafaga_cpu": 3,
    "duracion_rafaga_es": 2,
    "prioridad_externa": 3
  },
  {
    "nombre": "P2",
    "tiempo_arribo": 1,
    "cantidad_rafagas_cpu": 2,
    "duracion_rafaga_cpu": 8,
    "duracion_rafaga_es": 5,
    "prioridad_externa": 1
  },
  {
    "nombre": "P3",
    "tiempo_arribo": 3,
    "cantidad_rafagas_cpu": 5,
    "duracion_rafaga_cpu": 2,
    "duracion_rafaga_es": 1,
    "prioridad_externa": 4
  },
  {
    "nombre": "P4",
    "tiempo_arribo": 6,
    "cantidad_rafagas_cpu": 3,
    "duracion_rafaga_cpu": 6,
    "duracion_rafaga_es": 4,
    "prioridad_externa": 2
  },
  {
    "nombre": "P5",
    "tiempo_arribo": 10,
    "cantidad_rafagas_cpu": 1,
    "duracion_rafaga_cpu": 10,
    "duracion_rafaga_es": 0,
    "prioridad_externa": 5
  }

Para que sepas que el algoritmo funciona bien, los procesos deberian terminar en los siguientes tiempos (tfp): P1: tiempo 64(tiempo retorno de 64), P2: tiempo 75(tiempo retorno de 74), P3: tiempo 84(tiempo retorno de 81), p4: tiempo 93(tiempo retorno 87), p5: tiempo 56(tiempo retorno 46)

la forma de ejecutar es con "poetry run python archivo.py"
