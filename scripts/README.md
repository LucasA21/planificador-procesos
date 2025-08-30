# Scripts de Build

Esta carpeta contiene todos los scripts necesarios para generar ejecutables del proyecto.

## Scripts Disponibles

### 🐧 Linux/macOS: `build.sh`
```bash
# Desde la raíz del proyecto
./scripts/build.sh

# O navegando a la carpeta
cd scripts
./build.sh
```

### 🪟 Windows: `build_windows.bat`
```cmd
# Desde la raíz del proyecto
scripts\build_windows.bat

# O navegando a la carpeta
cd scripts
build_windows.bat
```

## Archivos de Configuración

### `simulador.spec`
Archivo de configuración de PyInstaller que define:
- Módulos a incluir
- Archivos de datos
- Configuración del ejecutable
- Nombre y opciones del build

**Ubicación**: En la raíz del proyecto (`simulador.spec`)

## Cómo Usar

### 1. Preparación
```bash
# Instalar dependencias
poetry install

# Verificar que PyInstaller esté disponible
poetry run pyinstaller --version
```

### 2. Generar Ejecutable
```bash
# Linux/macOS
./scripts/build.sh

# Windows
scripts\build_windows.bat
```

### 3. Resultado
Los ejecutables se generarán en:
- **Linux**: `dist/linux/Simulador_Planificacion`
- **Windows**: `dist/windows/Simulador_Planificacion.exe`

## Estructura del Proyecto

```
planificador-procesos/
├── scripts/              # Scripts de build (esta carpeta)
│   ├── build.sh         # Script para Linux
│   ├── build_windows.bat # Script para Windows
│   └── README.md        # Este archivo
├── simulador.spec        # Configuración de PyInstaller
├── build/                # Carpeta temporal (se borra automáticamente)
└── dist/                 # Ejecutables generados
```

## Personalización

### Modificar el Build
Para cambiar la configuración del build, edita `simulador.spec` en la raíz:
- Cambiar nombre del ejecutable
- Agregar/remover módulos
- Modificar opciones de PyInstaller

### Agregar Nuevas Plataformas
1. Crear nuevo script en `scripts/`
2. Crear nuevo archivo `.spec` si es necesario
3. Actualizar este README

## Troubleshooting

### Error: "No module named 'src'"
- Verificar que `simulador.spec` incluya todos los directorios de `src/`
- Revisar que las rutas en `datas` sean correctas

### Error: "PyInstaller not found"
- Ejecutar `poetry install` para instalar dependencias
- Verificar que estés en el entorno virtual de Poetry

### Error: "Permission denied"
- Dar permisos de ejecución: `chmod +x scripts/build.sh`
- En Windows, ejecutar como administrador si es necesario

## Notas Importantes

- **La carpeta `build/` se borra automáticamente** en cada build
- **Los scripts están preservados** en Git para uso futuro
- **El archivo `.spec` está en la raíz** para evitar problemas de rutas
