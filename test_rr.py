#!/usr/bin/env python3
"""
Script de prueba para el algoritmo Round Robin.
"""

import sys
import os

# Agregar el directorio src al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from simulador.proceso import Proceso
from simulador.algoritmos.RR import RR

def crear_procesos_prueba():
    """Crea los procesos de prueba según los datos proporcionados."""
    procesos = [
        Proceso(
            nombre="P1",
            tiempo_arrivo=0,
            cantidad_rafagas_cpu=4,
            duracion_rafagas_cpu=3,
            duracion_rafagas_io=2,
            prioridad=3
        ),
        Proceso(
            nombre="P2",
            tiempo_arrivo=1,
            cantidad_rafagas_cpu=2,
            duracion_rafagas_cpu=8,
            duracion_rafagas_io=5,
            prioridad=1
        ),
        Proceso(
            nombre="P3",
            tiempo_arrivo=3,
            cantidad_rafagas_cpu=5,
            duracion_rafagas_cpu=2,
            duracion_rafagas_io=1,
            prioridad=4
        ),
        Proceso(
            nombre="P4",
            tiempo_arrivo=6,
            cantidad_rafagas_cpu=3,
            duracion_rafagas_cpu=6,
            duracion_rafagas_io=4,
            prioridad=2
        ),
        Proceso(
            nombre="P5",
            tiempo_arrivo=10,
            cantidad_rafagas_cpu=1,
            duracion_rafagas_cpu=10,
            duracion_rafagas_io=0,
            prioridad=5
        )
    ]
    return procesos

def imprimir_eventos(eventos):
    """Imprime los eventos de la simulación de forma organizada."""
    print("\n" + "="*80)
    print("EVENTOS DE LA SIMULACIÓN")
    print("="*80)
    print(f"{'Tiempo':<8} {'Proceso':<8} {'Evento':<25} {'Estado':<20}")
    print("-"*80)
    
    for evento in eventos:
        print(f"{evento['tiempo']:<8} {evento['proceso']:<8} {evento['evento']:<25} {evento['estado']:<20}")

def imprimir_estadisticas(algoritmo):
    """Imprime las estadísticas de la simulación."""
    print("\n" + "="*80)
    print("ESTADÍSTICAS DE LA SIMULACIÓN")
    print("="*80)
    
    # Estadísticas de CPU
    stats = algoritmo.obtener_estadisticas_cpu()
    print(f"Tiempo total: {stats['t_total']}")
    print(f"CPU procesos: {stats['cpu_proc']} ({stats['cpu_proc']/stats['t_total']*100:.1f}%)")
    print(f"CPU SO: {stats['cpu_so']} ({stats['cpu_so']/stats['t_total']*100:.1f}%)")
    print(f"CPU idle: {stats['cpu_idle']} ({stats['cpu_idle']/stats['t_total']*100:.1f}%)")
    
    # Estadísticas por proceso
    print(f"\n{'Proceso':<10} {'Tiempo Retorno':<15} {'Tiempo Listo':<15} {'CPU Usado':<10}")
    print("-"*60)
    
    for proceso in algoritmo.procesos_terminados:
        print(f"{proceso.nombre:<10} {proceso.tiempo_retorno:<15} {proceso.tiempo_en_listo:<15} {stats['cpu_proc_por_proceso'].get(proceso.nombre, 0):<10}")

def main():
    """Función principal del script de prueba."""
    print("="*80)
    print("PRUEBA DEL ALGORITMO ROUND ROBIN")
    print("="*80)
    
    # Crear procesos de prueba
    procesos = crear_procesos_prueba()
    
    # Parámetros de la simulación
    tiempo_tip = 1
    tiempo_tcp = 1
    tiempo_tfp = 1
    quantum = 5
    
    print(f"Parámetros:")
    print(f"  TIP: {tiempo_tip}")
    print(f"  TCP: {tiempo_tcp}")
    print(f"  TFP: {tiempo_tfp}")
    print(f"  Quantum: {quantum}")
    
    print(f"\nProcesos:")
    for proceso in procesos:
        print(f"  {proceso.nombre}: llegada={proceso.tiempo_arrivo}, "
              f"rafagas_cpu={proceso.cantidad_rafagas_cpu}, "
              f"duracion_cpu={proceso.duracion_rafagas_cpu}, "
              f"duracion_io={proceso.duracion_rafagas_io}")
    
    # Crear y ejecutar algoritmo Round Robin
    algoritmo = RR(procesos, tiempo_tip, tiempo_tcp, tiempo_tfp, quantum)
    
    print(f"\nEjecutando simulación...")
    algoritmo.ejecutar()
    
    # Imprimir resultados
    imprimir_eventos(algoritmo.resultados)
    imprimir_estadisticas(algoritmo)
    
    print("\n" + "="*80)
    print("SIMULACIÓN COMPLETADA")
    print("="*80)

if __name__ == "__main__":
    main()
