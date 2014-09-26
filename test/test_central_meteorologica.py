import unittest
import datetime

from icherry.magnitudes import *
from icherry.tiempo import *
from icherry.central_meteorologica import *


#TODO completar
class TestCentralMeteorologica(unittest.TestCase):


    def test_central_meteorologica_devuelve_pronostico(self):
        desde = FechaYHora(datetime.date(2014, 9, 21), datetime.time(10, 45, 50))
        hasta = FechaYHora(datetime.date(2014, 9, 21), datetime.time(12, 45, 50))
        predictor = PredictorMeteorologicoMock(TemperaturaEnCelsius(25),
                                             Porcentaje(40),
                                             HumedadRelativa(Porcentaje(10)),
                                             LuzEnLux(800))

        central = CentralMeteorologica(predictor, None)
        pronostico = central.obtenerPronostico(desdeFechaYHora=desde, cantidadDeHs=2)

        self.assertEqual(desde, pronostico.fechaInicio())
        self.assertEqual(hasta, pronostico.fechaFin())

        prediccion1 = pronostico.prediccionPara(
            FechaYHora(datetime.date(2014, 9, 21), datetime.time(11, 40, 50)))
        self.assertEqual(Rango(desde, desde.agregarHoras(1)), prediccion1.lapso())
        self.assertEqual(TemperaturaEnCelsius(25), prediccion1.temperatura())
        self.assertEqual(Porcentaje(40), prediccion1.probabilidadDeLluvia())
        self.assertEqual(HumedadRelativa(Porcentaje(10)), prediccion1.humedad())
        self.assertEqual(LuzEnLux(800), prediccion1.luzAmbiente())

        prediccion2 = pronostico.prediccionPara(
            FechaYHora(datetime.date(2014, 9, 21), datetime.time(12, 40, 50)))
        self.assertEqual(Rango(desde.agregarHoras(1), hasta), prediccion2.lapso())
        self.assertEqual(TemperaturaEnCelsius(25), prediccion2.temperatura())
        self.assertEqual(Porcentaje(40), prediccion2.probabilidadDeLluvia())
        self.assertEqual(HumedadRelativa(Porcentaje(10)), prediccion2.humedad())
        self.assertEqual(LuzEnLux(800), prediccion2.luzAmbiente())


    def test_central_meteorologica_devuelve_fechaYHora(self):
        fechaYHora = FechaYHora(datetime.date(2014, 9, 21), datetime.time(10, 45, 50))
        proveedorDeTiempo = ProveedorDeTiempoMock(fechaYHora)
        central = CentralMeteorologica(None, proveedorDeTiempo)
        self.assertEqual(fechaYHora, central.obtenerFechaYHora())


class ProveedorDeTiempoMock(ProveedorDeTiempo):
    def __init__(self, fechaYHora):
        self.fechaYHora = fechaYHora

    def fechaYHoraActual(self):
        return self.fechaYHora


class PredictorMeteorologicoMock(PredictorMeteorologico):
    def __init__(self, temp, lluvia, humedad, luz):
        self.__temp = temp
        self.__lluvia = lluvia
        self.__humedad = humedad
        self.__luz = luz

    def prediccionPara(self, unLapso):
        return PrediccionMeteorologica(unLapso, self.__temp, self.__lluvia, self.__humedad, self.__luz)



class TestPronosticoMeteorologico(unittest.TestCase):

    def setUp(self):
        self.desdeLapso1 = FechaYHora(datetime.date(2014, 9, 21), datetime.time(10, 45, 50))
        self.hastaLapso1 = FechaYHora(datetime.date(2014, 9, 21), datetime.time(13, 45, 50))
        self.desdeLapso2 = FechaYHora(datetime.date(2014, 9, 20), datetime.time(10, 45, 50))
        self.hastaLapso2 = FechaYHora(datetime.date(2014, 9, 20), datetime.time(13, 45, 50))

        self.prediccion1 = PrediccionMeteorologica(Rango(self.desdeLapso1, self.hastaLapso1),
                                             TemperaturaEnCelsius(20),
                                             Porcentaje(80),
                                             HumedadRelativa(Porcentaje(50)),
                                             LuzEnLux(1000))
        self.prediccion2 = PrediccionMeteorologica(Rango(self.desdeLapso2, self.hastaLapso2),
                                             TemperaturaEnCelsius(25),
                                             Porcentaje(40),
                                             HumedadRelativa(Porcentaje(10)),
                                             LuzEnLux(800))

    def test_fechaInicio_es_correcta(self):
        pronostico = PronosticoMeteorologico([self.prediccion1, self.prediccion2])
        self.assertEqual(self.desdeLapso2, pronostico.fechaInicio())

    def test_fechaFin_es_correcta(self):
        pronostico = PronosticoMeteorologico([self.prediccion1, self.prediccion2])
        self.assertEqual(self.hastaLapso1, pronostico.fechaFin())

    def test_prediccion_para_una_fecha_existente(self):
        pronostico = PronosticoMeteorologico([self.prediccion1, self.prediccion2])

        prediccion = pronostico.prediccionPara(
            FechaYHora(datetime.date(2014, 9, 21), datetime.time(11, 0, 0)))
        self.assertEqual(self.prediccion1, prediccion)

        prediccion = pronostico.prediccionPara(
            FechaYHora(datetime.date(2014, 9, 20), datetime.time(12, 0, 0)))
        self.assertEqual(self.prediccion2, prediccion)

    @unittest.expectedFailure
    def test_prediccion_para_una_fecha_no_existente(self):
        pronostico = PronosticoMeteorologico([self.prediccion1, self.prediccion2])

        prediccion = pronostico.prediccionPara(
            FechaYHora(datetime.date(2014, 9, 25), datetime.time(11, 0, 0)))


class TestPrediccionMeteorologica(unittest.TestCase):

    def test_prediccion_se_construye_correctamente(self):
        desde = FechaYHora(datetime.date(2014, 9, 20), datetime.time(10, 45, 50))
        hasta = FechaYHora(datetime.date(2014, 9, 20), datetime.time(13, 45, 50))
        prediccion = PrediccionMeteorologica(Rango(desde, hasta),
                                             TemperaturaEnCelsius(25),
                                             Porcentaje(40),
                                             HumedadRelativa(Porcentaje(10)),
                                             LuzEnLux(800))

        self.assertEqual(Rango(desde, hasta), prediccion.lapso())
        self.assertEqual(TemperaturaEnCelsius(25), prediccion.temperatura())
        self.assertEqual(Porcentaje(40), prediccion.probabilidadDeLluvia())
        self.assertEqual(HumedadRelativa(Porcentaje(10)), prediccion.humedad())
        self.assertEqual(LuzEnLux(800), prediccion.luzAmbiente())
