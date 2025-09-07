# Scripts de Build

Esta carpeta los scripts necesarios para generar ejecutables del proyecto de manera sencilla.

## Scripts Disponibles

### Linux/macOS: `build.sh`
```bash
cd scripts
./build.sh
```

###  Windows: `build_windows.bat`
```bash
cd scripts
build_windows.bat
```

## Archivos de Configuración

### `simulador.spec`
Archivo de configuración de **PyInstaller** que define:
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


## Modificar Build

Para cambiar la configuración del build, edita `simulador.spec` en la raíz:
- Cambiar nombre del ejecutable
- Agregar/remover módulos
- Modificar opciones de PyInstaller


## Notas Importantes

- **Las carpetas `build` y `dist` se borran automáticamente** en cada build

