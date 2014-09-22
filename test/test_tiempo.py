import unittest
import datetime

from icherry.magnitudes import Rango
from icherry.tiempo import FechaYHora, DuracionEnSegundos

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


class TestDuracionEnSegundos(unittest.TestCase):

    def test_duracion_representada_en_segundos_es_correcta(self):
        duracion = DuracionEnSegundos(110)

        self.assertEqual(110, duracion.enSegundos())
