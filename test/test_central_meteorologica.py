import unittest
import datetime

from icherry.magnitudes import *
from icherry.app import *

class AmbienteSimulado():

    def __init__(self):
        pass

    def fechaYHora(self):
        #TODO
        return None


#TODO completar
class TestCentralMeteorologica(unittest.TestCase):

    def test_central_meteorologica_devuelve_pronostico(self):

        central = CentralMeteorologicaSimulada(AmbienteSimulado())
        unPronosticoMeteorologico = central.obtenerPronostico(24)

        #TODO completar cuando FechaYHora este lista

        #self.assertEqual(..., pronostico.fechaInicio())
        #self.assertEqual(..., pronostico.fechaFin())
        #self.assertIsNotNone(pronostico.prediccionPara(unaFechaYHoraEnRango))



    def test_central_meteorologica_devuelve_fechaYHora(self):

        central = CentralMeteorologicaSimulada(AmbienteSimulado())
        unaFechaYHora = central.obtenerFechaYHora()

#        TODO: testear que fechaYHora este bien.
#        self.assertEqual(...)


class TestPronosticoMeteorologico(unittest.TestCase):

    #TODO
    def test_pronostico_devuelve_predicciones(self):
        pass
        #self.assertEqual(..., pronostico.prediccionPara(otraFechaYHoraEnRango))
        #self.assertEqual(..., pronostico.prediccionPara(unaFechaYHoraFueraDelRango))


if __name__ == '__main__':
    unittest.main()
