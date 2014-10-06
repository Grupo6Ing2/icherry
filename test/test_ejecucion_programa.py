from icherry.tiempo import FechaYHora, DuracionEnMinutos, DuracionEnHoras
from icherry.magnitudes import Rango, LiquidoEnMililitros, LuzEnLux
from icherry.actuadores import Actuador
from icherry.programa_suministro import ProgramaDeSuministro, AccionRegado, AccionLuz
from icherry.programa_suministro import AccionFertilizante, AccionAntibiotico
from icherry.ejecucion_programa import PlanificadorDeEjecucion, EjecutorDeAccion

from datetime import date, time
import unittest


class Deposito:
    def __init__(self):
        self.reset()

    def __getitem__(self, item):
        return self._depo[item]

    def __setitem__(self, item, valor):
        self._depo[item] = valor

    def reset(self):
        self._depo = {'luz': 0, 'agua': 0, 'antibiotico': 0, 'fertilizante': 0}


class ActuadorMock(Actuador):

    def __init__(self, deposito, tipo):
        super().__init__()
        self._deposito = deposito
        self._tipo = tipo

    def aplicar(self, magnitud):
        self._deposito[self._tipo] += magnitud.valor()


class KitEjecucion():

    def __init__(self):
        self.depo = Deposito()
        self.actuadorLuz = ActuadorMock(self.depo, 'luz')
        self.actuadorRegado = ActuadorMock(self.depo, 'agua')
        self.actuadorAntibiotico = ActuadorMock(self.depo, 'antibiotico')
        self.actuadorFertilizante = ActuadorMock(self.depo, 'fertilizante')
        self.ejecutor = EjecutorDeAccion(self.actuadorRegado, self.actuadorAntibiotico,
                                         self.actuadorLuz, self.actuadorFertilizante)

    def ejecutar(self, accion):
        self.ejecutor.ejecutarAccion(accion)

    # eso sí, las magnitudes tienen que ser siempre de la misma unidad
    # para cada magnitud, porque en el depósito almacenamos números
    # planos, no magnitudes. Así que atenti con qué fruta metés.
    def agua(self):
        return self.depo['agua']

    def antibiotico(self):
        return self.depo['antibiotico']

    def luz(self):
        return self.depo['luz']

    def fertilizante(self):
        return self.depo['fertilizante']


class TestEjecutorDeAccion(unittest.TestCase):

    def setUp(self):
        self.depo = Deposito()
        self.actuadorLuz = ActuadorMock(self.depo, 'luz')
        self.actuadorRegado = ActuadorMock(self.depo, 'agua')
        self.actuadorAntibiotico = ActuadorMock(self.depo, 'antibiotico')
        self.actuadorFertilizante = ActuadorMock(self.depo, 'fertilizante')

    def test_las_acciones_se_ejecutan(self):
        accionRegado = AccionRegado(LiquidoEnMililitros(400))
        accionFertilizante = AccionFertilizante(LiquidoEnMililitros(100))
        accionAntibiotico = AccionAntibiotico(LiquidoEnMililitros(20))
        accionLuz = AccionLuz(LuzEnLux(1000))

        cantidadAgua = accionRegado.cantidad().valor()
        cantidadLuz = accionLuz.cantidad().valor()
        cantidadFertilizante = accionFertilizante.cantidad().valor()
        cantidadAntibiotico = accionAntibiotico.cantidad().valor()

        kit = KitEjecucion()

        self.assertEqual(kit.agua(), 0)
        kit.ejecutar(accionRegado)
        self.assertEqual(kit.agua(), cantidadAgua)
        kit.ejecutar(accionRegado)
        self.assertEqual(kit.agua(), 2 * cantidadAgua)

        self.assertEqual(kit.luz(), 0)
        kit.ejecutar(accionLuz)
        self.assertEqual(kit.luz(), cantidadLuz)
        kit.ejecutar(accionLuz)
        self.assertEqual(kit.luz(), 2 * cantidadLuz)

        self.assertEqual(kit.fertilizante(), 0)
        kit.ejecutar(accionFertilizante)
        self.assertEqual(kit.fertilizante(), cantidadFertilizante)
        kit.ejecutar(accionFertilizante)
        self.assertEqual(kit.fertilizante(), 2 * cantidadFertilizante)

        self.assertEqual(kit.antibiotico(), 0)
        kit.ejecutar(accionAntibiotico)
        self.assertEqual(kit.antibiotico(), cantidadAntibiotico)
        kit.ejecutar(accionAntibiotico)
        self.assertEqual(kit.antibiotico(), 2 * cantidadAntibiotico)

        self.assertEqual(kit.fertilizante(), 2 * cantidadFertilizante)
        self.assertEqual(kit.luz(), 2 * cantidadLuz)
        self.assertEqual(kit.agua(), 2 * cantidadAgua)


class TestPlanificadorDeEjecucion(unittest.TestCase):
    def setUp(self):
        # self.kit =

        # self.planificador = PlanificadorDeEjecucion(
        #     DuracionEnHoras(1), programa, kit )
        pass

    def test_planificador_planifica_ejecucion_hora_por_hora(self):
        hora = FechaYHora(date(1998, 7, 10), time(17, 0, 0))
        kit = KitEjecucion()

        # inicializamos un programa de suministro vacío
        programa = ProgramaDeSuministro(
            Rango(hora, hora.agregarDuracion(DuracionEnHoras(3))))

        # programamos las acciones que entran en la primer hora
        programa.programarAccion(hora.agregarDuracion(DuracionEnMinutos(15)),
                                 AccionRegado(LiquidoEnMililitros(200)))
        programa.programarAccion(hora.agregarDuracion(DuracionEnMinutos(20)),
                                 AccionLuz(LuzEnLux(800)))
        programa.programarAccion(hora.agregarDuracion(DuracionEnMinutos(35)),
                                 AccionFertilizante(LiquidoEnMililitros(100)))
        programa.programarAccion(hora.agregarDuracion(DuracionEnMinutos(40)),
                                 AccionRegado(LiquidoEnMililitros(20)))
        programa.programarAccion(hora.agregarDuracion(DuracionEnMinutos(50)),
                                 AccionAntibiotico(LiquidoEnMililitros(10)))
        # programamos las acciones que entran en la segunda hora
        programa.programarAccion(hora.agregarDuracion(DuracionEnMinutos(75)),
                                 AccionRegado(LiquidoEnMililitros(100)))
        programa.programarAccion(hora.agregarDuracion(DuracionEnMinutos(90)),
                                 AccionLuz(LuzEnLux(500)))
        # programamos las acciones que entran en la tercer hora
        programa.programarAccion(hora.agregarDuracion(DuracionEnMinutos(130)),
                                 AccionAntibiotico(LiquidoEnMililitros(10)))

        # ok, está cargado el programa. Creamos entonces el
        # planificador, lo configuramos para que ejecute sobre el kit
        # con el programa dado a intervalos de una hora. Obviamente no
        # hay temporizadores acá así que vamos a llamarlo manualmente
        # por cada hora.

        planificador = PlanificadorDeEjecucion(
            DuracionEnHoras(1), programa, kit.ejecutor)

        # WARNING. los números están clavados. si se cambian arriba,
        # deben cambiarse acá abajo (sumando todo con cuidado).

        # ejecutamos la primer hora
        cuantasAntes = len(programa.accionesProgramadas())
        planificador.planificarAcciones(hora)
        self.assertEqual(kit.fertilizante(), 100)
        self.assertEqual(kit.luz(), 800)
        self.assertEqual(kit.agua(), 220)
        self.assertEqual(kit.antibiotico(), 10)
        cuantasDespues = len(programa.accionesProgramadas())
        self.assertEqual(cuantasAntes - cuantasDespues, 5)

        # ejecutamos la segunda hora
        cuantasAntes = len(programa.accionesProgramadas())
        planificador.planificarAcciones(hora.agregarDuracion(DuracionEnHoras(1)))
        self.assertEqual(kit.fertilizante(), 100 + 0)
        self.assertEqual(kit.luz(), 800 + 500)
        self.assertEqual(kit.agua(), 220 + 100)
        self.assertEqual(kit.antibiotico(), 10 + 0)
        cuantasDespues = len(programa.accionesProgramadas())
        self.assertEqual(cuantasAntes - cuantasDespues, 2)

        # ejecutamos la tercer hora
        cuantasAntes = len(programa.accionesProgramadas())
        planificador.planificarAcciones(hora.agregarDuracion(DuracionEnHoras(2)))
        self.assertEqual(kit.fertilizante(), 100 + 0 + 0)
        self.assertEqual(kit.luz(), 800 + 500 + 0)
        self.assertEqual(kit.agua(), 220 + 100 + 0)
        self.assertEqual(kit.antibiotico(), 10 + 0 + 10)
        cuantasDespues = len(programa.accionesProgramadas())
        self.assertEqual(cuantasAntes - cuantasDespues, 1)

        # verificamos que el programa esté vacío
        self.assertEqual(programa.accionesProgramadas(), [])
