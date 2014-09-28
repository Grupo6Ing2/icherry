# coding=utf-8

from icherry.central_meteorologica import CentralMeteorologica
from icherry.central_meteorologica import PronosticoMeteorologico


class AmbienteSimulado():
    pass


class CentralMeteorologicaSimulada(CentralMeteorologica):
    def __init__(self, unAmbienteSimulado):
        self.__ambiente = unAmbienteSimulado

    def obtenerFechaYHora(self):
        return self.__ambiente.fechaYHora()

    def obtenerPronostico(self, unaCantidadDeHoras):
        # TODO
        return PronosticoMeteorologico(None)
