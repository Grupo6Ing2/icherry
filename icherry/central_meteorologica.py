# coding=utf-8

from icherry.magnitudes import Rango
from icherry.observer import Observable
import icherry.parsers


class PronosticoMeteorologico():

    def __init__(self, listaDePredicciones):
        self.__predicciones = sorted(listaDePredicciones,
                                     key=lambda p: p.lapso().desde())

    def fechaInicio(self):
        return self.__predicciones[0].lapso().desde()

    def fechaFin(self):
        return self.__predicciones[-1].lapso().hasta()

    def prediccionPara(self, unaFechaYHora):
        for p in self.__predicciones:
            if p.lapso().contiene(unaFechaYHora):
                return p
        raise ValueError("la fecha {0} no está en el rango de este pronóstico"
                         .format(unaFechaYHora))

    def __eq__(self, otroPronostico):
        return self.__predicciones == otroPronostico.__predicciones

    def __ne__(self, otroPronostico):
        return not self.__eq__(otroPronostico)

    def __str__(self):
        return str(self.__predicciones)


# Indica las predicciones de distintos parámetros para el lapso dado.
class PrediccionMeteorologica():

    def __init__(self, lapso, unaTemperatura,
                 unaProbabilidadDeLluvia, unaHumedad, unaLuz):
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
            self.__probabilidadDeLLuvia == \
            otraPrediccion.__probabilidadDeLLuvia and \
            self.__humedad == otraPrediccion.__humedad and \
            self.__temperatura == otraPrediccion.__temperatura and \
            self.__luzAmbiente == otraPrediccion.__luzAmbiente

    def __ne__(self, otraPrediccion):
        return not self.__eq__(otraPrediccion)

    def __str__(self):
        return ('Prediccion para {4} es: \nTemperatura: {0}, Humedad: {1}, '
                'Prob. de lluvia: {2}, Luz ambiente: {3}').format(
                    self.temperatura(),
                    self.humedad(),
                    self.probabilidadDeLluvia(),
                    self.luzAmbiente(),
                    self.lapso())

    def __repr__(self):
        return self.__str__()


class ProveedorDeTiempo():
    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def fechaYHoraActual(self):
        raise NotImplementedError("Método abstracto")


class PredictorMeteorologico():
    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    # Devuelve una PrediccionMeteorologica para el lapso especificado.
    def prediccionPara(self, unLapso):
        raise NotImplementedError("Método abstracto")


class CentralMeteorologica(Observable):
    def __init__(self, predictorMeteorologico, proveedorDeTiempo):
        super().__init__()

        self.__proveedorDeTiempo = proveedorDeTiempo
        self.__predictorMeteorologico = predictorMeteorologico
        self.__ultimoPronostico = None

    def obtenerFechaYHora(self):
        self.notificarObservers()
        return self.__proveedorDeTiempo.fechaYHoraActual()

    def obtenerPronostico(self, desdeFechaYHora, cantidadDeHs):
        predicciones = []
        desde = desdeFechaYHora

        for i in range(cantidadDeHs):
            hasta = desde.agregarHoras(1)
            predicciones.append(self.__predictorMeteorologico.prediccionPara(
                Rango(desde, hasta)))
            desde = desde.agregarHoras(1)

        self.__ultimoPronostico = PronosticoMeteorologico(predicciones)
        self.notificarObservers()
        return self.__ultimoPronostico

    def ultimoPronostico(self):
        return self.__ultimoPronostico


# Clases usadas para la demo. Leen los datos de los archivos.
class PredictorMeteorologicoPorArchivo(PredictorMeteorologico):

    def __init__(self, dispositivoDeLectura):
        parser = icherry.parsers.ParserPronosticoMeteorologico()
        pronostico = parser.parse(dispositivoDeLectura.leer())
        self.__pronostico = pronostico

    def prediccionPara(self, unLapso):
        return self.__pronostico.prediccionPara(unLapso.desde())


class ProveedorDeTiempoPorArchivo(ProveedorDeTiempo):
    def __init__(self, dispositivoDeLectura):
        self.__dispositivoDeLectura = dispositivoDeLectura

    def fechaYHoraActual(self):
        return icherry.parsers.CadenaAFechaYHora().parse(
            self.__dispositivoDeLectura.leer())
