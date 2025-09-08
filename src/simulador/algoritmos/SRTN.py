"""
Implementacion del algoritmo SRTN (Shortest Remaining Time Next).

Este es el unico algoritmo apropiativo (es decir, se apropia del cpu)
Este algoritmo prioriza los procesos mas cortos, es decir procesos con menor duracion de rafaga de cpu, a diferencia de los otros
si hay un proceso en ejecucion, y hay otro proceso en el mismo instante con menor duracion de rafagas de cpu, el proceso debe irse otra vez a la 
cola de listos (cada vez que pasa esto, se consume el TCP).
- Cada vez que se se ejecute un proceso, se debe consumir el TCP, esto se consume cada vez que el planificador cambia de un proceso a otro (al principio, 
cuando un proceso es nuevo es decir pasa de nuevo a listo, el tcp no se consume, si no que se consume el tip).
"""