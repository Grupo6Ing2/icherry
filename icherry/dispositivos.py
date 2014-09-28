# coding=utf-8
import os


class DispositivoDeLectura():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def leer(self):
        raise NotImplementedError("Método abstracto")


class DispositivoDeLecturaArchivo(DispositivoDeLectura):

    def __init__(self, unNombreArchivo):
        self._archivo = open(unNombreArchivo, 'r')

    def leer(self):
        self._archivo.seek(0)
        return self._archivo.read()

    def cerrar(self):
        self._archivo.close()


class DispositivoDeEscritura():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def escribir(self):
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
