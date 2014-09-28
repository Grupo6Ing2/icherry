# coding=utf-8
from icherry.magnitudes import Porcentaje, TemperaturaEnCelsius
from icherry.magnitudes import HumedadRelativa, LuzEnLux, Rango
from icherry.tiempo import FechaYHora
from icherry.central_meteorologica import PronosticoMeteorologico
from icherry.central_meteorologica import PrediccionMeteorologica
import datetime


class Parser():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def parse(unObjeto):
        raise NotImplementedError("Método abstracto")


class CadenaANumero(Parser):

    def __init__(self):
        pass

    def parse(self, unaCadena):
        return float(unaCadena)


class CadenaAPorcentaje(Parser):

    def __init__(self):
        pass

    def parse(self, unaCadena):
        return Porcentaje(int(unaCadena))


class CadenaAFechaYHora(Parser):

    def __init__(self):
        pass

    def parse(self, unaCadena):
        fecha = datetime.datetime.strptime(
            unaCadena.split()[0], "%Y-%m-%d").date()
        hora = datetime.datetime.strptime(
            unaCadena.split()[1], "%H:%M:%S.%f").time()
        return FechaYHora(fecha, hora)


class ParserPronosticoMeteorologico(Parser):

    def __init__(self):
        pass

    # Devuelve un PronosticoMeteorologico
    def parse(self, unaCadena):
        # El formato es:
        # desdeLapso
        # hastaLapso
        # temp
        # lluvia
        # humedad
        # luz
        # desdeLapso
        #...
        predicciones = []

        datosSerializados = unaCadena.split("\n")
        for i in range(0, len(datosSerializados) - 1, 6):
            desde = CadenaAFechaYHora().parse(datosSerializados[i])
            hasta = CadenaAFechaYHora().parse(datosSerializados[i + 1])
            temp = TemperaturaEnCelsius(
                CadenaANumero().parse(datosSerializados[i + 2]))
            lluvia = CadenaAPorcentaje().parse(datosSerializados[i + 3])
            humedad = HumedadRelativa(
                CadenaAPorcentaje().parse(datosSerializados[i + 4]))
            luz = LuzEnLux(CadenaANumero().parse(datosSerializados[i + 5]))

            predicciones.append(PrediccionMeteorologica(
                Rango(desde, hasta), temp, lluvia, humedad, luz))

        return PronosticoMeteorologico(predicciones)


class MagnitudACadena(Parser):

    def __init__(self):
        pass

    def parse(self, unaMagnitud):
        return str(unaMagnitud.valor())
