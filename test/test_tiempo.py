import unittest
import datetime

from icherry.magnitudes import Rango
from icherry.tiempo import FechaYHora
from icherry.tiempo import DuracionEnSegundos,DuracionEnMinutos,DuracionEnHoras

class TestFechaYHora(unittest.TestCase):

    def test_fechaYHora_se_instancia_bien(self):
        fechaYHora = FechaYHora(datetime.date(2014, 9, 21), datetime.time(10, 45, 50))

        self.assertEqual(datetime.date(2014, 9, 21), fechaYHora.fecha())
        self.assertEqual(datetime.time(10, 45, 50), fechaYHora.hora())

    def test_dos_instancias_iguales_son_iguales(self):
        unaFecha = FechaYHora(datetime.date(2014, 9, 21), datetime.time(10, 45, 50))
        otraFecha = FechaYHora(datetime.date(2014, 9, 21), datetime.time(10, 45, 50))

        self.assertEqual(unaFecha, otraFecha)

    def test_dos_instancias_con_fechas_no_iguales_no_son_iguales(self):
        unaFecha = FechaYHora(datetime.date(2014, 9, 21), datetime.time(10, 45, 50))
        otraFecha = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 50))

        self.assertNotEqual(unaFecha, otraFecha)

    def test_dos_instancias_con_horas_no_iguales_no_son_iguales(self):
        unaFecha = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 55))
        otraFecha = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 50))

        self.assertNotEqual(unaFecha, otraFecha)

    def test_comparacion_por_menor_es_correcta(self):
        unaFecha = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 55))
        otraFecha = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 50))
        self.assertLess(otraFecha, unaFecha)

        unaFecha = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 50))
        otraFecha = FechaYHora(datetime.date(2014, 9, 20), datetime.time(10, 45, 50))
        self.assertLess(otraFecha, unaFecha)

        unaFecha = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 55))
        otraFecha = FechaYHora(datetime.date(2014, 9, 20), datetime.time(10, 45, 50))
        self.assertLess(otraFecha, unaFecha)

        unaFecha = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 55))
        otraFecha = FechaYHora(datetime.date(2014, 9, 20), datetime.time(13, 45, 55))
        self.assertLess(otraFecha, unaFecha)



class TestLapso(unittest.TestCase):
    #NOTICE: en este test ya queda testeada la funcionalidad del Rango.

    def test_lapso_se_instancia_bien(self):
        desde = FechaYHora(datetime.date(2014, 9, 21), datetime.time(10, 45, 50))
        hasta = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 50))
        lapso = Rango(desde, hasta)

        self.assertEqual(desde, lapso.desde())
        self.assertEqual(hasta, lapso.hasta())

    def test_dos_lapsos_iguales_son_iguales(self):
        desde1 = FechaYHora(datetime.date(2014, 9, 21), datetime.time(10, 45, 50))
        hasta1 = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 50))
        lapso1 = Rango(desde1, hasta1)

        desde2 = FechaYHora(datetime.date(2014, 9, 21), datetime.time(10, 45, 50))
        hasta2 = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 50))
        lapso2 = Rango(desde2, hasta2)

        self.assertTrue(lapso1 == lapso2)

    def test_lapso_contiene_fechaYHora_contenida_en_el_lapso(self):
        desde = FechaYHora(datetime.date(2014, 9, 21), datetime.time(10, 45, 50))
        hasta = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 50))
        lapso = Rango(desde, hasta)

        unaFechaYHora = FechaYHora(datetime.date(2014, 9, 21), datetime.time(12, 45, 50))

        self.assertTrue(lapso.contiene(unaFechaYHora))

    def test_lapso_no_contiene_fechaYHora_no_contenida_en_el_lapso(self):
        desde = FechaYHora(datetime.date(2014, 9, 21), datetime.time(10, 45, 50))
        hasta = FechaYHora(datetime.date(2014, 9, 22), datetime.time(10, 45, 50))
        lapso = Rango(desde, hasta)

        unaFechaYHora = FechaYHora(datetime.date(2014, 9, 25), datetime.time(12, 45, 50))
        self.assertFalse(lapso.contiene(unaFechaYHora))

        unaFechaYHora = FechaYHora(datetime.date(2014, 9, 15), datetime.time(12, 45, 50))
        self.assertFalse(lapso.contiene(unaFechaYHora))


class TestDuracion(unittest.TestCase):
    def setUp(self):
        # las tres duraciones son equivalentes al convertir, todas
        # equivalen a media hora. La idea es ver que los valores
        # numéricos se obtengan bien y que las conversiones en todos
        # los sentidos posibles estén bien.
        self.segundos = 1800
        self.minutos  = 30
        self.horas    = 0.5

    def verificarIgualdades(self,segundos,minutos,horas):
        #verifica que todas las duraciones sean iguales y que sus
        #valores puedan obtenerse correctamente
        self.assertEqual(segundos         , minutos)
        self.assertEqual(segundos         , horas)
        self.assertEqual(segundos.valor() , self.segundos)
        self.assertEqual(minutos.valor()  , self.minutos)
        self.assertEqual(horas.valor()    , self.horas)

    def test_segundos_se_convierten_correctamente(self) :
        segundos = DuracionEnSegundos(self.segundos)
        minutos  = segundos.aMinutos()
        horas    = segundos.aHoras()
        self.verificarIgualdades(segundos,minutos,horas)

    def test_minutos_se_convierten_correctamente(self) :
        minutos  = DuracionEnMinutos(self.minutos)
        segundos = minutos.aSegundos()
        horas    = minutos.aHoras()
        self.verificarIgualdades(segundos,minutos,horas)

    def test_horas_se_convierten_correctamente(self) :
        horas    = DuracionEnHoras(self.horas)
        segundos = horas.aSegundos()
        minutos  = horas.aMinutos()
        self.verificarIgualdades(segundos,minutos,horas)
