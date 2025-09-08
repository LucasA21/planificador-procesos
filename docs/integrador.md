# Planificación del Procesador

### Objetivo
Programar un sistema que simule distintas estrategias de planificación del procesador (dispatcher) y calcule un conjunto de indicadores que serán utilizados para discutir las ventajas y desventajas de cada estrategia.

### Características del Sistema
- **Tipo de sistema**: Multiprogramado y monoprocesador
- **Entrada**: Archivo con datos de procesos
- **Salida**: Archivo de eventos y métricas de rendimiento

### Datos de Entrada por Proceso
Cada registro del archivo debe contener:
1. **Nombre del proceso**
2. **Tiempo de arribo**
3. **Cantidad de ráfagas de CPU** necesarias para terminar
4. **Duración de la ráfaga de CPU**
5. **Duración de la ráfaga de entrada-salida** entre ráfagas de CPU
6. **Prioridad externa**

### Políticas de Planificación Requeridas
El simulador debe permitir seleccionar entre:
- **FCFS** (First Come First Served)
- **Prioridad Externa**
- **Round-Robin**
- **SPN** (Shortest Process Next)
- **SRTN** (Shortest Remaining Time Next)

### Parámetros del Sistema
El usuario debe poder configurar:
- **TIP**: Tiempo que utiliza el SO para aceptar nuevos procesos
- **TFP**: Tiempo que utiliza el SO para terminar procesos
- **TCP**: Tiempo de conmutación entre procesos
- **Quantum**: Tiempo de quantum (si es necesario)

### Salidas del Simulador

#### Archivo de Eventos
Debe registrar todos los eventos del sistema con sus tiempos:
- Arribo de trabajo
- Incorporación de trabajo al sistema
- Completado de ráfaga de proceso
- Agotamiento de quantum
- Terminación de operación de E/S
- Atención de interrupción de E/S
- Terminación de proceso

#### Indicadores por Proceso
- **Tiempo de Retorno** (TRp): Desde que arriba hasta que termina (incluyendo TFP)
- **Tiempo de Retorno Normalizado** (TRn): TRp dividido por tiempo efectivo de CPU
- **Tiempo en Estado de Listo**

#### Indicadores de la Tanda
- **Tiempo de Retorno de la Tanda** (TRt): Desde que arriba el primer proceso hasta el último TFP
- **Tiempo Medio de Retorno** (TMRt): Suma de TRp dividido por cantidad de procesos

#### Uso de CPU
- Tiempos de CPU desocupada
- CPU utilizada por el SO
- CPU utilizada por los procesos
- Valores en tiempos absolutos y porcentuales

### Condiciones de Implementación

#### Orden de Procesamiento de Eventos
1. Corriendo → Terminado
2. Corriendo → Bloqueado
3. Corriendo → Listo
4. Bloqueado → Listo
5. Nuevo → Listo
6. **Finalmente**: Despacho de Listo → Corriendo

#### Reglas Específicas
- **Round Robin**: Si hay un único proceso y su quantum termina, se pasa a listo y luego se le vuelve a asignar la CPU (usando TCP)
- **Despacho inicial**: También requiere TCP
- **Transición Bloqueado → Listo**: Instantánea (0 unidades de tiempo, considerada dentro del TCP posterior)
- **Prioridades**: Valores de 1 a 100, siendo los más grandes de mayor prioridad
- **Expropiación**: En Prioridades y SRT, se expropia la CPU si aparece un proceso con mayor prioridad o menor tiempo restante
- **Estado de Listo**: Un proceso no computa tiempo de listo hasta cumplir su TIP

### Requisitos de Presentación
- **Pruebas**: Al menos 4 tandas de trabajos con características distintas
- **Lenguaje**: Java o cualquier lenguaje conocido
- **Ejecutable**: Debe ejecutarse intuitivamente sin instalación de librerías
- **Documentación**: Diagramas de Gantt, de clases, de flujo
- **Formato**: Archivo JSON acordado para todos los trabajos
- **Entrega**: Código fuente y ejecutable en soporte digital o repositorio

### Beneficios Académicos
- **Exención**: Trabajo correctamente resuelto exime de rendir puntos de planificación en el parcial
- **Puntaje**: Máximo puntaje previsto para esos puntos
- **Fecha límite**: Sin excepción

### Definiciones Importantes
- **Tiempo de Retorno de un proceso (TRp)**: Desde que arriba hasta que termina (después de su TFP, incluyendo éste)
- **Tiempo de retorno normalizado (TRn)**: TRp dividido por el tiempo efectivo de CPU utilizado
- **Tiempo de retorno de la tanda (TRt)**: Desde que arriba el primer proceso hasta que se realiza el último TFP
- **Tiempo Medio de retorno de la tanda (TMRt)**: Suma de los TRp dividido por la cantidad de procesos


### A tener en cuenta


- Cada proceso "NUEVO" tiene que pagar una cuota de TIP (tiempo de ingreso del proceso) y solo lo paga cuando entra por primera vez al sistema, este tiempo que paga lo va a determinar el TIP que ingresemos en la interfaz, por otro lado cada vez que el CPU elije cambiar de un proceso a otro se paga un TCP un tiempo de conmutacion, que tambien lo definimos en la interfaz. Por ultimo cuando un proceso termina tambien consume un TFP (tiempo de finalizacion del proceso), que tambien lo definimos en la interfaz. Es muy importante tener en cuenta que mientras se esta consumiendo alguno de estos 3 tiempos la cpu no puede ejecutarse, debe esperar que se termine de consumir el tiempo.

Muy importante tambien, el tiempo de retorno es el tiempo de finalizacion del proceso (al tiempo de finalizacion hay que sumarle el TFP tambien) menos el tiempo de arribo, en el caso de que el proceso 5 termine en el tiempo 36, y tenga un arrivo de 10, el tiempo de retorno seria 26