# ====================================================================
#                       PROGRAMA DE SUMINISTRO
# ====================================================================

# Se definen todas las clases relacionadas con el programa de
# suministro: Accion (y subclases), AccionProgramada y
# ProgramaDeSuministro.

# ====================================================================
# Accion

from icherry.observer import Observable


class Accion:
    """Una acción es aquello que puede ejecutarse en el contexto de un
    ejecutor, o sea, ser ejecutador por un EjecutorDeAccion. Todas
    las acciones se definen con una cantidad de suministro, la
    magnitud empleada dependerá de qué tipo de acción se trata (una
    acción de regado requerirá una magnitud líquida, mientras que una
    acción de luz requerirá una magnitud de luz, etc). Cada tipo de
    acción es una subclase de Accion.

    """
    def __init__(self, cantidad):
        raise NotImplementedError("Clase abstracta")

    def ejecutarEn(self, ejecutor):
        """Ejecuta la acción en el contexto de un EjecutorDeAccion.

        """
        raise NotImplementedError("Método abstracto")

    def nombre(self):
        """Retorna el nombre de la acción"""
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

    def nombre(self):
        return 'REGADO'


class AccionAntibiotico(Accion):
    """Una acción de aplicación de antibiótico. Su cantidad es una
    magnitud líquida.

    """
    def __init__(self, cantidadLiquido):
        self._cantidad = cantidadLiquido

    def ejecutarEn(self, ejecutor):
        ejecutor.ejecutarAntibiotico(self.cantidad())

    def nombre(self):
        return 'ANTIBIOTICO'


class AccionFertilizante(Accion):
    """Una acción de aplicación de fertilizante. Su cantidad es una
    magnitud líquida.

    """
    def __init__(self, cantidadFertilizante):
        self._cantidad = cantidadFertilizante

    def ejecutarEn(self, ejecutor):
        ejecutor.ejecutarFertilizante(self.cantidad())

    def nombre(self):
        return 'FERTILIZANTE'


class AccionLuz(Accion):
    """Una acción de aplicación de luz. Su cantidad es una magnitud de
    luz.

    """
    def __init__(self, cantidadLuz):
        self._cantidad = cantidadLuz

    def ejecutarEn(self, ejecutor):
        ejecutor.ejecutarLuz(self.cantidad())

    def nombre(self):
        return 'LUZ'


# ====================================================================
# Accion programada

class AccionProgramada:
    """Una acción programada es un par <FechaYHora, Accion> glorificado,
    con métodos de acceso. El programa de suministro tiene
    internamente una lista de instancias de esta clase.

    """
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

class ProgramaDeSuministro(Observable):
    """Un programa de suministro es un cronograma de acciones programadas.
    Sabe responder qué acciones caen en un lapso de tiempo dado. Se
    construye con un lapso, el cronograma será vacío. Puede usarse el
    método 'programar()' para agregar una nueva tarea programada. La
    fecha y hora de cualquier acción programada debe caer en el lapso
    indicado. La variante 'programarAccion()' permite proveer
    directamente el horario y la acción, sin requerir construir un
    argumento de tipo AccionProgramada. El programa de suministro es
    un mero cronograma, y no es responsable de la ejecución de sus
    tareas programadas. Es observable, pero no la actualización de los
    observadores no es responsabilidad del programa de suministro,
    debe llamarse a 'actualizar()' en forma externa.

    """

    def __init__(self, lapso):
        """Crea un programa de suministro abarcando el lapso dado. El
        programa está inicialmente vacío, y deberán programarse las
        tareas una por una.

        """
        super().__init__()

        self._lapso = lapso
        self._accionesProgramadas = []

    def vaciar(self):
        """Vacía el programa, dejándolo sin ninguna acción programada."""
        self._accionesProgramadas = []

    def copiar(self, otroPrograma):
        """Modifica al programa de suministro para que se vuelva una copia de
        otro programa de suministro. Se comparten los colaboradores internos."""
        self._lapso = otroPrograma._lapso
        self._accionesProgramadas = otroPrograma._accionesProgramadas

    def programar(self, accionProgramada):
        """Agrega una acción programada a la lista de acciones programadas. La
        fecha y hora de la acción programada debe estar en el lapso
        del programa de suministro.

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

    def accionesEnHorario(self, lapso):
        """Determina qué acciones programadas caen en un lapso dado. El
        resultado es una lista (sin ningún orden particular).

        """
        acciones = [aP.accion() for aP in self.accionesProgramadas()
                    if lapso.contiene(aP.fechaYHora())]

        return acciones

    def retirarAccionesEnHorario(self, lapso):
        """Variante de 'accionesEnHorario()', que adicionalmente retira las
        acciones programadas (por ejemplo porque van a ser ejecutadas
        y por lo tanto no tiene sentido que permanezcan en el
        cronograma).

        """

        accionesEnHorario = self.accionesEnHorario(lapso)
        self._accionesProgramadas = [aP for aP in self._accionesProgramadas
                                     if aP.accion() not in accionesEnHorario]

        return accionesEnHorario
