# coding=utf-8
import datetime

from icherry.magnitudes import Magnitud

# ====================================================================
# FechaYHora


class FechaYHora():

    # unDate: instancia de timedate.date
    # unTime: instancia de timedate.time
    def __init__(self, unDate, unTime):
        self.__date = unDate
        self.__time = unTime

    # Devuelve una instancia de timedate.date
    def fecha(self):
        return self.__date

    # Devuelve una instancia de timedate.time
    def hora(self):
        return self.__time

    def agregarHoras(self, cantHoras):
        delta = datetime.timedelta(hours=cantHoras)
        newDateTime = datetime.datetime.combine(
            self.__date, self.__time) + delta
        return FechaYHora(newDateTime.date(), newDateTime.time())

    @staticmethod
    def ahora():
        return FechaYHora(
            datetime.datetime.now().date(), datetime.datetime.now().time()
        )

    def __lt__(self, otraFechaYHora):
        return self.fecha() < otraFechaYHora.fecha() or \
            (self.fecha() == otraFechaYHora.fecha() and
             self.hora() < otraFechaYHora.hora())

    def __le__(self, otraFechaYHora):
        return self < otraFechaYHora or self == otraFechaYHora

    def __eq__(self, otraFechaYHora):
        return self.fecha() == otraFechaYHora.fecha() and\
            self.hora() == otraFechaYHora.hora()

    def __ne__(self, otraFechaYHora):
        return not self.__eq__(otraFechaYHora)

    def __str__(self):
        return "{0} {1}".format(self.fecha(), self.hora())


# ====================================================================
# Duracion

# Las duraciones son todas subclases 'compatibles' de Magnitud, con lo
# cual implementan el protocolo de conversiones, y pueden compararse y
# convertirse como cualquier otra magnitud. Ver magnitudes.py.

class Duracion(Magnitud):

    """Representa una duracion de tiempo. Las subclases indican las
    unidades en las que se expresa la duración.

    """

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def aSegundos(self):
        raise NotImplementedError("Método abstracto")

    def aMinutos(self):
        raise NotImplementedError("Método abstracto")

    def aHoras(self):
        raise NotImplementedError("Método abstracto")


class DuracionEnSegundos(Duracion):

    def __init__(self, segundos):
        self._valor = segundos

    def valor(self):
        return self._valor

    def aSegundos(self):
        return self

    def aMinutos(self):
        return DuracionEnMinutos(self.valor() / 60)

    def aHoras(self):
        return DuracionEnHoras(self.valor() / 3600)

    def _compatibilizar(self, otraMagnitud):
        return otraMagnitud.aSegundos()


class DuracionEnMinutos(Duracion):

    def __init__(self, minutos):
        self._valor = minutos

    def valor(self):
        return self._valor

    def aSegundos(self):
        return DuracionEnSegundos(self.valor() * 60)

    def aMinutos(self):
        return self

    def aHoras(self):
        return DuracionEnHoras(self.valor() / 60)

    def _compatibilizar(self, otraMagnitud):
        return otraMagnitud.aMinutos()


class DuracionEnHoras(Duracion):

    def __init__(self, horas):
        self._valor = horas

    def valor(self):
        return self._valor

    def aSegundos(self):
        return DuracionEnSegundos(self.valor() * 3600)

    def aMinutos(self):
        return DuracionEnMinutos(self.valor() * 60)

    def aHoras(self):
        return self

    def _compatibilizar(self, otraMagnitud):
        return otraMagnitud.aHoras()
