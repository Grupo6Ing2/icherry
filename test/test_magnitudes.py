# coding=utf-8
from icherry.magnitudes import LiquidoEnLitros, LiquidoEnMililitros
from icherry.magnitudes import LuzEnLux
from icherry.magnitudes import TemperaturaEnCelsius, TemperaturaEnFahrenheit
from icherry.magnitudes import AcidezEnPH
from icherry.magnitudes import Porcentaje
from icherry.magnitudes import HumedadRelativa
from icherry.magnitudes import LongitudEnCentimetros
from icherry.magnitudes import Rango

import unittest


# abreviatura
def litros(numero):
    return LiquidoEnLitros(numero)


# abreviatura
def mililitros(numero):
    return LiquidoEnMililitros(numero)


class TestLiquido(unittest.TestCase):
    def test_conversion_litros_mililitros(self):
        self.assertEqual(litros(1.5), mililitros(1500))
        self.assertEqual(mililitros(500), litros(0.5))

    def test_comparadores(self):
        self.assertLess         (mililitros(10), mililitros(11))
        self.assertGreater      (mililitros(20), mililitros(10))
        self.assertGreaterEqual (mililitros(20), mililitros(10))
        self.assertGreaterEqual (mililitros(20), mililitros(20))
        self.assertLessEqual    (mililitros(20), mililitros(20))
        self.assertLessEqual    (mililitros(10), mililitros(20))
        self.assertEqual        (litros(10), litros(10))
        self.assertNotEqual     (litros(10), litros(11))

    @unittest.expectedFailure
    def test_comparar_liquido_con_luz_explota(self):
        # debe tirar excepción
        LiquidoEnLitros(1) == LuzEnLux(1)


class TestLuzEnLux(unittest.TestCase):
    def test_comparadores(self):
        self.assertLess         (LuzEnLux(10), LuzEnLux(11))
        self.assertGreater      (LuzEnLux(20), LuzEnLux(10))
        self.assertGreaterEqual (LuzEnLux(20), LuzEnLux(10))
        self.assertGreaterEqual (LuzEnLux(20), LuzEnLux(20))
        self.assertLessEqual    (LuzEnLux(20), LuzEnLux(20))
        self.assertLessEqual    (LuzEnLux(10), LuzEnLux(20))
        self.assertEqual        (LuzEnLux(10), LuzEnLux(10))
        self.assertNotEqual     (LuzEnLux(10), LuzEnLux(11))

    @unittest.expectedFailure
    def test_comparar_luz_con_temperatura_explota(self):
        # debe tirar excepción
        LuzEnLux(20) == TemperaturaEnCelsius(16)


# abreviatura
def celsius(numero):
    return TemperaturaEnCelsius(numero)


# abreviatura
def fahrenheit(numero):
    return TemperaturaEnFahrenheit(numero)


class TestTemperatura(unittest.TestCase):
    def test_conversion_celsius_fahrenheit(self):
        self.assertEqual(celsius(0), fahrenheit(32))
        self.assertEqual(fahrenheit(68), celsius(20))

    def test_comparadores(self):
        self.assertLess         (celsius(10), celsius(11))
        self.assertGreater      (celsius(20), celsius(10))
        self.assertGreaterEqual (celsius(20), celsius(10))
        self.assertGreaterEqual (celsius(20), celsius(20))
        self.assertLessEqual    (celsius(20), celsius(20))
        self.assertLessEqual    (celsius(10), celsius(20))
        self.assertEqual        (fahrenheit(10), fahrenheit(10))
        self.assertNotEqual     (fahrenheit(10), fahrenheit(11))

    @unittest.expectedFailure
    def test_comparar_temperatura_con_liquido_explota(self):
        # debe tirar excepción
        TemperaturaEnFahrenheit(5) == LiquidoEnLitros(5)


class TestPH(unittest.TestCase):
    def test_comparadores(self):
        self.assertLess         (AcidezEnPH(10), AcidezEnPH(11))
        self.assertGreater      (AcidezEnPH(11), AcidezEnPH(10))
        self.assertGreaterEqual (AcidezEnPH(11), AcidezEnPH(10))
        self.assertGreaterEqual (AcidezEnPH(11), AcidezEnPH(11))
        self.assertLessEqual    (AcidezEnPH(11), AcidezEnPH(11))
        self.assertLessEqual    (AcidezEnPH(10), AcidezEnPH(11))
        self.assertEqual        (AcidezEnPH(10), AcidezEnPH(10))
        self.assertNotEqual     (AcidezEnPH(10), AcidezEnPH(11))

    @unittest.expectedFailure
    def test_comparar_ph_con_porcentaje_explota(self):
        # debe tirar excepción
        LuzEnLux(5) == Porcentaje(16)

    @unittest.expectedFailure
    def test_ph_fuera_de_limite_inferior(self):
        AcidezEnPH(-1)          # debe tirar excepción

    @unittest.expectedFailure
    def test_ph_fuera_de_limite_superior(self):
        AcidezEnPH(14.5)        # debe tirar excepción


class TestPorcentaje(unittest.TestCase):
    def test_comparadores(self):
        self.assertLess         (Porcentaje(10), Porcentaje(11))
        self.assertGreater      (Porcentaje(11), Porcentaje(10))
        self.assertGreaterEqual (Porcentaje(11), Porcentaje(10))
        self.assertGreaterEqual (Porcentaje(11), Porcentaje(11))
        self.assertLessEqual    (Porcentaje(11), Porcentaje(11))
        self.assertLessEqual    (Porcentaje(10), Porcentaje(11))
        self.assertEqual        (Porcentaje(10), Porcentaje(10))
        self.assertNotEqual     (Porcentaje(10), Porcentaje(11))

    @unittest.expectedFailure
    def test_comparar_porcentaje_con_liquido_explota(self):
        # debe tirar excepción
        Porcentaje(50) == LiquidoEnLitros(100)

    @unittest.expectedFailure
    def test_porcentaje_fuera_de_limite_inferior(self):
        Porcentaje(-1)          # debe tirar excepción

    @unittest.expectedFailure
    def test_porcentaje_fuera_de_limite_superior(self):
        Porcentaje(101)         # debe tirar excepción


def humedad(numero):
    # dado un número entre 1 y 100, construye una humedad relativa,
    # para ahorrar verbosidad, nomás.
    return HumedadRelativa(Porcentaje(numero))


class TestHumedadRelativa(unittest.TestCase):
    def test_comparadores(self):
        self.assertLess         (humedad(10), humedad(11))
        self.assertGreater      (humedad(11), humedad(10))
        self.assertGreaterEqual (humedad(11), humedad(10))
        self.assertGreaterEqual (humedad(11), humedad(11))
        self.assertLessEqual    (humedad(11), humedad(11))
        self.assertLessEqual    (humedad(10), humedad(11))
        self.assertEqual        (humedad(10), humedad(10))
        self.assertNotEqual     (humedad(10), humedad(11))

    @unittest.expectedFailure
    def test_comparar_humedad_con_porcentaje_explota(self):
        humedad(50) == Porcentaje(50)  # debe tirar excepción

    @unittest.expectedFailure
    def test_valor_de_humedad_relativa_no_es_numero(self):
        h = humedad(57)       # una humedad
        h.valor() == 57         # debe tirar excepción

    def test_valor_de_humedad_relativa_es_ratio(self):
        h = humedad(66)             # una humedad
        p = h.valor().aPorcentaje()  # extraemos el porcentaje
        v = p.valor()                # extraemos el número
        self.assertEqual(v, 66)


class TestLongitudCentimetros(unittest.TestCase):
    def test_valor_centimetros(self):
        l = LongitudEnCentimetros(100)
        self.assertEqual(l.valor(), 100)

    def test_igualdad_centimetros(self):
        l1 = LongitudEnCentimetros(100)
        l2 = LongitudEnCentimetros(100)
        self.assertEqual(l1, l2)


class TestRango(unittest.TestCase):
    def chk_eje(self, rx, ry):
        self.assertTrue(rx.interseca(ry))

    def chk_no_eje(self, rx, ry):
        self.assertFalse(rx.interseca(ry))

    def test_rango_interseccion(self):
        # Este test está basado en la idea de un grafo de intervalos
        # (cada vértice representa un intervalo, dos vertices son
        # adyacentes si y sólo si los intervalos respectivos se
        # intersecan).

        #     0--1--2--3--4--5--6--7--8--9
        # r1        |--------|
        # r2     |-----|
        # r3              |--------|
        # r4  |-----------------------|
        # r5                    |--------|
        #
        # dibujito del grafo:
        #
        # r1------------r3
        # | -\       /- |
        # |   -\   /-   |
        # |     -\/     |
        # |      r4-----r5
        # |   /--
        # | /-
        # r2

        # Armamos el grafo y verificamos todas las combinaciones
        # posibles de cada par de vértices. Esto hace un test
        # exhaustivo de todo el grafo (verifica tanto los pares
        # adyacentes como los no adyacentes).
        r1, r2, r3, r4, r5 = Rango(2, 5), Rango(1, 3), Rango(4, 7), Rango(0, 8), Rango(6, 9)
        vertices = {r1, r2, r3, r4, r5}
        r1.__ady = {r2, r3, r4}
        r2.__ady = {r1, r4}
        r3.__ady = {r1, r4, r5}
        r4.__ady = {r1, r2, r3, r5}
        r5.__ady = {r3, r4}
        for v in vertices:
            self.chk_eje(v, v)  # reflexividad
            for w in v.__ady:   # adyacencia dirigida
                self.chk_eje(v, w)
            for w in ((vertices - v.__ady) - {v}):  # no-adyacencia dirigida
                self.chk_no_eje(v, w)
