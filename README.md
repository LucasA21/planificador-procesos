# Simulador de Planificación de Procesos

## Descripción del Proyecto

Este proyecto implementa un simulador de estrategias de planificación del procesador para un sistema multiprogramado y monoprocesador. Permite comparar diferentes algoritmos de planificación y analizar su rendimiento.

## Estructura del Proyecto

```
planificador-procesos/
├── src/                    # Código fuente principal
│   ├── simulador/              # Lógica del simulador
│   │   ├── proceso.py     # Clase Proceso
│   │   ├── planificador.py # Clase base Planificador
│   │   └── algoritmos/    # Implementaciones de algoritmos
│   ├── ui/                # Interfaz gráfica
│   │   ├── components/    # Componentes reutilizables
│   │   ├── main_window.py # Ventana principal
│   │   └── interfaz.py    # Clase principal de la UI
│   ├── data/              # Gestión de datos
│   │   ├── parser.py      # Lectura de archivos
│   │   └── export.py      # Exportación de resultados
│   └── utils/             
├── data/                   # Datos de entrada y salida
│   ├── input/             # Archivos de procesos
│   └── output/            # Resultados de simulación
├── main.py                 
└── README.md               
```

