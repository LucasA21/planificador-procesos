#!/bin/bash

echo "=== CONSTRUCTOR DE EJECUTABLE PARA LINUX ==="
echo ""

# Obtener el directorio raíz del proyecto
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "Directorio del proyecto: $PROJECT_ROOT"

# Cambiar al directorio raíz del proyecto
cd "$PROJECT_ROOT"

# Limpiar solo builds anteriores (no la carpeta build)
echo "Limpiando builds anteriores..."
rm -rf dist

# Crear directorio de salida
mkdir -p dist/linux

# Generar ejecutable para Linux
echo "Generando ejecutable para Linux..."
# Asegurar que las variables de entorno estén disponibles
export DISPLAY=${DISPLAY:-:0}
poetry run pyinstaller simulador.spec --distpath dist/linux --clean

# Verificar si se generó correctamente
if [ -f "dist/linux/Simulador_Planificacion" ]; then
    # Dar permisos de ejecución
    echo "Configurando permisos de ejecución..."
    chmod +x dist/linux/Simulador_Planificacion
    
    echo ""
    echo "¡Build completado exitosamente!"
    echo "Ubicación: dist/linux/Simulador_Planificacion"
    echo "Tamaño: $(du -h dist/linux/Simulador_Planificacion | cut -f1)"
    echo ""
    echo "Para ejecutar: ./dist/linux/Simulador_Planificacion"
else
    echo ""
    echo "Error: No se pudo generar el ejecutable"
    echo "Revisa los errores anteriores"
    exit 1
fi
