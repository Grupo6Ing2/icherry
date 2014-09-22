#coding=utf-8

from icherry.tiempo import *


class PronosticoMeteorologico():

    def __init__(self, listaDePredicciones):
        self.__predicciones = list(listaDePredicciones)
        self.__predicciones = sorted(self.__predicciones, key = lambda p: p.lapso().desde())

    def fechaInicio(self):
        return self.__predicciones[0].lapso().desde()

    def fechaFin(self):
        return self.__predicciones[-1].lapso().hasta()

    def prediccionPara(self, unaFechaYHora):
        for p in self.__predicciones:
            if p.lapso().contiene(unaFechaYHora):
                return p
        raise ValueError("la fecha {0} no se encuentra en el rango de este pronóstico"
                         .format(unaFechaYHora))


#Indica las predicciones de distintos parámetros para el lapso dado.
class PrediccionMeteorologica():

    def __init__(self, lapso, unaTemperatura, unaProbabilidadDeLluvia, unaHumedad, unaLuz):
        self.__lapso = lapso
        self.__probabilidadDeLLuvia = unaProbabilidadDeLluvia
        self.__humedad = unaHumedad
        self.__temperatura = unaTemperatura
        self.__luzAmbiente = unaLuz

    def lapso(self):
        return self.__lapso

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
