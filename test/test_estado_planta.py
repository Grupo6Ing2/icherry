from icherry.estado_planta import EstadoDePlanta, EstadoFenologico
from icherry.estado_planta import EstadoDeSaludBueno, EstadoDeSaludMalo
from icherry.plan_maestro import EstadioGerminacion, EstadioFloracion
from icherry.magnitudes import Porcentaje, LongitudEnCentimetros, AcidezEnPH
from icherry.magnitudes import TemperaturaEnCelsius, HumedadRelativa

import unittest


class TestEstadoFenologico(unittest.TestCase):
    def test_estadoFenologico_se_inicializa_en_cero_y_estadio_germinacion(self):
        """Inicializa un estado fenológico, deberían estar todos los
        parámetros numéricos en cero (el porcentaje tiene valor() 0),
        y el estadio de cultivo debería ser el de germinación (es el
        primer estadio de cualquier plan maestro).

        """
        x = EstadoFenologico()
        self.assertEqual(x.cantidadBrotes(), 0)
        self.assertEqual(x.cantidadFlores(), 0)
        self.assertEqual(x.cantidadFrutos(), 0)
        self.assertEqual(x.porcentajeFrutasMaduras(), Porcentaje(0))
        self.assertEqual(x.estadioDeCultivo(), EstadioGerminacion)
        self.assertEqual(x.altura(), LongitudEnCentimetros(0))

    def test_estadoFenologico_puede_modificarse_correctamente(self):
        """verificamos que los setters efectivamente modifiquen los valores
        como corresponde. De paso verificamos que los métodos
        funcionen bien tanto como getters y setters.

        """
        x = EstadoFenologico()
        x.cantidadBrotes(3)
        self.assertEqual(x.cantidadBrotes(), 3)
        x.cantidadFlores(2)
        self.assertEqual(x.cantidadFlores(), 2)
        x.porcentajeFrutasMaduras(20)
        self.assertEqual(x.porcentajeFrutasMaduras(), 20)
        x.estadioDeCultivo(EstadioFloracion)
        self.assertEqual(x.estadioDeCultivo(), EstadioFloracion)
        x.altura(LongitudEnCentimetros(20))
        self.assertEqual(x.altura(), LongitudEnCentimetros(20))


class TestPlanta(unittest.TestCase):
    def test_planta_puede_modificarse_correctamente(self):
        x = EstadoDePlanta()
        x.temperatura(TemperaturaEnCelsius(15))
        self.assertEqual(x.temperatura(), TemperaturaEnCelsius(15))
        x.humedad(HumedadRelativa(Porcentaje(30)))
        self.assertEqual(x.humedad(), HumedadRelativa(Porcentaje(30)))
        x.acidez(AcidezEnPH(6.66))
        self.assertEqual(x.acidez(), AcidezEnPH(6.66))


class TestEstadoSalud(unittest.TestCase):
    def test_estadoSalud_notifica_correctamente(self):

        class NotificadoMock():
            def __init__(self):
                self.estado = 'BUENO'

            def notificarseEstadoBueno(self):
                self.estado = 'BUENO'

            def notificarseEstadoMalo(self):
                self.estado = 'MALO'

        n = NotificadoMock()
        for e in [EstadoDeSaludBueno, EstadoDeSaludMalo]:
            e.notificarEstadoA(n)
            self.assertEqual(n.estado, e.nombre())
