#coding=utf-8

class FechaYHora():

    #unDate: instancia de timedate.date
    #unTime: instancia de timedate.time
    def __init__(self, unDate, unTime):
        self.__date = unDate
        self.__time = unTime

    #Devuelve una instancia de timedate.date
    def fecha(self):
        return self.__date

    #Devuelve una instancia de timedate.time
    def hora(self):
        return self.__time

    def __lt__(self, otraFechaYHora):
        return self.fecha() < otraFechaYHora.fecha() or \
            (self.fecha() == otraFechaYHora.fecha() and self.hora() < otraFechaYHora.hora())

    def __le__(self, otraFechaYHora):
        return self < otraFechaYHora or self == otraFechaYHora

    def __eq__(self, otraFechaYHora):
        return self.fecha() == otraFechaYHora.fecha() and\
                self.hora() == otraFechaYHora.hora()

    # WARNING: ojo con definir '__eq__' sin definir '__ne__', el "!="
    # no hace lo que esperarías.
    def __ne__(self, otraFechaYHora):
        return not self.__eq__(otraFechaYHora)

    def __str__(self):
        return "{0} {1}".format(self.fecha(), self.hora())


#Representa una duracion de tiempo. Las subclases indican las unidades en las que se
#expresa la duracion.
class Duracion():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def enSegundos(self):
        raise NotImplementedError("Método abstracto")


class DuracionEnSegundos(Duracion):

    def __init__(self, segundos):
        self.__segundos = segundos

    def enSegundos(self):
        return self.__segundos
