import unittest
import datetime

from icherry.magnitudes import *
from icherry.tiempo import *
from icherry.central_meteorologica import *


#TODO completar
class TestCentralMeteorologica(unittest.TestCase):

    def test_central_meteorologica_devuelve_pronostico(self):
        pass

    def test_central_meteorologica_devuelve_fechaYHora(self):
        pass


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
        desdeLapso = FechaYHora(datetime.date(2014, 9, 20), datetime.time(10, 45, 50))
        hastaLapso = FechaYHora(datetime.date(2014, 9, 20), datetime.time(13, 45, 50))
        prediccion = PrediccionMeteorologica(Rango(desdeLapso, hastaLapso),
                                             TemperaturaEnCelsius(25),
                                             Porcentaje(40),
                                             HumedadRelativa(Porcentaje(10)),
                                             LuzEnLux(800))

        self.assertEqual(Rango(desdeLapso, hastaLapso), prediccion.lapso())
        self.assertEqual(TemperaturaEnCelsius(25), prediccion.temperatura())
        self.assertEqual(Porcentaje(40), prediccion.probabilidadDeLluvia())
        self.assertEqual(HumedadRelativa(Porcentaje(10)), prediccion.humedad())
        self.assertEqual(LuzEnLux(800), prediccion.luzAmbiente())
