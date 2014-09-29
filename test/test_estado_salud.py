from icherry.estado_salud import EstadoDeSalud, EstadoFenologico
from icherry.plan_maestro import EstadiosFenologicos
from icherry.magnitudes import Porcentaje, LongitudEnCentimetros, AcidezEnPH
from icherry.magnitudes import TemperaturaEnCelsius, HumedadRelativa

import unittest

class TestEstadoFenologico(unittest.TestCase):
    def test_estadoFenologico_se_inicializa_en_cero_y_estadio_germinacion(self):
        """inicializamos un estado fenologico, deberian estar todos los
        parametros numericos en cero (el porcentaje tiene valor() 0),
        y el estadio de cultivo deberia ser el de germinacion (es el
        primer estadio de cualquier plan maestro).

        """
        x = EstadoFenologico()
        self.assertEqual(x.cantidadBrotes(), 0)
        self.assertEqual(x.cantidadFlores(), 0)
        self.assertEqual(x.cantidadFrutos(), 0)
        self.assertEqual(x.porcentajeFrutasMaduras(), Porcentaje(0))
        self.assertEqual(x.estadioDeCultivo(), EstadiosFenologicos.germinacion())
        self.assertEqual(x.altura(), LongitudEnCentimetros(0))

    def test_estadoFenologico_puede_modificarse_correctamente(self):
        """verificamos que los setters efectivamente modifiquen los valores
        como corresponde. De paso verificamos que los metodos
        funcionen bien tanto como getters y setters.

        """
        x = EstadoFenologico()
        x.cantidadBrotes(3)
        self.assertEqual(x.cantidadBrotes(), 3)
        x.cantidadFlores(2)
        self.assertEqual(x.cantidadFlores(), 2)
        x.porcentajeFrutasMaduras(20)
        self.assertEqual(x.porcentajeFrutasMaduras(), 20)
        x.estadioDeCultivo(EstadiosFenologicos.floracion())
        self.assertEqual(x.estadioDeCultivo(), EstadiosFenologicos.floracion())
        x.altura(LongitudEnCentimetros(20))
        self.assertEqual(x.altura(), LongitudEnCentimetros(20))

class TestEstadoSalud(unittest.TestCase):
    def test_estadoDeSalud_puede_modificarse_correctamente(self):
        x = EstadoDeSalud(EstadoFenologico())
        x.temperatura(TemperaturaEnCelsius(15))
        self.assertEqual(x.temperatura(), TemperaturaEnCelsius(15))
        x.humedad(HumedadRelativa(Porcentaje(30)))
        self.assertEqual(x.humedad(), HumedadRelativa(Porcentaje(30)))
        x.acidez(AcidezEnPH(6.66))
        self.assertEqual(x.acidez(), AcidezEnPH(6.66))
