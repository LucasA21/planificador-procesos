# Documentación de la Interfaz

## Descripción General

Esta interfaz está construida usando CustomTkinter, una biblioteca moderna que extiende Tkinter.

## Arquitectura de la Interfaz

### Estructura de Componentes

```
VentanaPrincipal (main_window.py)
├── Panel Izquierdo (Sidebar de Configuración)
│   ├── Header con Botón de Simulación
│   ├── CargadorArchivos
│   ├── SelectorPoliticas
│   └── EntradaParametros
└── Panel Derecho (Área Principal)
    ├── Sistema de Pestañas
    │   ├── PestañaResultados
    │   ├── PestañaGantt
    │   └── PestañaEstadisticas
    └── Navegación entre Pestañas
```

### Componentes Principales

#### 1. CargadorArchivos (file_loader.py)
- **Función**: Carga y valida archivos de procesos desde archivos de texto
- **Características**:
  - Botón de selección de archivo
  - Indicador visual del estado de carga
  - Validación automática del formato
  - Callback cuando se carga un archivo
- **Métodos principales**:
  - `obtener_procesos()`: Retorna los procesos cargados
  - `establecer_callback(callback)`: Configura callback cuando se carga un archivo

#### 2. SelectorPoliticas (policy_selector.py)
- **Función**: Permite seleccionar el algoritmo de planificación
- **Políticas disponibles**:
  - FCFS (First Come, First Served)
  - Prioridad Externa
  - Round Robin
  - SPN (Shortest Process Next)
  - SRTN (Shortest Remaining Time Next)
- **Métodos principales**:
  - `obtener_politica_seleccionada()`: Retorna la política seleccionada
  - `establecer_callback(callback)`: Configura callback cuando cambia la política

#### 3. EntradaParametros (parameter_input.py)
- **Función**: Entrada de parámetros del sistema con validación en tiempo real
- **Parámetros**:
  - **TIP**: Tiempo de Ingreso de Proceso
  - **TFP**: Tiempo de Finalización de Proceso
  - **TCP**: Tiempo de Conmutación de Proceso
  - **Quantum**: Solo para Round Robin
- **Características**:
  - Validación automática de valores
  - Indicadores visuales de estado
  - Habilitación/deshabilitación condicional del quantum
- **Métodos principales**:
  - `obtener_todos_parametros()`: Retorna todos los parámetros
  - `habilitar_quantum(habilitar)`: Habilita/deshabilita campo quantum
  - `validar_parametros()`: Valida que los parámetros sean correctos

#### 4. PestañaResultados (results_tab.py)
- **Función**: Muestra el log de eventos de la simulación con formato enriquecido
- **Características**:
  - Área de texto con scroll
  - Formato automático para diferentes tipos de contenido
  - Tags de color para timestamps, títulos y separadores
- **Métodos principales**:
  - `agregar_resultado(texto)`: Agrega texto a los resultados
  - `limpiar_resultados()`: Limpia todos los resultados
  - `configurar_tags()`: Configura el formato de texto

#### 5. PestañaGantt (gantt_tab.py)
- **Función**: Muestra diagrama de Gantt de la simulación usando matplotlib
- **Características**:
  - Gráfico interactivo con matplotlib
  - Colores del tema para los procesos
  - Grid y ejes personalizados
  - Soporte para múltiples procesos
- **Métodos principales**:
  - `actualizar_gantt(procesos, inicios, duraciones)`: Actualiza con datos reales
  - `limpiar_gantt()`: Limpia el diagrama
  - `mostrar_gantt_ejemplo()`: Muestra un ejemplo de diagrama

#### 6. PestañaEstadisticas (stats_tab.py)
- **Función**: Muestra métricas y estadísticas de la simulación
- **Secciones**:
  - Estadísticas por proceso
  - Estadísticas de la tanda
  - Uso de CPU
- **Métodos principales**:
  - `actualizar_estadisticas_proceso(texto)`: Actualiza estadísticas por proceso
  - `actualizar_estadisticas_tanda(tr, tmr)`: Actualiza estadísticas de la tanda
  - `actualizar_estadisticas_cpu(desocupada, so, procesos)`: Actualiza uso de CPU

## Sistema de Colores Unificado

La interfaz utiliza un sistema de colores completamente unificado definido en `theme.py`:

### Uso en Componentes

Todos los componentes reciben los colores del tema y los aplican consistentemente:

```python
# En cualquier componente
self.colores = colores or {}
self.configure(
    fg_color=self.colores["bg_card"],
    border_color=self.colores["border"],
    text_color=self.colores["text_primary"]
)
```

## Sistema de Escalado Automático

### Escalado por Resolución

La interfaz se adapta automáticamente a diferentes resoluciones de pantalla:

- **4K (3840+)**: Factor de escala 2.0x
- **2K/QHD (2560+)**: Factor de escala 1.8x
- **Full HD (1920+)**: Factor de escala 1.2x
- **HD o menor**: Factor de escala 1.0x


## Cómo Funciona CustomTkinter

### Conceptos Básicos

1. **Widgets**: CustomTkinter proporciona widgets modernos como `CTkFrame`, `CTkButton`, `CTkLabel`, etc.
2. **Layout**: Usa el sistema de grid de Tkinter para organizar widgets
3. **Temas**: Soporta temas claro/oscuro y colores personalizables
4. **Eventos**: Los widgets pueden tener callbacks para responder a acciones del usuario

### Ejemplo de Widget Básico

```python
import customtkinter as ctk

# Crear un botón
boton = ctk.CTkButton(
    parent,                    # Widget padre
    text="Texto del botón",    # Texto visible
    command=mi_funcion,        # Función a ejecutar al hacer clic
    height=35,                 # Altura del botón
    fg_color=self.colores["accent"]  # Color del tema
)

# Posicionar en el grid
boton.grid(row=0, column=0, pady=10, padx=15, sticky="ew")
```

### Sistema de Grid

```python
# Configurar columnas y filas para que se expandan
parent.grid_columnconfigure(0, weight=1)  # Columna 0 se expande
parent.grid_rowconfigure(1, weight=1)     # Fila 1 se expande

# Posicionar widget
widget.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
```

## Cómo Conectar tu Lógica de Simulación

### 1. Modificar el Método de Simulación

En `main_window.py`, encuentra el método `_ejecutar_simulacion_basica` y reemplázalo con tu lógica:

```python
def _ejecutar_simulacion_basica(self, politica, parametros):
    # Aquí va tu lógica de simulación
    resultados = tu_simulador.ejecutar(politica, parametros, self.procesos_cargados)
    
    # Mostrar resultados en la interfaz
    self.pestaña_resultados.limpiar_resultados()
    for evento in resultados['eventos']:
        self.pestaña_resultados.agregar_resultado(evento)
    
    # Actualizar diagrama de Gantt
    self.pestaña_gantt.actualizar_gantt(
        resultados['procesos'],
        resultados['inicios'],
        resultados['duraciones']
    )
    
    # Actualizar estadísticas
    self.pestaña_estadisticas.actualizar_estadisticas_tanda(
        resultados['tiempo_retorno'],
        resultados['tiempo_medio_retorno']
    )
```

### 2. Crear tu Simulador

Crea una clase simulador en `src/simulador/`:

```python
class Simulador:
    def __init__(self):
        self.tiempo_actual = 0
        self.eventos = []
    
    def ejecutar(self, politica, parametros, procesos):
        # Tu lógica de simulación aquí
        # Retorna diccionario con resultados
        return {
            'eventos': self.eventos,
            'procesos': [p['nombre'] for p in procesos],
            'inicios': [0, 5, 8],
            'duraciones': [5, 3, 2],
            'tiempo_retorno': 15,
            'tiempo_medio_retorno': 7.5
        }
```

### 3. Integrar con la Interfaz

Importa tu simulador en `main_window.py`:

```python
from ..simulador.simulador import Simulador

class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        # ... código existente ...
        self.simulador = Simulador()
```

## Agregar Nuevos Componentes

1. Crea un nuevo archivo en `src/ui/components/`
2. Hereda de `ctk.CTkFrame`
3. Implementa los métodos necesarios
4. Agrégalo a la ventana principal en `_crear_componentes()`

## Flujo de Trabajo de la Interfaz

### 1. Carga de Archivos
- Usuario selecciona archivo de procesos
- Se valida el formato del archivo
- Se cargan los procesos en memoria
- Se habilita el botón de simulación

### 2. Configuración
- Usuario selecciona política de planificación
- Se configuran parámetros del sistema
- Se valida que todos los parámetros sean correctos
- Se habilita la simulación

### 3. Ejecución
- Se ejecuta la simulación con los parámetros configurados
- Se muestran resultados en la pestaña correspondiente
- Se actualiza el diagrama de Gantt
- Se muestran estadísticas del sistema

### 4. Visualización
- Usuario puede navegar entre pestañas
- Cada pestaña muestra información específica
- Los datos se mantienen hasta la próxima simulación

## Estructura de Datos Esperada

### Procesos
```python
proceso = {
    'nombre': 'P1',
    'tiempo_arribo': 0,
    'rafagas_cpu': 3,
    'duracion_rafaga_cpu': 5,
    'duracion_rafaga_io': 2,
    'prioridad': 50
}
```

### Parámetros del Sistema
```python
parametros = {
    'tip': 1,      # Tiempo de ingreso de proceso
    'tfp': 1,      # Tiempo de finalización de proceso
    'tcp': 1,      # Tiempo de conmutación de proceso
    'quantum': 2   # Quantum para Round Robin
}
```

### Resultados de Simulación
```python
resultados = {
    'eventos': ['[0] Arriba proceso P1', '...'],
    'procesos': ['P1', 'P2', 'P3'],
    'inicios': [0, 5, 8],
    'duraciones': [5, 3, 2],
    'tiempo_retorno': 15,
    'tiempo_medio_retorno': 7.5
}
```

