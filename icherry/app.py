#coding=utf-8

#Un intervalo de tiempo
class Intervalo():

    def __init__(self, desdeFechaYHora, hastaFechaYHora):
        self.__desde = desdeFechaYHora
        self.__hasta = hastaFechaYHora

    def desdeFechaYHora(self):
        return self.__desde

    def hastaFechaYHora(self):
        return self.__hasta


#TODO
class PronosticoMeteorologico():

    def __init__(self, listaDePredicciones):
        self.__predicciones = listaDePredicciones

    def fechaInicio(self):
        pass

    def fechaFin(self):
        pass

    def prediccionPara(self, unaFechaYHora):
        pass


#Indica las predicciones de distintos parametros para el intervalo de tiempo dado.
class PrediccionMeteorologica():

    def __init__(self, intervalo, unaTemperatura, unaProbabilidadDeLluvia, unaHumedad, unaLuz):
        self.__intervalo = intervalo
        self.__probabilidadDeLLuvia = unaProbabilidadDeLluvia
        self.__humedad = unaHumedad
        self.__temperatura = unaTemperatura
        self.__luzAmbiente = unaLuz

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


class CentralMeteorologicaSimulada(CentralMeteorologica):
    def __init__(self, unAmbienteSimulado):
        self.__ambiente = unAmbienteSimulado

    def obtenerFechaYHora(self):
        return self.__ambiente.fechaYHora()

    def obtenerPronostico(self, unaCantidadDeHoras):
        #TODO
        return PronosticoMeteorologico(None)


class CentralMeteorologicaUSB(CentralMeteorologica):
    def __init__(self, unPuertoUSB):
        pass

    def obtenerFechaYHora(self):
        pass

    def obtenerPronostico(self, unaCantidadDeHoras):
        pass


class Aplicacion():
    def __init__(self, centralMeteorologica):
        self.__centralMeteorologica = centralMeteorologica

    def pronosticoSiguientes24Hs(self):
        pass
        #TODO: pasar parametros correctos a Periodo
        #return self.__centralMeteorologica.armarPronostico(Periodo(None, None))
