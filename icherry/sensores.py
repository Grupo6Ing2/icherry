class Sensor():

    def __init__(self, unDispositivoDeLectura, unParser, unaClaseDeMagnitud):
        self.dispositivo = unDispositivoDeLectura
        self.parser = unParser
        self.clase_de_magnitud = unaClaseDeMagnitud

    def sensar(self):
        return self.clase_de_magnitud(self.parser(self.dispositivo.leer()))
