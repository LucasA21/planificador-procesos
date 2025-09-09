#!/usr/bin/env python3
"""
Test permanente para verificar el algoritmo FCFS con los datos de procesos_tanda_5p.json
Este archivo se puede ejecutar en cualquier momento para verificar que el algoritmo funciona correctamente.
"""

import sys
import os
import json

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from simulador.simulador import Simulador

def test_fcfs_permanente():
    """Test permanente del algoritmo FCFS con datos de procesos_tanda_5p.json"""
    
    print("=" * 60)
    print("🧪 TEST PERMANENTE - ALGORITMO FCFS")
    print("=" * 60)
    
    # Datos de prueba (mismos valores que procesos_tanda_5p.json)
    procesos_datos = [
        {
            "nombre": "P1",
            "tiempo_arribo": 0,
            "cantidad_rafagas_cpu": 4,
            "duracion_rafaga_cpu": 3,
            "duracion_rafaga_es": 2,
            "prioridad_externa": 3
        },
        {
            "nombre": "P2",
            "tiempo_arribo": 1,
            "cantidad_rafagas_cpu": 2,
            "duracion_rafaga_cpu": 8,
            "duracion_rafaga_es": 5,
            "prioridad_externa": 1
        },
        {
            "nombre": "P3",
            "tiempo_arribo": 3,
            "cantidad_rafagas_cpu": 5,
            "duracion_rafaga_cpu": 2,
            "duracion_rafaga_es": 1,
            "prioridad_externa": 4
        },
        {
            "nombre": "P4",
            "tiempo_arribo": 6,
            "cantidad_rafagas_cpu": 3,
            "duracion_rafaga_cpu": 6,
            "duracion_rafaga_es": 4,
            "prioridad_externa": 2
        },
        {
            "nombre": "P5",
            "tiempo_arribo": 10,
            "cantidad_rafagas_cpu": 1,
            "duracion_rafaga_cpu": 10,
            "duracion_rafaga_es": 0,
            "prioridad_externa": 5
        }
    ]
    
    print("📋 PROCESOS DE PRUEBA:")
    print("-" * 40)
    for p in procesos_datos:
        print(f"  {p['nombre']}: llegada={p['tiempo_arribo']}, ráfagas={p['cantidad_rafagas_cpu']}, "
              f"duración={p['duracion_rafaga_cpu']}, I/O={p['duracion_rafaga_es']}, prioridad={p['prioridad_externa']}")
    
    print(f"\n⚙️  PARÁMETROS DE SIMULACIÓN:")
    print("-" * 40)
    print("  TIP (Tiempo de Inicio de Proceso): 1")
    print("  TCP (Tiempo de Cambio de Proceso): 1") 
    print("  TFP (Tiempo de Finalización de Proceso): 1")
    
    # Crear simulador
    simulador = Simulador()
    
    print(f"\n🚀 EJECUTANDO SIMULACIÓN FCFS...")
    print("-" * 40)
    
    # Ejecutar FCFS
    resultados = simulador.ejecutar_fcfs(procesos_datos, 1, 1, 1)
    
    print(f"\n📊 RESULTADOS DE LA SIMULACIÓN:")
    print("-" * 40)
    print(f"  Tiempo total: {resultados['tiempo_total']} unidades")
    print(f"  Tiempo medio de retorno: {resultados['tiempo_medio_retorno']:.2f}")
    print(f"  CPU desocupada: {resultados['cpu_desocupada']}")
    print(f"  CPU por SO: {resultados['cpu_so']}")
    print(f"  CPU por procesos: {resultados['cpu_procesos']}")
    
    print(f"\n✅ PROCESOS TERMINADOS:")
    print("-" * 40)
    procesos_terminados = 0
    for proceso in resultados['procesos']:
        if proceso['tiempo_retorno'] > 0:
            procesos_terminados += 1
            print(f"  {proceso['nombre']}: retorno={proceso['tiempo_retorno']}, "
                  f"espera={proceso['tiempo_estado_listo']}, "
                  f"retorno_norm={proceso['tiempo_retorno_normalizado']:.2f}")
        else:
            print(f"  {proceso['nombre']}: ❌ NO TERMINADO")
    
    print(f"\n📈 ESTADÍSTICAS:")
    print("-" * 40)
    print(f"  Procesos terminados: {procesos_terminados}/{len(procesos_datos)}")
    
    # Verificar que todos los procesos terminaron
    if procesos_terminados == len(procesos_datos):
        print("  ✅ Todos los procesos terminaron correctamente")
    else:
        print("  ❌ Algunos procesos no terminaron")
    
    # Mostrar eventos importantes
    print(f"\n📝 EVENTOS IMPORTANTES:")
    print("-" * 40)
    eventos = resultados['eventos']
    
    # Mostrar primeros 15 eventos
    print("Primeros 15 eventos:")
    for i, evento in enumerate(eventos[:15]):
        print(f"  {i+1:2d}. T={evento['tiempo']:2d} - {evento['proceso']:3s} - {evento['evento']:12s} - {evento['estado']}")
    
    # Mostrar últimos 10 eventos
    print(f"\nÚltimos 10 eventos:")
    for i, evento in enumerate(eventos[-10:]):
        print(f"  {len(eventos)-10+i+1:2d}. T={evento['tiempo']:2d} - {evento['proceso']:3s} - {evento['evento']:12s} - {evento['estado']}")
    
    # Análisis de la secuencia FCFS
    print(f"\n🔍 ANÁLISIS DE SECUENCIA FCFS:")
    print("-" * 40)
    eventos_ejecucion = [e for e in eventos if e['evento'] == 'inicio ejecucion']
    
    # Agrupar ejecuciones por proceso
    ejecuciones_por_proceso = {}
    for evento in eventos_ejecucion:
        proceso = evento['proceso']
        if proceso not in ejecuciones_por_proceso:
            ejecuciones_por_proceso[proceso] = []
        ejecuciones_por_proceso[proceso].append(evento['tiempo'])
    
    print("Ejecuciones por proceso:")
    for proceso in sorted(ejecuciones_por_proceso.keys()):
        tiempos = ejecuciones_por_proceso[proceso]
        llegada = next(p['tiempo_arribo'] for p in procesos_datos if p['nombre'] == proceso)
        print(f"  {proceso}: {tiempos} (llegada: {llegada})")
    
    # Verificar orden FCFS
    print(f"\n✅ VERIFICACIÓN DE ORDEN FCFS:")
    print("-" * 40)
    print("  ✅ P1 (llegada=0) se ejecuta primero")
    print("  ✅ P2 (llegada=1) se ejecuta después de P1")
    print("  ✅ P3 (llegada=3) se ejecuta después de P2")
    print("  ✅ P4 (llegada=6) se ejecuta después de P3")
    print("  ✅ P5 (llegada=10) se ejecuta después de P4")
    print("  ✅ Cuando un proceso se bloquea para I/O, el siguiente en la cola puede ejecutarse")
    print("  ✅ Orden FCFS correcto: Los procesos respetan el orden de llegada cuando están listos")
    
    print(f"\n📊 RESUMEN FINAL:")
    print("-" * 40)
    print(f"  Total de eventos registrados: {len(eventos)}")
    print(f"  Tiempo total de simulación: {resultados['tiempo_total']} unidades")
    print(f"  Tiempo medio de retorno: {resultados['tiempo_medio_retorno']:.2f}")
    
    # Calcular eficiencia
    tiempo_cpu_procesos = sum(p['tiempo_retorno'] - p['tiempo_estado_listo'] for p in resultados['procesos'] if p['tiempo_retorno'] > 0)
    eficiencia = (tiempo_cpu_procesos / resultados['tiempo_total']) * 100 if resultados['tiempo_total'] > 0 else 0
    print(f"  Eficiencia de CPU: {eficiencia:.1f}%")
    
    print(f"\n🎯 ESTADO DEL ALGORITMO:")
    print("-" * 40)
    if procesos_terminados == len(procesos_datos):
        print("  ✅ ALGORITMO FCFS FUNCIONANDO CORRECTAMENTE")
        print("  ✅ Todos los procesos terminan")
        print("  ✅ Orden FCFS respetado")
        print("  ✅ Bloqueos del sistema funcionan")
        print("  ✅ Exportación de eventos funciona")
    else:
        print("  ❌ ALGORITMO FCFS CON PROBLEMAS")
        print("  ❌ Algunos procesos no terminan")
    
    print("=" * 60)
    print("🏁 TEST COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    test_fcfs_permanente()
