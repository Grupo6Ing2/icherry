#coding=utf-8

import datetime

#Un intervalo de tiempo
class Intervalo():

    def __init__(self, desdeFechaYHora, hastaFechaYHora):
        if hastaFechaYHora < desdeFechaYHora:
            raise ValueError("desdeFechaYHora tiene que ser anterior a hastaFechaYHora")

        self.__desde = desdeFechaYHora
        self.__hasta = hastaFechaYHora

    def desdeFechaYHora(self):
        return self.__desde

    def hastaFechaYHora(self):
        return self.__hasta

    def contieneFechaYHora(self, unaFechaYHora):
        return self.desdeFechaYHora() <= unaFechaYHora <= self.hastaFechaYHora()

    def __eq__(self, otroIntervalo):
        return self.desdeFechaYHora() == otroIntervalo.desdeFechaYHora() and \
            self.hastaFechaYHora() == otroIntervalo.hastaFechaYHora()


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

    def __str__(self):
        return "{0} {1}".format(fecha(), hora())


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
