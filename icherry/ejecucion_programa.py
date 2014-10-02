# ====================================================================
#                EJECUCIÓN DEL PROGRAMA DE SUMINISTRO
# ====================================================================

# Ejecución del programa de suministro

# En este módulo se define lo relacionado con la planificación y
# ejecución de las acciones del programa de suministro. Durante el
# funcionamiento de iCherry, a lapsos fijos se ejecuta un "heartbeat"
# en que un planificador de ejecución se activa y decide qué acciones
# del programa de suministro deben ejecutarse en ese instante. Estas
# acciones se remueven del plan de suministro y son ejecutadas de
# inmediato por el ejecutor de acción, activando los actuadores para
# que éstos tomen la acción que corresponda. Terminado esto, el
# heartbeat termina, reiniciando el ciclo.

from icherry.magnitudes import Rango


# ====================================================================
# PlanificadorDeEjecucion

# La "planificación" es como denominamos al proceso de seleccionar qué
# acciones corresponden al heartbeat de ejecución del plan de
# suministro, es el planificador de ejecución que lleva esta tarea a
# cabo. Un planificador está configurado con un parámetro de duración
# que le especifica cuánto tiempo de acciones programadas debe
# seleccionarse para ejecución. Cuanto mayor sea esta duración, más
# acciones se ejecutarán por heartbeat. Este parámetro debe escogerse
# con cuidado y tener una relación razonable con el período de
# heartbeat del generador del plan de suministro.

class PlanificadorDeEjecucion:
    # NOTICE: hay muchas combinaciones posibles para armar el
    # planificador. Al planificador lo despierta un temporizador
    # externo, o el temporizador es interno? Requiere realmente
    # consultar la hora a la central meteorológica, o simplemente
    # podemos aprovechar que la hora de despierte es la hora previa de
    # despierte más el delta de heartbeat? Hay mucho para decidir, y
    # por lo tanto mucho que puede variar acá. Por ahora considerar
    # esto en un estado muy inmaduro!

    def __init__(self, delta, programaDeSuministro, ejecutorDeAccion):
        self._programaDeSuministro = programaDeSuministro
        self._delta = delta  # NOTICE: Es una duración (magnitud)
        self._ejecutor = ejecutorDeAccion

    def planificarAcciones(self, fechaYHora):
        desde = fechaYHora
        hasta = fechaYHora.agregarDuracion(self._delta)
        lapso = Rango(desde, hasta)
        accionesAEjecutar = self._programaDeSuministro.retirarAccionesEnHorario(lapso)
        for accion in accionesAEjecutar:
            self._ejecutor.ejecutarAccion(accion)

# ====================================================================
# EjecutorDeAccion

# Un ejecutor es el responsable de ejecutar una acción (previamente
# obtenida del programa de suministro). El ejecutor cuenta con cuatro
# actuadores, uno para cada dimensión de acción (Regado, Fertilizante,
# Antibiótico, Luz). El método 'ejecutarAcción()' es el más importante
# porque define la API con el exterior, los demás métodos son de uso
# interno compartido con las acciones (para doble dispatch). El método
# 'ejecutarEn()' de las acciones se engancha en doble dispatch con los
# métodos ejecutarAccion, ejecutarRegado, etc, para finalmente poner
# en acción al actuador correspondiente.


class EjecutorDeAccion:

    def __init__(self, actuadorRegado, actuadorFertilizante,
                 actuadorAntibiotico, actuadorLuz):
        self._actuadorRegado = actuadorRegado
        self._actuadorFertilizante = actuadorFertilizante
        self._actuadorAntibiotico = actuadorAntibiotico
        self._actuadorLuz = actuadorLuz

    # Esquema de doble dispatch:
    # ---->  ejecutarAccion      | EjecutorDeAccion (self)
    # <----  ejecutarEn          | Accion
    # ---->  ejecutar{R,F,A,L}   | EjecutorDeAccion (self)
    # <----  aplicar             | Actuador

    def ejecutarAccion(self, accion):
        """Ejecuta una acción dada. Esto activará al actuador correspondiente
        para que éste a su vez aplique una cantidad apropiada del
        suministro correspondiente al tipo de acción.

        """
        accion.ejecutarEn(self)  # esto dispara el doble dispatch

    # los que siguen son los métodos que ejecutan cada tipo de acción

    def ejecutarRegado(self, cantidad):
        self._actuadorRegado.aplicar(cantidad)

    def ejecutarFertilizante(self, cantidad):
        self._actuadorFertilizante.aplicar(cantidad)

    def ejecutarAntibiotico(self, cantidad):
        self._actuadorAntibiotico.aplicar(cantidad)

    def ejecutarLuz(self, cantidad):
        self._actuadorLuz.aplicar(cantidad)
