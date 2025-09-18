# Simulador de Planificación de Procesos

Este proyecto implementa un simulador de estrategias de planificación del procesador para un sistema multiprogramado y monoprocesador. Permite comparar diferentes algoritmos de planificación y analizar su rendimiento.


## Algoritmos Implementados

1. **FCFS** (First Come, First Served) - Por orden de llegada
2. **Round Robin** - Con quantum configurable
3. **SPN** (Shortest Process Next) - Por duración más corta
4. **SRTN** (Shortest Remaining Time Next) - Por tiempo restante más corto
5. **Prioridad Externa** - Por prioridad asignada externamente

## Estructura del Proyecto

```
planificador-procesos/
├── src/
│   ├── simulador/
│   │   ├── simulador.py          # Motor principal de simulación
│   │   ├── proceso.py            # Clase Proceso con estados y métricas
│   │   ├── exportador_pdf.py     # Generación de reportes PDF
│   │   └── algoritmos/           # Implementación de algoritmos
│   │       ├── FCFS.py          
│   │       ├── RR.py            
│   │       ├── SPN.py           
│   │       ├── SRTN.py          
│   │       └── PE.py            
│   ├── ui/
│       ├── main_window.py       # Main UI
│       └── components/          # Componentes UI
│           ├── file_loader.py   
│           ├── policy_selector.py 
│           ├── parameter_input.py 
│           ├── results_tab.py   
│           └── stats_tab.py     
│   
├── data/
│   ├── input/                   # Archivos de entrada procesos (JSON)
│   │   └── procesos_tanda_5p.json
│   └── output/                  # Reportes PDF generados
├── scripts/
│   ├── build.sh                 # Script de build para Linux/macOS
│   ├── build_windows.bat        # Script de build para Windows
│   └── README.md               
├── docs/                        # Diagramas Gantt
│   ├── diagramas/                        
│   └── README.md               
├── dist/                        # Ejecutables compilados  
├── ejecutables/                 # Ejecutables precompilados
├── simulador.spec             
├── pyproject.toml             
└── main.py                     
```

## Ejecutables Precompilados

La carpeta `ejecutables` contiene ejecutables listos para usar:

- **Linux:** `ejecutables/Simulador_Planificacion`
- **Windows:** `ejecutables/windows/Simulador_Planificacion.exe`

Para usar la aplicacion: 
1. En **"Seleccionar Archivo"** se elige el conjunto de procesos en formato JSON.
2. Ingresar los valores de **TIP, TCP y TFP** correspondientes en los campos de entrada.
3. En el caso de Round Robin tambien ingresar el **Quantum**.
4. Presionar el boton de **"Ejecutar Simulacion"**
5. Una vez ejecutado se van a mostrar los resultados correspondientes.
6. Tambien se va a generar un **PDF** con los eventos de cada tick de tiempo y un diagrama de Gantt para mayor entendimiento. (`Para abrir el pdf esta el boton abajo de los resultados, en caso de que no se abra este pdf se guarda en una carpeta /Output que se genera en la misma ruta donde se ejecuto el programa`)

## Desarrollo

### Requisitos Previos

- Python 3.8 o superior
- Poetry (gestor de dependencias)

### Instalación

1. **Instalar Poetry:**
```bash
pipx install poetry
```

2. **Instalar dependencias:**
```bash
poetry install
```

3. **Ejecutar la aplicación:**
```bash
poetry run python main.py
```

## Compilación de Ejecutables

### Linux/macOS

Ejecutar el script de build:
```bash
./scripts/build.sh
```

El ejecutable se genera en: `dist/linux/Simulador_Planificacion`

### Windows

Ejecutar el script de build:
```bash
scripts\build_windows.bat
```

El ejecutable se genera en: `dist\windows\Simulador_Planificacion.exe`

## Formato de Archivos de Entrada

Los archivos de procesos deben estar en formato JSON con la siguiente estructura:

```json
{
  "procesos": [
    {
      "nombre": "A",
      "tiempo_llegada": 0,
      "tiempo_cpu": 3,
      "prioridad": 1
    },
    {
      "nombre": "B",
      "tiempo_llegada": 1,
      "tiempo_cpu": 5,
      "prioridad": 2
    }
  ]
}
```

### Campos Requeridos

- **nombre**: Identificador único del proceso
- **tiempo_llegada**: Momento en que el proceso llega al sistema
- **tiempo_cpu**: Tiempo total de CPU requerido por el proceso
- **prioridad**: Prioridad del proceso (solo para algoritmo de Prioridad Externa)

## Parámetros del Sistema

- **TIP** (Tiempo de Ingreso de Proceso): Tiempo que toma ingresar un proceso al sistema
- **TFP** (Tiempo de Finalización de Proceso): Tiempo que toma finalizar un proceso
- **TCP** (Tiempo de Conmutación de Proceso): Tiempo de cambio de contexto entre procesos
- **Quantum**: Tiempo asignado a cada proceso en Round Robin

## Métricas Calculadas

El simulador calcula y muestra las siguientes métricas:

- **Tiempo de Retorno**: Tiempo total desde llegada hasta finalización
- **Tiempo de Retorno Normalizado**: Tiempo de retorno dividido por tiempo de servicio
- **Tiempo Medio de Retorno**: Promedio de tiempos de retorno de todos los procesos
- **Utilización de CPU**: Porcentaje de tiempo que la CPU estuvo ocupada
- **Tiempo en Estado Listo**: Tiempo que cada proceso esperó en la cola de listos

## Reportes PDF

La aplicación genera automáticamente reportes PDF que incluyen:

- Tabla detallada de resultados por proceso
- Estadísticas de rendimiento del sistema
- Métricas de utilización de CPU
- Información de la configuración utilizada

Los reportes se guardan en la carpeta `data/output/` con timestamp automático.

## Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **CustomTkinter**: Interfaz gráfica moderna
- **ReportLab**: Generación de reportes PDF
- **Poetry**: Gestión de dependencias
- **PyInstaller**: Compilación de ejecutables