from icherry.dispositivos import DispositivoDeEscrituraArchivo
from icherry.dispositivos import DispositivosDeLecturaArchivo

import unittest
from random import random


class TestDispositivoArchivo(unittest.TestCase):

    def generarNombreArchivo(self):
        return '/tmp/test_' + self.id()

    def escribirArchivo(self, texto):
        nombreArchivo = self.generarNombreArchivo()
        archivo = open(nombreArchivo, 'w')
        archivo.write(texto)
        archivo.close()
        return nombreArchivo

    def leerArchivo(self, nombreArchivo):
        archivo = open(nombreArchivo, 'r')
        texto = archivo.read()
        archivo.close()
        return texto


class TestDispositivoDeLecturaArchivo(TestDispositivoArchivo):

    def test_se_genera_una_excepcion_si_el_archivo_no_existe(self):
        with self.assertRaises(IOError):
            DispositivosDeLecturaArchivo(
                '/tmp/archivo_inexsitente' + str(random()))

    def test_se_lee_correctamente_el_archivo(self):
        textoEsperado = '10'
        nombreArchivo = self.escribirArchivo(textoEsperado)

        dispositivo = DispositivosDeLecturaArchivo(nombreArchivo)
        self.assertEqual(textoEsperado, dispositivo.leer())


class TestDispositivoDeEscrituraArchivo(TestDispositivoArchivo):

    def test_se_genera_una_excepcion_si_el_archivo_no_existe(self):
        with self.assertRaises(IOError):
            DispositivosDeLecturaArchivo(
                '/tmp/archivo_inexsitente' + str(random()))

    def test_se_escribe_correctamente_el_archivo(self):
        texto = 'texto de ejemplo'
        nombreArchivo = self.generarNombreArchivo()
        dispositivo = DispositivoDeEscrituraArchivo(nombreArchivo)
        dispositivo.escribir(texto)
        self.assertEqual(texto, self.leerArchivo(nombreArchivo))
