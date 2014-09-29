# ====================================================================
#                       PROGRAMA DE SUMINISTRO
# ====================================================================

# Se definen todas las clases relacionadas con el programa de
# suministro: Accion, AccionProgramada (y subclases) y
# ProgramaDeSuministro.

# ====================================================================
# Accion


class Accion:
    """Una acción es aquello que puede ejecutarse en el contexto de un
    Ejecutor, o sea, ser ejecutador por un Ejecutor. Todas las
    acciones se definen con una cantidad de suministro, la magnitud
    empleada dependerá de qué tipo de acción se trata (una acción de
    regado requerirá una magnitud líquida, mientras que una acción de
    luz requerirá una magnitud de luz, etc). Cada tipo de acción es
    una subclase de Accion.

    """
    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def ejecutarEn(self, ejecutor):
        """Ejecuta la acción en el contexto de un Ejecutor.

        """
        raise NotImplementedError("Método abstracto")

    def cantidad(self):
        """Obtiene la cantidad de suministro. Es una instancia de alguna
        magnitud, según el tipo de acción.

        """
        # como protocolo interno de subclases, asumimos que todas
        # deben tener su variable miembro '_cantidad'
        return self._cantidad


class AccionRegado(Accion):
    """Una acción de regado. Su cantidad es una magnitud líquida.
    """
    def __init__(self, cantidadLiquido):
        self._cantidad = cantidadLiquido

    def ejecutarEn(self, ejecutor):
        ejecutor.ejecutarRegado(self.cantidad())


class AccionAntibiotico(Accion):
    """Una acción de aplicación de antibiótico. Su cantidad es una
    magnitud líquida.

    """
    def __init__(self, cantidadLiquido):
        self._cantidad = cantidadLiquido

    def ejecutarEn(self, ejecutor):
        ejecutor.ejecutarAntibiotico(self.cantidad())


class AccionFertilizante(Accion):
    """Una acción de aplicación de fertilizante. Su cantidad es una
    magnitud líquida.

    """
    def __init__(self, cantidadFertilizante):
        self._cantidad = cantidadFertilizante

    def ejecutarEn(self, ejecutor):
        ejecutor.ejecutarFertilizante(self.cantidad())


class AccionLuz(Accion):
    """Una acción de aplicación de luz. Su cantidad es una magnitud
    líquida.

    """
    def __init__(self, cantidadLuz):
        self._cantidad = cantidadLuz

    def ejecutarEn(self, ejecutor):
        ejecutor.ejecutarAntibiotico(self.cantidad())


# ====================================================================
# Accion programada

# NOTICE: Esta clase es más bien de uso interno del programa de
# suministro. En esta versión se expone bastante de esto hacia afuera,
# pero lo ideal tal vez sería que el usuario no cree instancias de
# esta clase y que simplemente se limite a usar 'accionProgramada()'
# de ProgramaDeSuministro, proyevendo el horario y la acción (el
# programa de suministro se encargará de ensamblarlas internamente).
# Si se sigue este consejo, tampoco debería usarse el constructor de
# lista. Por ahora queda a discresión del usuario.

class AccionProgramada:
    def __init__(self, fechaYHora, accion):
        """Crea una acción programada a partir de un horario y una acción.

        """
        self._tupla = (fechaYHora, accion)

    def fechaYHora(self):
        return self._tupla[0]

    def accion(self):
        return self._tupla[1]

    # operadores :

    def __lt__(self, otro):
        return self.fechaYHora() < otro.fechaYHora()

    def __le__(self, otro):
        return self.fechaYHora() <= otro.fechaYHora()

    def __eq__(self, otro):
        return self._tupla == otro._tupla

    def __ne__(self, otro):
        return not self.__eq__(otro)

    def __hash__(self):
        return self._tupla.__hash__()


# ====================================================================
# ProgramaDeSuministro

# NOTICE: Esta versión de 'ProgramaDeSuministro' es en realidad mucho
# más general que lo que el nombre indica, ya que lo único que
# interesa es que haya "eventos" programados a "horarios" (y lo único
# que realmente se exige es que los "horarios" puedan formar rangos,
# es decir que sean comparables con "<="). Por lo tanto puede
# construirse una instancia a partir de una lista como
# [(1,"uno"),(2,"dos"),(3,"tres")] para el rango 'Rango(1,3)' por
# ejemplo, y responderse a 'accionesEnHorario(Rango(1,2))'.
#
# Una alternativa es renombrarlo todo y llamarlo 'Cronograma' y
# cambiar el nombre de 'accionProgramada' a otra cosa
# ('eventoProgramado' por ejemplo, o ni siquiera tener tal clase y
# hacerlo totalmente interno, eso simplificaría las cosas). Pero por
# ahora no parece haber otros usos de esta clase, así que por ahora no
# está tan mal supongo.
#
# -- xol (28/09/2014)

class ProgramaDeSuministro:
    """Un programa de suministro es un cronograma de acciones programadas.
    Sabe responder qué acciones caen en un lapso de tiempo dado. Se
    construye con un lapso dado, y opcionalmente una lista de acciones
    programadas, en su defecto la lista será vacía. En cualquier caso,
    siempre puede usarse el método 'programar()' para agregar una
    nueva tarea programada. La fecha y hora de cualquier acción
    programada debe caer en el lapso indicado). La variante
    'programarAccion()' permite proveer directamente el horario y la
    acción, sin requerir construir un argumento de tipo
    AccionProgramada. El programa de suministro es un mero cronograma,
    y no es responsable de la ejecución de sus tareas programadas.

    """

    def __init__(self, lapso, lista=None):
        """Crea un programa de suministros abarcando el lapso dado, puede
        opcionalmente proveerse una lista de acciones programadas (si
        se omite, la lista interna de tareas programadas será vacía)

        """
        self._lapso = lapso
        self._accionesProgramadas = []

        if lista is not None:
            for accionProgramada in lista:
                self.programar(accionProgramada)

    def programar(self, accionProgramada):
        """Agrega una acción programada a la lista de acciones programadas. La
        fecha y hora de la acción programada debe estar en el lapso
        del programa de suministros.

        """
        assert(self.lapso().contiene(accionProgramada.fechaYHora()))
        self._accionesProgramadas.append(accionProgramada)

    def programarAccion(self, fechaYHora, accion):
        """Alternativa a programar(), toma el horario y la acción como
        argumentos separados. Si es posible, preferir esto a
        programar(), así el llamador se evita la necesidad de
        pasar una AccionProgramada.

        """
        self.programar(AccionProgramada(fechaYHora, accion))

    def lapso(self):
        """Retorna el lapso de validez del programa de suministro"""
        return self._lapso

    def accionesProgramadas(self):
        """Retorna la lista de acciones programadas. La lista está ordenada de
        menor a mayor según el horario de las acciones programadas.

        """
        return sorted(self._accionesProgramadas)

    def accionesEnHorario(self, lapso, remover=False):
        """Determina qué acciones programadas caen en un lapso dado. El
        resultado es una lista (sin ningún orden particular). Se puede
        especificar si se desea o no remover las acciones programadas
        (por ejemplo porque van a ser ejecutadas y por lo tanto no
        tiene sentido que permanezcan en el cronograma).

        """
        # un while sería más eficiente. sigh.
        if not self.lapso().interseca(lapso):
            return []  # meh, optimización
        acciones = [aP.accion() for aP in self.accionesProgramadas()
                    if lapso.contiene(aP.fechaYHora())]

        if remover:
            r = [aP for aP in self._accionesProgramadas
                 if aP.accion() not in acciones]
            self._accionesProgramadas = r
            # contamos con la comparación por default para las
            # acciones programadas, es decir la que utiliza 'id',
            # eso alcanza.
        return acciones
