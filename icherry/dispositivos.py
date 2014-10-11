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
        if not os.path.exists(unNombreArchivo):
            raise IOError("El archivo {0} no existe".format(unNombreArchivo))
        self._nombreArchivo = unNombreArchivo

    def escribir(self, unaCadena):
        with open(self._nombreArchivo, 'w') as archivo:
            archivo.write(unaCadena)
            archivo.flush()
            os.fsync(archivo.fileno())
        return self
