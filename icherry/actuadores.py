import dispositivos
import parsers


class Actuador():

    def __init__(self, unDispositivoDeEscritura, unParserACadena):
        raise NotImplementedError("Clase abstracta")

    def aplicar(self, unaMagnitud):
        raise NotImplementedError("Método abstracto")


class ActuadorEnArchivo(Actuador):

    def __init__(self, unDispositivoDeEscritura, unParserACadena):
        self._dispositivo = unDispositivoDeEscritura
        self._parser = unParserACadena

    def aplicar(self, unaMagnitud):
        self._dispositivo.escribir(self._parser.parse(unaMagnitud))


class ConstructorDeActuadorEnArchivo():

    def __init__(self):
        pass

    def crear(self, unNombreArchivo):
        return ActuadorEnArchivo(
            dispositivos.DispositivoDeEscrituraArchivo(unNombreArchivo),
            parsers.MagnitudACadena()
        )
