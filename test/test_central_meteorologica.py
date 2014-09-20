import unittest
import datetime

from icherry.magnitudes import Porcentaje,TemperaturaEnCelsius,HumedadRelativa,LuzEnLux
from icherry.app import ProveedorDeDatosMeteorologicos
from icherry.app import CentralMeteorologica
from icherry.app import Periodo

class ProveedorDeDatosMeteorologicosSimulado(ProveedorDeDatosMeteorologicos):

    def __init__(self):
        pass

    def probabilidadDeLLuviaPronosticada(self, periodo):
        return Porcentaje(50)

    def humedadPronosticada(self, periodo):
        return HumedadRelativa(Porcentaje(10))

    def temperaturaPronosticada(self, periodo):
        return TemperaturaEnCelsius(18)

    def luzAmbientePronosticada(self, periodo):
        return LuzEnLux(10)


#TODO completar
class TestCentralMeteorologica(unittest.TestCase):

    def test_central_meteorologica_devuelve_pronostico(self):
        proveedor = ProveedorDeDatosMeteorologicosSimulado()
        central = CentralMeteorologica(proveedor)
        #TODO: Tal vez conviene reemplazar las fechas por nuestras clases, ademas deberian
        #incluir el tiempo
        periodo = Periodo(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1))
        pronostico = central.armarPronostico(periodo)

        self.assertEqual(Porcentaje(50), pronostico.probabilidadDeLluvia())
        self.assertEqual(HumedadRelativa(Porcentaje(10)), pronostico.humedad())
        self.assertEqual(TemperaturaEnCelsius(18), pronostico.temperatura())
        self.assertEqual(LuzEnLux(10), pronostico.luzAmbiente())
        self.assertEqual(periodo, pronostico.periodo())



if __name__ == '__main__':
    unittest.main()
