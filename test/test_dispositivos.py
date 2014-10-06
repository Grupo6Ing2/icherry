from icherry.dispositivos import DispositivoDeEscrituraArchivo
from icherry.dispositivos import DispositivoDeLecturaArchivo

import unittest
from random import random


class TestDispositivoArchivo(unittest.TestCase):

    def generarNombreArchivo(self):
        return '/tmp/test_' + self.id()

    def escribirArchivo(self, texto):
        nombreArchivo = self.generarNombreArchivo()
        with open(nombreArchivo, 'w') as archivo:
            archivo.write(texto)
        return nombreArchivo

    def leerArchivo(self, nombreArchivo):
        with open(nombreArchivo, 'r') as archivo:
            texto = archivo.read()
        return texto


class TestDispositivoDeLecturaArchivo(TestDispositivoArchivo):

    def test_se_genera_una_excepcion_si_el_archivo_no_existe(self):
        with self.assertRaises(IOError):
            DispositivoDeLecturaArchivo(
                '/tmp/archivo_inexistente' + str(random()))

    def test_se_lee_correctamente_el_archivo(self):
        textoEsperado = '10'
        nombreArchivo = self.escribirArchivo(textoEsperado)

        dispositivo = DispositivoDeLecturaArchivo(nombreArchivo)
        self.assertEqual(textoEsperado, dispositivo.leer())


class TestDispositivoDeEscrituraArchivo(TestDispositivoArchivo):

    def test_se_genera_una_excepcion_si_el_archivo_no_existe(self):
        with self.assertRaises(IOError):
            DispositivoDeLecturaArchivo(
                '/tmp/archivo_inexistente' + str(random()))

    def test_se_escribe_correctamente_el_archivo(self):
        texto = 'texto de ejemplo'
        nombreArchivo = self.generarNombreArchivo()
        dispositivo = DispositivoDeEscrituraArchivo(nombreArchivo)
        dispositivo.escribir(texto)
        self.assertEqual(texto, self.leerArchivo(nombreArchivo))
        dispositivo.cerrar()
