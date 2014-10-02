import icherry.temporizador as temporizador
import icherry.tiempo as tiempo
import icherry.observer as observer


class ActualizadorDeObjectos(observer.Observable):

    def __init__(self, segundosDeActualizacion, *args, **kargs):
        super().__init__()

        self._timer = temporizador.Temporizador()
        self._timer.ejecutarCada(
            tiempo.DuracionEnSegundos(segundosDeActualizacion),
            lambda: self.actualizar()
        )

        self._inicializar(*args, **kargs)

    def _inicializar():
        pass

    def actualizar(self):

        self._actualizar()
        self.notificarObservers()

    def iniciarActualizacion(self):

        self._timer.iniciarEjecucion()

    def detenerActualizacion(self):

        self._timer.detener()

    def _actualizar(self):
        pass


class ActualizadorDeSensores(ActualizadorDeObjectos):

    def _inicializar(self, sensorTemperatura, sensorHumedad, sensorAcidez):

        self._sensorTemperatura = sensorTemperatura
        self._sensorHumedad = sensorHumedad
        self._sensorAcidez = sensorAcidez

    def _actualizar(self):

        self._sensorTemperatura.sensar()
        self._sensorAcidez.sensar()
        self._sensorHumedad.sensar()

    def sensorTemperatura(self):
        return self._sensorTemperatura

    def sensorAcidez(self):
        return self._sensorAcidez

    def sensorHumedad(self):
        return self._sensorHumedad


class ActualizadorDeCentralMeteorologica(ActualizadorDeObjectos):

    def _inicializar(self, centralMeteorologica):

        self._central = centralMeteorologica

    def _actualizar(self):

        fechaYHora = self._central.obtenerFechaYHora()
        self._central.obtenerPronostico(fechaYHora, 24)

    def centralMeteorologica(self):
        return self._central


class ActualizadorDeEstadoDePlanta(ActualizadorDeObjectos):

    def _inicializar(self, estadoPlanta, sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez, planMaestro):

        self._estadoPlanta = estadoPlanta
        self._sensorDeTemperatura = sensorDeTemperatura
        self._sensorDeHumedad = sensorDeHumedad
        self._sensorDeAcidez = sensorDeAcidez
        self._planMaestro = planMaestro

    def estadoPlanta(self):

        return self.estadoPlanta

    def sensorDeTemperatura(self):

        return self.sensorDeTemperatura

    def sensorDeHumedad(self):

        return self.sensorDeHumedad

    def sensorDeAcidez(self):

        return self.sensorDeAcidez

    def planMaestro(self):

        return self.planMaestro

    def _actualizar(self):

        # Actualizo los valores de los sensores
        self._estadoPlanta.temperatura(self._sensorDeTemperatura.ultimoValorSensado())
        self._estadoPlanta.humedad(self._sensorDeHumedad.ultimoValorSensado())
        self._estadoPlanta.acidez(self._sensorDeAcidez.ultimoValorSensado())
        self._estadoPlanta.notificarObservers()
