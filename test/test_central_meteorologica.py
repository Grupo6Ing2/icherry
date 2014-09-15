import unittest
import datetime

from icherry.app import *


class ProveedorDeDatosMeteorologicosSimulado(ProveedorDeDatosMeteorologicos):

    def __init__(self):
        pass

    def probabilidadDeLLuviaPronosticada(self, periodo):
        return Porcentaje(50)

    def humedadPronosticada(self, periodo):
        return Porcentaje(10)

    def temperaturaPronosticada(self, periodo):
        return 1 #TODO: usar un objeto temperatura

    def luzAmbientePronosticada(self, periodo):
        return Lux(10)


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
        self.assertEqual(Porcentaje(10), pronostico.humedad())
        #TODO: comparar las temperaturas
        pronostico.temperatura()
        self.assertEqual(Lux(10), pronostico.luzAmbiente())
        self.assertEqual(periodo, pronostico.periodo())



if __name__ == '__main__':
    unittest.main()
