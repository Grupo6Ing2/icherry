import unittest

from icherry.magnitudes import Rango
from icherry.magnitudes import HumedadRelativa, Porcentaje
from icherry.magnitudes import TemperaturaEnCelsius, AcidezEnPH
from icherry.plan_maestro import EstadiosFenologicos
from icherry.plan_maestro import UmbralOptimoDeCultivo, PlanMaestro


class TestPlanMaestro(unittest.TestCase):

    def setUp(self):
        def humedadRelativa(x):
            return HumedadRelativa(Porcentaje(x))

        self.e0 = EstadiosFenologicos.germinacion()
        self.e1 = EstadiosFenologicos.desarrollo()
        self.e2 = EstadiosFenologicos.brotes()
        self.e3 = EstadiosFenologicos.aparicion()
        self.e4 = EstadiosFenologicos.floracion()
        self.e5 = EstadiosFenologicos.fruto()
        self.e6 = EstadiosFenologicos.maduracion()
        self.e7 = EstadiosFenologicos.senescencia()

        self.estadios = [self.e0, self.e1, self.e2, self.e3,
                         self.e4, self.e5, self.e6, self.e7]

        # argumentos para ensamblar los umbrales. Modificar a gusto.
        args = [[10, 30, 40, 50, 6.5, 7.5]] + [[12, 20, 40, 70, 6.0, 7.5]]*7
        x = [10, 30, 40, 50, 6.5, 7.5]

        # armamos los umbrales para cada estadio a partir de las
        # listas de argumentos
        self.umbrales = []
        for i in range(len(self.estadios)):
            x = args[i]
            temperatura = Rango(TemperaturaEnCelsius(x[0]),
                                TemperaturaEnCelsius(x[1]))
            humedad = Rango(humedadRelativa(x[2]),
                            humedadRelativa(x[3]))
            acidez = Rango(AcidezEnPH(x[4]), AcidezEnPH(x[5]))
            self.umbrales.append(UmbralOptimoDeCultivo(
                self.estadios[i], temperatura, humedad, acidez))

        # la lista de los nombres esperados para los estadios
        self.nombres = ['GERMINACION', 'DESARROLLO', 'BROTES', 'APARICION',
                        'FLORACION', 'FRUTO', 'MADURACION', 'SENESCENCIA']

    def test_chequea_que_esten_todos_los_estadios_fenologicos_definidos(self):
        for i in range(len(self.nombres)):
            self.assertEqual(self.estadios[i].nombre(), self.nombres[i])

    def aux_chequea_un_plan_maestro_que_tenga_todo_definido(self, planMaestro):
        for i in range(len(self.estadios)):
            self.assertEqual(planMaestro.umbralParaEstadio(self.estadios[i]),
                             self.umbrales[i])

    def test_chequea_un_plan_maestro_que_tenga_todo_definido(self):
        umbrales = self.umbrales
        plan = PlanMaestro(umbrales)
        self.aux_chequea_un_plan_maestro_que_tenga_todo_definido(plan)

    @unittest.expectedFailure
    def test_debe_fallar_ante_un_plan_maestro_con_menos_items(self):
        umbrales = [self.umbral4, self.umbral5, self.umbral6]  # no están todos
        plan = PlanMaestro(umbrales)
        # debe tirar excepción
        self.aux_chequea_un_plan_maestro_que_tenga_todo_definido(plan)
