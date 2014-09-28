class Sensor():

    def __init__(self, unDispositivoDeLectura, unParser, unaClaseDeMagnitud):
        self._dispositivo = unDispositivoDeLectura
        self._parser = unParser
        self._clase_de_magnitud = unaClaseDeMagnitud

    def sensar(self):
        return self._clase_de_magnitud(self._parser.parse(self._dispositivo.leer()))
