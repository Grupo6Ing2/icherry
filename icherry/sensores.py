from icherry.observer import Observable


# Clase abstracta. No instanciar
class Sensor(Observable):

    def __init__(self):
        super().__init__()

    def sensar(self):
        raise NotImplementedError("Método abstracto")

    def ultimoValorSensado(self):
        raise NotImplementedError("Método abstracto")


class SensorDesdeArchivo(Sensor):

    def __init__(self, unDispositivoDeLectura, unParser, unaClaseDeMagnitud):
        super().__init__()

        self._dispositivo = unDispositivoDeLectura
        self._parser = unParser
        self._clase_de_magnitud = unaClaseDeMagnitud
        self._valor = None

    def sensar(self):
        cantidadParseada = self._parser.parse(self._dispositivo.leer())
        self._valor = self._clase_de_magnitud(cantidadParseada)
        self.notificarObservers()
        return self._valor

    def ultimoValorSensado(self):
        return self._valor
