import unittest

from icherry.sensores import Sensor
from icherry.parsers import CadenaANumero
from icherry.dispositivos import DispositivoDeLectura
from icherry.magnitudes import LuzEnLux


class DispositivoDeLecturaMock(DispositivoDeLectura):
    def __init__(self, valor):
        self.valor = valor

    def leer(self):
        return self.valor


class TestSensor(unittest.TestCase):

    def test_sensar(self):
        dispositivo = DispositivoDeLecturaMock('42')
        parser = CadenaANumero()
        sensor = Sensor(dispositivo, parser, LuzEnLux)

        self.assertIsNone(sensor.ultimoValorSensado())

        resultado = sensor.sensar()

        self.assertIsNotNone(sensor.ultimoValorSensado())
        self.assertEqual(LuzEnLux(42), sensor.ultimoValorSensado())
        self.assertEqual(LuzEnLux(42), resultado)
