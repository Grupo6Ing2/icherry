import unittest
import datetime

from icherry.tiempo import FechaYHora
from icherry.parsers import CadenaAFechaYHora, ParserPronosticoMeteorologico
from icherry.magnitudes import *
from icherry.central_meteorologica import *

class TestParserFechaYHora(unittest.TestCase):

    def test_fechaYHora_se_parsea(self):
        s = '2014-09-27 11:18:31.0'
        result = CadenaAFechaYHora().parse(s)
        self.assertEqual(FechaYHora(datetime.date(2014, 9, 27), datetime.time(11, 18, 31)), result)


class TestParserPronosticoMeteorologico(unittest.TestCase):

    def test_pronosticoMeteorologico_se_parse(self):
        s = ("2014-09-27 11:00:0.0\n"
            "2014-09-27 11:59:59.0\n"
            "20\n"
            "55\n"
            "60\n"
            "1010\n"
            "2014-09-27 12:00:00.0\n"
            "2014-09-27 12:59:59.0\n"
            "25\n"
            "50\n"
            "65\n"
            "1020\n")

        result = ParserPronosticoMeteorologico().parse(s)

        prediccionesEsperadas = [
            PrediccionMeteorologica(
                Rango(FechaYHora(datetime.date(2014, 9, 27), datetime.time(11, 0, 0)),
                  FechaYHora(datetime.date(2014, 9, 27), datetime.time(11, 59, 59))),
                TemperaturaEnCelsius(20),
                Porcentaje(55),
                HumedadRelativa(Porcentaje(60)),
                LuzEnLux(1010)),
            PrediccionMeteorologica(
                Rango(FechaYHora(datetime.date(2014, 9, 27), datetime.time(12, 0, 0)),
                  FechaYHora(datetime.date(2014, 9, 27), datetime.time(12, 59, 59))),
                TemperaturaEnCelsius(25),
                Porcentaje(50),
                HumedadRelativa(Porcentaje(65)),
                LuzEnLux(1020)),
        ]
        expected = PronosticoMeteorologico(prediccionesEsperadas)

        self.assertEqual(expected, result)

