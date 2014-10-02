# coding=utf-8
# ====================================================================
#                            TEMPORIZADOR
# ====================================================================

# Temporización continua de eventos (funciones arbitrarias) a períodos
# fijos.

# La versión actual del temporizador sólo puede programar una única
# función (via threading.timer), había una versión previa que podía
# schedulear varias funciones (via sched.scheduler) garantizando una
# ejecución serial de éstas. Si se quieren schedulear N tareas, en
# esta versión deben usarse N temporizadores (cada uno creará un
# thread, y no se garantiza una ejecución serial entre las tareas de
# los distintos temporizadores (son independientes), es decir puede
# haber race conditions si las tareas acceden a una región crítica).
#
# Actualmente, el protocolo de temporización consiste en tres pasos:
# primero instanciar el temporizador (sin argumentos o con un
# argumento de velocidad para acelerar o desacelerar la
# temporización), luego programar la temporización (cuánto tiempo, qué
# función y opcionalmente qué argumentos) y finalmente activarlo (ver
# ejemplo a continuación):

# t = Temporizador()
# t.ejecutarCada(duracion, funcion)
# t.iniciarEjecucion()

# El argumento 'duracion' es cualquier instancia de Duracion, es
# independiente de la unidad. La función puede ser un lambda o una
# función definida con 'def'. Si hay argumentos para la función, se
# pasan en una lista como último argumento.

# En cualquier momento puede llamarse a 'ejecutarCada' para crear un
# nuevo scheduling (si había una tarea programada, se cancela
# automáticamente). Además, el método 'detener' sirve para detener el
# temporizador (cancela la programación de la tarea, si había), en
# este estado puede volver a programarse una tarea (aunque no es
# necesario detenerla para hacer esto, por lo recién explicado).

# Notar que el hecho de que un temporizador tenga la facultad de
# ejecutar una tarea que lo detenga permite ejecutar tareas una
# cantidad finita (definida) de veces, por ejemplo, para ejecutar una
# tarea una única vez, la función parámetro puede consistir en
# ejecutar la tarea propiamente dicha seguida de una detención del
# temporizador. No es lo más elegante pero funciona si se hace con
# cuidado.

# En esta versión no puede modificarse la velocidad, sólo puede
# pasarse como parámetro durante la construcción.

# Ver demo al final.

# ====================================================================

import threading


class Temporizador:
    """Un temporizador: se utiliza para ejecutar una tarea en forma
    repetida con un período dado (una duración) y opcionalmente a una
    velocidad dada (cuántos segundos de duración por segundo de la
    realidad, usado para reescalar el tiempo). Primero debe definirse
    la tarea (una función), finalmente se pone a ejecutar el
    temporizador. La tarea se ejecutará en su propio thread.

    """

    def __init__(self, velocidad=1.0):
        # usamos el timer provisto por Python
        self.timer = None
        assert(velocidad > 0)
        self._velocidad = velocidad

    def _action(self, segundos, funcion, args):
        # esta función es un pequeño hack para reschedulear la
        # función, no forma parte de la interfaz.
        funcion(*args)               # llamamos a la función primero
        # podría ser que la función recién ejecutada haya tenido como
        # efecto lateral detener a este temporizador. Rescheduleamos
        # sólo si no está detenido. Así permitimos que un temporizador
        # planifique su propia detención.
        if self.timer is not None:
            self._ejecutarCada(segundos, funcion, args)  # la rescheduleamos
            self.timer.start()                         # y activamos

    def _ejecutarCada(self, segundos, funcion, args):
        self.timer = threading.Timer(segundos, self._action,
                                     [segundos, funcion, args])

    def ejecutarCada(self, duracion, funcion, args=None):
        """Encarga una función para ser ejecutada con un período dado

        """
        # primero cancelamos el timer si estaba ya instanciado
        if self.timer:
            self.timer.cancel()
        # convertimos a segundos y le damos rosca para que empiece el
        # ciclo de temporizaciones.
        segundos = duracion.aSegundos().valor() / self._velocidad
        if args is None:
            args = []
        self._ejecutarCada(segundos, funcion, args)

    def detener(self):
        """Detiene el temporizador, si había una tarea pendiente se cancela.
        Siempre puede volver a programarse una tarea con un
        temporizador detenido (como si estuviese recién construido),
        pero no es necesario detenerlo para hacer una reprogramación.

        """
        self.timer.cancel()
        self.timer = None       # con esto indicamos que está detenido

    def iniciarEjecucion(self):
        """Pone en marcha el temporizador.

        """
        self.timer.start()

# ====================================================================
# mini demo (para correr en la repl)

# Lo que hace es ejecutar algunas tareas a distintos intervalos
# de unos pocos segundos (se imprimen los minutos y segundos para
# mayor claridad). Luego de unos instantes se detienen los
# temporizadores (esto está programado también). Al ejecutarlo en la
# repl, se crean varios threads hasta que sólo queda activo el
# thread de la repl.

def demo():
    from time import gmtime, strftime
    from tiempo import DuracionEnSegundos

    #
    # 0. inicialización de algunas mierditas
    #
    class Contador:
        pass

    def incrementar(contador):
        contador.i += 1
    contador = Contador()
    contador.i = 0

    def detener(temporizadores, contador):
        # detiene los temporizadores e imprime el valor del contador.
        for t in temporizadores:
            t.detener()
        print("terminado. contador = %d" % contador.i)

    #
    # 1. creamos los temporizadores
    #
    velocidad = 2             # 1.0 = escala real, 2.0 = doblemente rápido
    t1 = Temporizador(velocidad)
    t2 = Temporizador(velocidad)
    t3 = Temporizador(velocidad)
    t4 = Temporizador(velocidad)
    temporizadores = [t1, t2, t3, t4]

    #
    # 2. programamos los temporizadores
    #
    t1.ejecutarCada(DuracionEnSegundos(2),
                    lambda: print("2      : ", strftime("%M:%S", gmtime())))
    t2.ejecutarCada(DuracionEnSegundos(4),
                    lambda: print("4      : ", strftime("%M:%S", gmtime())))
    t3.ejecutarCada(DuracionEnSegundos(1), incrementar, [contador])
    t4.ejecutarCada(DuracionEnSegundos(12), detener,
                    [temporizadores, contador])
    # notar que t4 detiene a todos los temporizadores, incluso se
    # detiene a sí mismo.

    #
    # 3. ponemos los temporizadores a ejecutar
    #
    print("ejecutando temporizadores a velocidad = %.2f" % velocidad)
    for t in temporizadores:
        t.iniciarEjecucion()
    print("hay %d temporizadores y %d threads en ejecución" %
          (len(temporizadores), threading.active_count()))

if __name__ == "__main__":
    demo()

# tick, tock, tick, tock ...
