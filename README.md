# Simulador de Planificación de Procesos

Este proyecto implementa un simulador de estrategias de planificación del procesador para un sistema multiprogramado y monoprocesador. Permite comparar diferentes algoritmos de planificación y analizar su rendimiento.

## Estructura del Proyecto

```
planificador-procesos/
├── src/                 
│   ├── simulador/              
│   │   ├── proceso.py     # Clase Proceso
│   │   ├── planificador.py # Clase base Planificador
│   │   └── algoritmos/    # Implementaciones de algoritmos
│   ├── ui/                
│   │   ├── components/    # Componentes 
│   │   ├── main_window.py # Ventana principal
│   │   └── interfaz.py    # Clase principal de la UI
│   ├── data/              
│   │   ├── parser.py      # Lectura de archivos
│   │   └── export.py      # Exportación de resultados
│   └── utils/             
├── data/                 
│   ├── input/             # Archivos de procesos
│   └── output/            # Resultados de simulación
├── main.py                 
└── README.md               
```
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


