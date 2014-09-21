#coding=utf-8

from icherry.tiempo import *


class PronosticoMeteorologico():

    def __init__(self, listaDePredicciones):
        self.__predicciones = list(listaDePredicciones)
        self.__predicciones = sorted(self.__predicciones, key = lambda p: p.intervalo().desdeFechaYHora())

    def fechaInicio(self):
        return self.__predicciones[0].intervalo().desdeFechaYHora()

    def fechaFin(self):
        return self.__predicciones[-1].intervalo().hastaFechaYHora()

    def prediccionPara(self, unaFechaYHora):
        for p in self.__predicciones:
            if p.intervalo().contieneFechaYHora(unaFechaYHora):
                return p
        ValueError("la fecha {0} no se encuentra en el rando de este pronostico".format(unaFechaYHora))


#Indica las predicciones de distintos parametros para el intervalo de tiempo dado.
class PrediccionMeteorologica():

    def __init__(self, intervalo, unaTemperatura, unaProbabilidadDeLluvia, unaHumedad, unaLuz):
        self.__intervalo = intervalo
        self.__probabilidadDeLLuvia = unaProbabilidadDeLluvia
        self.__humedad = unaHumedad
        self.__temperatura = unaTemperatura
        self.__luzAmbiente = unaLuz

    def intervalo(self):
        return self.__intervalo

    def probabilidadDeLluvia(self):
        return self.__probabilidadDeLLuvia

    def humedad(self):
        return self.__humedad

    def temperatura(self):
        return self.__temperatura

    def luzAmbiente(self):
        return self.__luzAmbiente


class CentralMeteorologica():
    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def obtenerFechaYHora(self):
        raise NotImplementedError("Método abstracto")

    def obtenerPronostico(self, unaCantidadDeHoras):
        raise NotImplementedError("Método abstracto")



class CentralMeteorologicaUSB(CentralMeteorologica):
    def __init__(self, unPuertoUSB):
        pass

    def obtenerFechaYHora(self):
        pass

    def obtenerPronostico(self, unaCantidadDeHoras):
        pass
