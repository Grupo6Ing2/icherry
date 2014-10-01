# coding=utf-8
import os


class DispositivoDeLectura():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def leer(self):
        raise NotImplementedError("Método abstracto")


class DispositivoDeLecturaArchivo(DispositivoDeLectura):

    def __init__(self, unNombreArchivo):
        if not os.path.exists(unNombreArchivo):
            raise IOError("El archivo {0} no existe".format(unNombreArchivo))
        self._nombreArchivo = unNombreArchivo

    def leer(self):
        with open(self._nombreArchivo, 'r') as archivo:
            lectura = archivo.read()
        return lectura

class DispositivoDeEscritura():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def escribir(self, unaCadena):
        raise NotImplementedError("Método abstracto")


class DispositivoDeEscrituraArchivo(DispositivoDeEscritura):

    def __init__(self, unNombreArchivo):
        self._archivo = open(unNombreArchivo, 'w')

    def escribir(self, unaCadena):
        self._archivo.write(unaCadena)
        self._archivo.flush()
        os.fsync(self._archivo.fileno())
        return self

    def cerrar(self):
        self._archivo.close()
