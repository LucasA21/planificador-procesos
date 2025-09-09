#!/usr/bin/env python3
"""
Test para verificar que el mapeo de datos entre la interfaz y el simulador funciona correctamente.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from simulador.simulador import Simulador

def test_mapeo_datos():
    """Test del mapeo de datos."""
    
    # Datos como los envía la interfaz (después del file_loader)
    procesos_datos_interfaz = [
        {
            'nombre': 'P1',
            'tiempo_arribo': 0,
            'cantidad_rafagas_cpu': 4,
            'duracion_rafaga_cpu': 3,
            'duracion_rafaga_es': 2,
            'prioridad_externa': 3
        },
        {
            'nombre': 'P2',
            'tiempo_arribo': 1,
            'cantidad_rafagas_cpu': 2,
            'duracion_rafaga_cpu': 8,
            'duracion_rafaga_es': 5,
            'prioridad_externa': 1
        }
    ]
    
    print("=== Test Mapeo de Datos ===")
    print("Datos de entrada (como los envía la interfaz):")
    for p in procesos_datos_interfaz:
        print(f"  {p}")
    
    # Crear simulador
    simulador = Simulador()
    
    try:
        # Ejecutar FCFS
        resultados = simulador.ejecutar_fcfs(procesos_datos_interfaz, 1, 1, 1)
        
        print(f"\n✅ ÉXITO: El mapeo de datos funciona correctamente")
        print(f"Tiempo total: {resultados['tiempo_total']}")
        print(f"Procesos terminados: {len([p for p in resultados['procesos'] if p['tiempo_retorno'] > 0])}/{len(procesos_datos_interfaz)}")
        
        print(f"\nProcesos terminados:")
        for proceso in resultados['procesos']:
            if proceso['tiempo_retorno'] > 0:
                print(f"  {proceso['nombre']}: retorno={proceso['tiempo_retorno']}")
            else:
                print(f"  {proceso['nombre']}: NO TERMINADO")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("El mapeo de datos no funciona correctamente")

if __name__ == "__main__":
    test_mapeo_datos()
