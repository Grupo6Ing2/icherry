from icherry.observer import Observable


class Sensor(Observable):

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
