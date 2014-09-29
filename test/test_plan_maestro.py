import unittest

from icherry.magnitudes import Rango
from icherry.magnitudes import HumedadRelativa, Porcentaje
from icherry.magnitudes import TemperaturaEnCelsius, AcidezEnPH
from icherry.plan_maestro import EstadiosFenologicos
from icherry.plan_maestro import UmbralOptimoDeCultivo, PlanMaestro


class TestPlanMaestro(unittest.TestCase):

    def test_chequea_que_esten_todos_los_estadios_fenologicos_definidos(self):
        self.assertEqual(EstadiosFenologicos.germinacion().nombre(), 'GERMINACION')
        self.assertEqual(EstadiosFenologicos.desarrollo().nombre(), 'DESARROLLO')
        self.assertEqual(EstadiosFenologicos.brotes().nombre(), 'BROTES')
        self.assertEqual(EstadiosFenologicos.aparicion().nombre(), 'APARICION')
        self.assertEqual(EstadiosFenologicos.floracion().nombre(), 'FLORACION')
        self.assertEqual(EstadiosFenologicos.fruto().nombre(), 'FRUTO')
        self.assertEqual(EstadiosFenologicos.maduracion().nombre(), 'MADURACION')
        self.assertEqual(EstadiosFenologicos.senescencia().nombre(), 'SENESCENCIA')

    def setUp(self):
        def humedadRelativa(x):
            return HumedadRelativa(Porcentaje(x))

        e0 = EstadiosFenologicos.germinacion()
        e1 = EstadiosFenologicos.desarrollo()
        e2 = EstadiosFenologicos.brotes()
        e3 = EstadiosFenologicos.aparicion()
        e4 = EstadiosFenologicos.floracion()
        e5 = EstadiosFenologicos.fruto()
        e6 = EstadiosFenologicos.maduracion()
        e7 = EstadiosFenologicos.senescencia()

        self.estadios = [e0, e1, e2, e3, e4, e5, e6, e7]

        temperatura = Rango(TemperaturaEnCelsius(10), TemperaturaEnCelsius(30))
        humedad = Rango(humedadRelativa(40), humedadRelativa(50))
        acidez = Rango(AcidezEnPH(6.5), AcidezEnPH(7.5))
        self.umbral0 = UmbralOptimoDeCultivo(e0, temperatura, humedad, acidez)

        temperatura = Rango(TemperaturaEnCelsius(12), TemperaturaEnCelsius(20))
        humedad = Rango(humedadRelativa(40), humedadRelativa(70))
        acidez = Rango(AcidezEnPH(6.0), AcidezEnPH(7.5))
        self.umbral1 = UmbralOptimoDeCultivo(e1, temperatura, humedad, acidez)

        temperatura = Rango(TemperaturaEnCelsius(12), TemperaturaEnCelsius(20))
        humedad = Rango(humedadRelativa(40), humedadRelativa(70))
        acidez = Rango(AcidezEnPH(6.0), AcidezEnPH(7.5))
        self.umbral2 = UmbralOptimoDeCultivo(e2, temperatura, humedad, acidez)

        temperatura = Rango(TemperaturaEnCelsius(12), TemperaturaEnCelsius(20))
        humedad = Rango(humedadRelativa(40), humedadRelativa(70))
        acidez = Rango(AcidezEnPH(6.0), AcidezEnPH(7.5))
        self.umbral3 = UmbralOptimoDeCultivo(e3, temperatura, humedad, acidez)

        temperatura = Rango(TemperaturaEnCelsius(12), TemperaturaEnCelsius(20))
        humedad = Rango(humedadRelativa(40), humedadRelativa(70))
        acidez = Rango(AcidezEnPH(6.0), AcidezEnPH(7.5))
        self.umbral4 = UmbralOptimoDeCultivo(e4, temperatura, humedad, acidez)

        temperatura = Rango(TemperaturaEnCelsius(12), TemperaturaEnCelsius(20))
        humedad = Rango(humedadRelativa(40), humedadRelativa(70))
        acidez = Rango(AcidezEnPH(6.0), AcidezEnPH(7.5))
        self.umbral5 = UmbralOptimoDeCultivo(e5, temperatura, humedad, acidez)

        temperatura = Rango(TemperaturaEnCelsius(12), TemperaturaEnCelsius(20))
        humedad = Rango(humedadRelativa(40), humedadRelativa(70))
        acidez = Rango(AcidezEnPH(6.0), AcidezEnPH(7.5))
        self.umbral6 = UmbralOptimoDeCultivo(e6, temperatura, humedad, acidez)

        temperatura = Rango(TemperaturaEnCelsius(12), TemperaturaEnCelsius(20))
        humedad = Rango(humedadRelativa(40), humedadRelativa(70))
        acidez = Rango(AcidezEnPH(6.0), AcidezEnPH(7.5))
        self.umbral7 = UmbralOptimoDeCultivo(e7, temperatura, humedad, acidez)

        self.umbrales = [self.umbral0, self.umbral1, self.umbral2,
                         self.umbral3, self.umbral4, self.umbral5,
                         self.umbral6, self.umbral7]

        self.plan = PlanMaestro(self.umbrales)

    def aux_chequea_un_plan_maestro_que_tenga_todo_definido(self, planMaestro):
        self.assertEqual(planMaestro.umbralParaEstadio(self.estadios[0]), self.umbral0)
        self.assertEqual(planMaestro.umbralParaEstadio(self.estadios[1]), self.umbral1)
        self.assertEqual(planMaestro.umbralParaEstadio(self.estadios[2]), self.umbral2)
        self.assertEqual(planMaestro.umbralParaEstadio(self.estadios[3]), self.umbral3)
        self.assertEqual(planMaestro.umbralParaEstadio(self.estadios[4]), self.umbral4)
        self.assertEqual(planMaestro.umbralParaEstadio(self.estadios[5]), self.umbral5)
        self.assertEqual(planMaestro.umbralParaEstadio(self.estadios[6]), self.umbral6)
        self.assertEqual(planMaestro.umbralParaEstadio(self.estadios[7]), self.umbral7)

    def test_chequea_un_plan_maestro_que_tenga_todo_definido(self):
        self.aux_chequea_un_plan_maestro_que_tenga_todo_definido(self.plan)

    @unittest.expectedFailure
    def test_debe_fallar_ante_un_plan_maestro_con_menos_items(self):
        umbrales2 = [self.umbral0, self.umbral1, self.umbral2, self.umbral3,
                     self.umbral4, self.umbral5, self.umbral6]

        plan2 = PlanMaestro(umbrales2)
        # debe tirar excepción
        self.aux_chequea_un_plan_maestro_que_tenga_todo_definido(self.plan)
