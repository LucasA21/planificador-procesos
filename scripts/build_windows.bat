@echo off
setlocal enabledelayedexpansion
echo === CONSTRUCTOR DE EJECUTABLE PARA WINDOWS ===
echo.

REM Obtener el directorio raíz del proyecto (subir un nivel desde scripts/)
cd /d "%~dp0.."
set PROJECT_ROOT=%CD%
echo Directorio del proyecto: %PROJECT_ROOT%

REM Verificar si Python está instalado
echo Verificando Python...
py --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://python.org
    echo.
    pause
    exit /b 1
)

REM Instalar/Actualizar todas las dependencias necesarias
echo Instalando dependencias del proyecto...
echo - Actualizando pip...
py -m pip install --upgrade pip --quiet

echo - Instalando dependencias principales...
py -m pip install customtkinter>=5.2.2 matplotlib>=3.10.5 tk>=0.1.0 ctktable>=1.1 screeninfo>=0.8.1 reportlab>=4.4.3 --quiet

echo - Instalando PyInstaller...
py -m pip install pyinstaller>=6.15.0 --quiet

REM Verificar que PyInstaller se instaló correctamente
py -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: PyInstaller no se pudo instalar correctamente
    echo Intentando instalación manual...
    py -m pip install pyinstaller --force-reinstall
    if errorlevel 1 (
        echo.
        echo ERROR: No se pudo instalar PyInstaller
        pause
        exit /b 1
    )
)

echo Todas las dependencias instaladas correctamente.

REM Verificar que los módulos principales se pueden importar
echo Verificando módulos principales...
py -c "import customtkinter, matplotlib, tkinter, CTkTable, screeninfo, reportlab; print('Todos los módulos verificados correctamente')" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ADVERTENCIA: Algunos módulos no se pudieron verificar
    echo Continuando con la construcción...
    echo.
)

REM Limpiar builds anteriores
echo Limpiando builds anteriores...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM Crear directorio de salida
echo Creando directorio de salida...
mkdir dist\windows

REM Generar ejecutable para Windows
echo Generando ejecutable para Windows...
py -m PyInstaller simulador.spec --distpath dist\windows

REM Verificar si se generó correctamente
if exist "dist\windows\Simulador_Planificacion.exe" (
    echo.
    echo ================================================
    echo ¡BUILD COMPLETADO EXITOSAMENTE!
    echo ================================================
    echo.
    echo Ubicación: dist\windows\Simulador_Planificacion.exe
    
    REM Mostrar tamaño del archivo
    for %%A in ("dist\windows\Simulador_Planificacion.exe") do (
        set /a size_mb=%%~zA/1024/1024
        echo Tamaño: %%~zA bytes (~!size_mb! MB^)
    )
    
    echo.
    echo Para ejecutar el simulador:
    echo   dist\windows\Simulador_Planificacion.exe
    echo.
    echo El ejecutable es independiente y no requiere Python instalado.
    echo.
    echo ¿Deseas abrir la carpeta del ejecutable? (S/N^)
    choice /c SN /n /m "Presiona S para abrir la carpeta o N para salir: "
    if errorlevel 2 goto :fin
    if errorlevel 1 explorer dist\windows
    :fin
) else (
    echo.
    echo ================================================
    echo ERROR: NO SE PUDO GENERAR EL EJECUTABLE
    echo ================================================
    echo.
    echo Posibles causas:
    echo - Falta alguna dependencia
    echo - Error en el archivo simulador.spec
    echo - Problema con PyInstaller
    echo.
    echo Revisa los mensajes de error anteriores para más detalles.
    echo.
    pause
    exit /b 1
)
