# coding=utf-8

import icherry.dispositivos as dispositivos
import icherry.parsers as parsers
from icherry.observer import Observable


class Actuador(Observable):

    def __init__(self):
        super().__init__()

    def aplicar(self, unaMagnitud):
        raise NotImplementedError("Método abstracto")


class ActuadorEnArchivo(Actuador):

    def __init__(self, unDispositivoDeEscritura, unParserACadena):
        super().__init__()

        self._dispositivo = unDispositivoDeEscritura
        self._parser = unParserACadena

    def aplicar(self, unaMagnitud):
        self._dispositivo.escribir(self._parser.parse(unaMagnitud))


class ConstructorDeActuadorEnArchivo():

    def crear(self, unNombreArchivo):
        return ActuadorEnArchivo(
            dispositivos.DispositivoDeEscrituraArchivo(unNombreArchivo),
            parsers.MagnitudACadena()
        )
