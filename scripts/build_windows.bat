@echo off
echo === CONSTRUCTOR DE EJECUTABLE PARA WINDOWS ===
echo.

REM Obtener el directorio raíz del proyecto (subir un nivel desde scripts/)
cd /d "%~dp0.."
set PROJECT_ROOT=%CD%
echo Directorio del proyecto: %PROJECT_ROOT%

REM Limpiar solo builds anteriores (no la carpeta build)
echo Limpiando builds anteriores...
if exist dist rmdir /s /q dist

REM Crear directorio de salida
echo Creando directorio de salida...
mkdir dist\windows

REM Generar ejecutable para Windows
echo Generando ejecutable para Windows...
poetry run pyinstaller simulador.spec --distpath dist\windows

REM Verificar si se generó correctamente
if exist "dist\windows\Simulador_Planificacion.exe" (
    echo.
    echo ¡Build completado exitosamente!
    echo Ubicacion: dist\windows\Simulador_Planificacion.exe
    
    REM Mostrar tamaño del archivo
    for %%A in ("dist\windows\Simulador_Planificacion.exe") do echo Tamaño: %%~zA bytes
    
    echo.
    echo Para ejecutar: dist\windows\Simulador_Planificacion.exe
    echo.
    echo Presiona cualquier tecla para abrir la carpeta...
    pause >nul
    explorer dist\windows
) else (
    echo.
    echo Error: No se pudo generar el ejecutable
    echo Revisa los errores anteriores
    pause
    exit /b 1
)
