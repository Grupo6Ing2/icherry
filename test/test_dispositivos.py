from icherry.dispositivos import DispositivoDeEscrituraArchivo
from icherry.dispositivos import DispositivoDeLecturaArchivo

import unittest
import os
from tempfile import NamedTemporaryFile


class TestDispositivoArchivo(unittest.TestCase):

    def generarArchivo(self):
        """Crea un archivo de nombre aleatorio (se garantiza que el
        archivo no existía previamente), y retorna su nombre. El
        nombre es relativo al directorio actual.

        """
        prefijo = 'test_' + self.id()
        archivo = NamedTemporaryFile(delete=False, dir=".", prefix=prefijo)
        archivo.close()
        return archivo.name

    def escribirArchivo(self, texto):
        nombreArchivo = self.generarArchivo()
        with open(nombreArchivo, 'w') as archivo:
            archivo.write(texto)
        return nombreArchivo

    def leerArchivo(self, nombreArchivo):
        with open(nombreArchivo, 'r') as archivo:
            texto = archivo.read()
        return texto


class TestDispositivoDeLecturaArchivo(TestDispositivoArchivo):

    def test_se_genera_una_excepcion_si_el_archivo_no_existe(self):
        nombreArchivoInexistente = self.generarArchivo()
        os.unlink(nombreArchivoInexistente)
        # asumimos que no ocurrirá que _justo_ ahora alguien cree un
        # archivo con ese nombre (race condition).
        with self.assertRaises(IOError):
            DispositivoDeLecturaArchivo(nombreArchivoInexistente)

    def test_se_lee_correctamente_el_archivo(self):
        textoEsperado = '10'
        nombreArchivo = self.escribirArchivo(textoEsperado)

        dispositivo = DispositivoDeLecturaArchivo(nombreArchivo)
        self.assertEqual(textoEsperado, dispositivo.leer())

        os.unlink(nombreArchivo)


class TestDispositivoDeEscrituraArchivo(TestDispositivoArchivo):

    def test_se_genera_una_excepcion_si_el_archivo_no_existe(self):
        nombreArchivoInexistente = self.generarArchivo()
        os.unlink(nombreArchivoInexistente)
        # asumimos que no ocurrirá que _justo_ ahora alguien cree un
        # archivo con ese nombre (race condition).
        with self.assertRaises(IOError):
            DispositivoDeEscrituraArchivo(nombreArchivoInexistente)

    def test_se_escribe_correctamente_el_archivo(self):
        texto = 'texto de ejemplo'
        nombreArchivo = self.generarArchivo()

        dispositivo = DispositivoDeEscrituraArchivo(nombreArchivo)
        dispositivo.escribir(texto)
        self.assertEqual(texto, self.leerArchivo(nombreArchivo))

        os.unlink(nombreArchivo)
