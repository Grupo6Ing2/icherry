from icherry.observer import Observer

# Clase abstracta, no instanciar.
class Log(Observer):
    def __init__(self, unDispositivoDeEscritura):
        self.__dispositivoDeEscritura = unDispositivoDeEscritura

    def update(self, unObservable):
        self.__dispositivoDeEscritura.escribir(self.entradaEnElLog(unObservable))

    # Devuelve una cadena que se va a escribir en el log
    def entradaEnElLog(self, unObservable):
        raise NotImplementedError("Metodo abstracta")


class LogCentralMeteorologica(Log):
    def entradaEnElLog(self, centralMeteorologica):
        return 'Ultimo pronostico de la central meteorologica: {0}\n'.\
            format(centralMeteorologica.ultimoPronostico())


class LogSensor(Log):
    def __init__(self, nombreSensor, unDispositivoDeEscritura):
        super().__init__(unDispositivoDeEscritura)
        self.__nombreSensor = nombreSensor

    def entradaEnElLog(self, unSensor):
        return '{0} indica {1}\n'.format(self.__nombreSensor, unSensor.ultimoValorSensado())
