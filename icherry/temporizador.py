# ====================================================================
#                            TEMPORIZADOR
# ====================================================================

# Temporización continua de eventos (funciones arbitrarias) a períodos
# fijos.

# La versión actual del temporizador sólo puede programar una única
# función (via threading.timer), había una versión previa que podía
# schedulear varias funciones al mismo tiempo (via sched.scheduler),
# garantizando una ejecución serial de las mismas. Si se quieren
# schedulear N tareas, en esta versión deben usarse N temporizadores
# (cada uno requerirá un thread, y no se garantiza una ejecución
# serial, es decir puede haber race conditions si las tareas acceden a
# una región crítica).
#
# Actualmente, el protocolo de temporización consiste en tres pasos:
# primero instanciar el temporizador (sin argumentos), luego programar
# la temporización y finalmente activarlo (ver ejemplo a
# continuación):

# t = Temporizador()
# t.EjecutarCada(tiempo, funcion)
# t.IniciarEjecucion()

# El tiempo es en segundos. La función puede ser un lambda o una
# función definida con 'def' (esto asume un diseño en que no hay un
# concepto de 'closure').

# En cualquier momento puede llamarse a 'EjecutarCada' para crear un
# nuevo scheduling (si había una tarea programada, se cancela
# automáticamente). Además, el método 'Detener' sirve para detener el
# temporizador (cancela la programación de la tarea, si había).

# Ver demo al final.

# ====================================================================

import threading

class Temporizador :
    """Un temporizador: se utiliza para ejecutar una tarea en forma
    repetida con un período dado. Primero debe definirse la tarea (una
    función), finalmente se pone a ejecutar el temporizador. La tarea
    se ejecutará en su propio thread.

    """

    def __init__(self) :
        # usamos el scheduler provisto por Python
        # self.scheduler = sched.scheduler()
        self.timer = None

    def _action(self,tiempo,funcion) :
        # esta función es un pequeño hack para reschedulear la
        # función, no forma parte de la interfaz.
        funcion()               # llamamos a la función primero
        self.EjecutarCada(tiempo,funcion)  # y la rescheduleamos
        self.timer.start()

    def EjecutarCada(self,tiempo,funcion) :
        """Encarga una función para ser ejecutada con un período dado

        """
        # primero cancelamos el timer si estaba ya instanciado
        if self.timer : self.timer.cancel()
        self.timer = threading.Timer(tiempo,self._action,[tiempo,funcion])

    def Detener(self) :
        """Detiene el temporizador, si había una tarea pendiente se cancela.

        """
        self.timer.cancel()

    def IniciarEjecucion(self) :
        """Pone en marcha el temporizador.

        """
        self.timer.start()

# ====================================================================
# mini demo (para correr en la repl)

# Lo que hace es ejecutar un par de tareas a intervalos de 2 y 4
# segundos respectivamente (se imprimen los minutos y segundos para
# mayor claridad). Luego de unos instantes se detienen los
# temporizadores (esto está programado también). Al ejecutarlo en la
# repl, hay un total de 4 threads hasta que sólo queda activo el
# thread de la repl.

def detener(t1,t2) :
    t1.Detener()
    t2.Detener()
    print("terminado!")

# una pruebita para ver cómo anda
def demo() :
    from time import gmtime, strftime
    t1 = Temporizador()
    t2 = Temporizador()
    t1.EjecutarCada(2,lambda:print("2: ",strftime("%M:%S", gmtime())))
    t2.EjecutarCada(4,lambda:print("4: ",strftime("%M:%S", gmtime())))
    t1.IniciarEjecucion()
    t2.IniciarEjecucion()
    s = threading.Timer(16,detener,args=[t1,t2])
    s.start()
    print("hay %d threads en ejecución" % threading.active_count())

if __name__ == "__main__" : demo()

# tick, tock, tick, tock ...
