# Simulador de Planificación de Procesos

Este proyecto implementa un simulador de estrategias de planificación del procesador para un sistema multiprogramado y monoprocesador. Permite comparar diferentes algoritmos de planificación y analizar su rendimiento.

## Estructura del Proyecto

```
planificador-procesos/
├── src/                 
│   ├── simulador/              
│   │   ├── proceso.py        # Clase Proceso
│   │   ├── pcb.py            # Process Control Block
│   │   ├── estado_proceso.py # Tipos de estados (ENUM)
│   │   ├── evento.py         # Evento
│   │   ├── cola.py           # Cola de procesos listos
│   │   ├── algoritmos/       # Algoritmos de planificacion
│   │   └── planificador.py   # Planificador de procesos
│   ├── ui/                
│   │   ├── components/    # Componentes UI 
│   │   ├── main_window.py # Ventana principal
│   │   ├── theme.py       # Configuracion de colores
│   │   └── README.md                 
├── data/                 
│   ├── input/   # Archivos de procesos (JSON)
│   └── output/  # Resultados de simulación 
├── main.py                 
└── README.md               
```


## Ejecutable

La carpeta `execute` contiene dos archivos ejecutables, ya funcionales:

- **Linux:** `execute/linux/Simulador_Planificacion`
- **Windows:** `execute/windows/Simulador_Planificacion.exe`

## Levantar Desarrollo

- Instalar **Poetry**:
```bash 
pipx install poetry
```
- Instalar dependencias:
```bash
poetry install
```
- Correr proyecto:
```bash 
poetry run python main.py
```

## Build

### Linux/macOS
Ejecutar script de build
```bash
./scripts/build.sh 
```
El build se va a guardar en la carpeta `./dist/linux/Simulador_Planificacion`

### Windows
Ejecutar script de build
```bash
scripts\build_windows.bat 
```

El build se va a guardar en la carpeta `dist\windows\Simulador_Planificacion.exe`


