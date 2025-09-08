"""
Implementacion del algoritmo FCFS (First Come First Served).

Este algoritmo es el mas sencillo:
- Debe fijarse en la cola de listos cual es el proceso que arribo primero
- Una vez se selecciona el proceso puede largarlo a ejecutar
- Para ejecutarlo primero debe consumir el TIP (este atributo va a ser puesto por el usuario), el TIP es el tiempo de ingreso del proceso,
se va a consumir solo la primera vez que un proceso pasa de nuevo a listo, si el proceso se bloquea y vuelve a entrar a la cola de listos no se consume
- Luego se va a ejecutar la rafaga de cpu pertinente (tambien puesto por el usuario)
- Cuando termine de ejecutarse la rafaga, se va a ejecutar la rafaga de I/O (tambien proporcionada por el usuario), la rafaga de I/O se va a ejecutar
siempre mientras el valor de la rafaga de I/O sea mayor que 0 y se haya terminado de ejecutar la rafaga.
- El proceso se va a ejecutar hasta que termine su tiempo total de cpu (tambien introducido por el usuario), este tiempo total no es lo mismo que la rafaga
de cpu, ejemplo: un proceso puede ejecutar a la vez 3 rafagas de cpu y el tiempo total para que finalize es de 12 rafagas, por lo cual debera ejecutarse
4 veces para terminar, y cada vez que se bloquee por que su burst time(rafagas que puede hacer) se termine, se bloquea haciendo las rafagas de I/O
- Cada vez que se se ejecute un proceso, se debe consumir el TCP, esto se consume cada vez que el planificador cambia de un proceso a otro (al principio, 
cuando un proceso es nuevo es decir pasa de nuevo a listo, el tcp no se consume, si no que se consume el tip).
"""
