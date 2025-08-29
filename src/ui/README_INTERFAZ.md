# Documentación de la Interfaz - Simulador de Planificación de Procesos

## Descripción General

Esta interfaz está construida usando CustomTkinter, una biblioteca moderna que extiende Tkinter con widgets más atractivos y funcionales. La interfaz está diseñada de manera modular para facilitar el mantenimiento y la extensión.

## Arquitectura de la Interfaz

### Estructura de Componentes

```
VentanaPrincipal (main_window.py)
├── Panel Izquierdo (Configuración)
│   ├── CargadorArchivos
│   ├── SelectorPoliticas
│   ├── EntradaParametros
│   └── ControlesSimulacion
└── Panel Derecho (Resultados)
    ├── PestañaResultados
    ├── PestañaGantt
    └── PestañaEstadisticas
```

### Componentes Principales

#### 1. CargadorArchivos (file_loader.py)
- **Función**: Carga y valida archivos de procesos
- **Métodos principales**:
  - `obtener_procesos()`: Retorna los procesos cargados
  - `establecer_callback(callback)`: Configura callback cuando se carga un archivo

#### 2. SelectorPoliticas (policy_selector.py)
- **Función**: Permite seleccionar el algoritmo de planificación
- **Métodos principales**:
  - `obtener_politica_seleccionada()`: Retorna la política seleccionada
  - `establecer_callback(callback)`: Configura callback cuando cambia la política

#### 3. EntradaParametros (parameter_input.py)
- **Función**: Entrada de parámetros del sistema (TIP, TFP, TCP, Quantum)
- **Métodos principales**:
  - `obtener_todos_parametros()`: Retorna todos los parámetros
  - `habilitar_quantum(habilitar)`: Habilita/deshabilita campo quantum
  - `validar_parametros()`: Valida que los parámetros sean correctos

#### 4. ControlesSimulacion (simulation_controls.py)
- **Función**: Botones para ejecutar simulación y limpiar resultados
- **Métodos principales**:
  - `habilitar_simulacion(habilitar)`: Habilita/deshabilita botón de simulación
  - `establecer_callback_simulacion(callback)`: Configura callback para simulación
  - `establecer_callback_limpiar(callback)`: Configura callback para limpiar

#### 5. PestañaResultados (results_tab.py)
- **Función**: Muestra el log de eventos de la simulación
- **Métodos principales**:
  - `agregar_resultado(texto)`: Agrega texto a los resultados
  - `limpiar_resultados()`: Limpia todos los resultados
  - `establecer_resultados(texto)`: Establece contenido completo

#### 6. PestañaGantt (gantt_tab.py)
- **Función**: Muestra diagrama de Gantt de la simulación
- **Métodos principales**:
  - `actualizar_gantt(procesos, inicios, duraciones)`: Actualiza con datos reales
  - `limpiar_gantt()`: Limpia el diagrama

#### 7. PestañaEstadisticas (stats_tab.py)
- **Función**: Muestra métricas y estadísticas de la simulación
- **Métodos principales**:
  - `actualizar_estadisticas_proceso(texto)`: Actualiza estadísticas por proceso
  - `actualizar_estadisticas_tanda(tr, tmr)`: Actualiza estadísticas de la tanda
  - `actualizar_estadisticas_cpu(desocupada, so, procesos)`: Actualiza uso de CPU

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
    fg_color="blue"            # Color de fondo
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

Crea una clase simulador en `src/core/simulador.py`:

```python
class Simulador:
    def __init__(self):
        self.tiempo_actual = 0
        self.eventos = []
    
    def ejecutar(self, politica, parametros, procesos):
        # Tu lógica de simulación aquí
        pass
```

### 3. Integrar con la Interfaz

Importa tu simulador en `main_window.py`:

```python
from ..core.simulador import Simulador

class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        # ... código existente ...
        self.simulador = Simulador()
```

## Personalización de la Interfaz

### Cambiar Colores

```python
# En el constructor de cualquier componente
self.configure(fg_color="darkblue")  # Color de fondo
self.configure(border_color="lightblue")  # Color del borde

# Para botones
boton.configure(fg_color="green", hover_color="darkgreen")
```

### Cambiar Tamaños

```python
# Configurar tamaño de la ventana principal
self.geometry("1600x1000")  # Ancho x Alto
self.minsize(1400, 900)     # Tamaño mínimo
```

### Agregar Nuevos Componentes

1. Crea un nuevo archivo en `src/ui/components/`
2. Hereda de `ctk.CTkFrame`
3. Implementa los métodos necesarios
4. Agrégalo a la ventana principal

## Consejos para el Desarrollo

1. **Mantén la modularidad**: Cada componente debe tener una responsabilidad específica
2. **Usa callbacks**: Los componentes se comunican a través de callbacks, no referencias directas
3. **Valida entradas**: Siempre valida los datos de entrada antes de procesarlos
4. **Maneja errores**: Usa try/except para manejar errores de archivos y datos
5. **Documenta métodos**: Cada método público debe tener docstring explicando su función

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
