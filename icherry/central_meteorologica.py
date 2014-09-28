# coding=utf-8

from icherry.magnitudes import Rango


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

    def __eq__(self, otroPronostico):
        return self.__predicciones == otroPronostico.__predicciones

    def __ne__(self, otroPronostico):
        return not self.__eq__(otroPronostico)


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

    def __eq__(self, otraPrediccion):
        return self.__lapso == otraPrediccion.__lapso and \
            self.__probabilidadDeLLuvia == otraPrediccion.__probabilidadDeLLuvia and \
            self.__humedad == otraPrediccion.__humedad and \
            self.__temperatura == otraPrediccion.__temperatura and \
            self.__luzAmbiente == otraPrediccion.__luzAmbiente

    def __ne__(self, otraPrediccion):
        return not self.__eq__(otraPrediccion)

    def __str__(self):
        return ('Prediccion para {4} es: \nTemperatura: {0}, Humedad: {1}, '
                  'Prob. de lluvia: {2}, Luz ambiente: {3}').format(self.temperatura(),
                                                                    self.humedad(),
                                                                    self.probabilidadDeLluvia(),
                                                                    self.luzAmbiente(),
                                                                    self.lapso())


class ProveedorDeTiempo():
    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def fechaYHoraActual(self):
        raise NotImplementedError("Metodo abstracto")


class PredictorMeteorologico():
    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    #Devuelve una PrediccionMeteorologica para el lapso especificado.
    def prediccionPara(self, unLapso):
        raise NotImplementedError("Metodo abstracto")


class CentralMeteorologica():
    def __init__(self, predictorMeteorologico, proveedorDeTiempo):
        self.__proveedorDeTiempo = proveedorDeTiempo
        self.__predictorMeteorologico = predictorMeteorologico

    def obtenerFechaYHora(self):
        return self.__proveedorDeTiempo.fechaYHoraActual()

    def obtenerPronostico(self, desdeFechaYHora, cantidadDeHs):
        predicciones = []
        desde = desdeFechaYHora

        for i in range(cantidadDeHs):
            hasta = desde.agregarHoras(1)
            predicciones.append(self.__predictorMeteorologico.prediccionPara(Rango(desde, hasta)))
            desde = desde.agregarHoras(1)

        return PronosticoMeteorologico(predicciones)
