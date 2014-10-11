import icherry.temporizador as temporizador
import icherry.observer as observer
import icherry.estado_planta as planta


class ActualizadorDeObjectos(observer.Observable):

    def __init__(self, duracionDeActualizacion, *args, **kargs):
        super().__init__()

        self._timer = temporizador.Temporizador()
        self._timer.ejecutarCada(
            duracionDeActualizacion,
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
        self._central.obtenerPronostico(fechaYHora, 28)

    def centralMeteorologica(self):
        return self._central


class ActualizadorDeEstadoDePlanta(ActualizadorDeObjectos):

    def _inicializar(self, estadoPlanta, sensorDeTemperatura,
                     sensorDeHumedad, sensorDeAcidez, planMaestro):

        self._estadoPlanta = estadoPlanta
        self._sensorDeTemperatura = sensorDeTemperatura
        self._sensorDeHumedad = sensorDeHumedad
        self._sensorDeAcidez = sensorDeAcidez
        self._planMaestro = planMaestro

    def estadoPlanta(self):

        return self._estadoPlanta

    def sensorDeTemperatura(self):

        return self._sensorDeTemperatura

    def sensorDeHumedad(self):

        return self._sensorDeHumedad

    def sensorDeAcidez(self):

        return self._sensorDeAcidez

    def planMaestro(self):

        return self._planMaestro

    def _actualizar(self):

        # Obtenemos los valores de T/H/PH de los sensores según la última medición
        temperatura = self.sensorDeTemperatura().ultimoValorSensado()
        humedad = self.sensorDeHumedad().ultimoValorSensado()
        acidez = self.sensorDeAcidez().ultimoValorSensado()

        # Obtenemos el umbral del estadio actual de la planta
        estadio = self.estadoPlanta().estadoFenologico().estadioDeCultivo()
        umbral = self.planMaestro()[estadio]

        # Actualizamos el estado de salud, según el umbral óptimo de
        # cultivo para el estadio de cultivo actual
        estadoDeSalud = planta.EstadoDeSaludBueno
        if not umbral.temperatura().contiene(temperatura):
            estadoDeSalud = planta.EstadoDeSaludMalo
        if not umbral.humedad().contiene(humedad):
            estadoDeSalud = planta.EstadoDeSaludMalo
        if not umbral.acidez().contiene(acidez):
            estadoDeSalud = planta.EstadoDeSaludMalo

        self._estadoPlanta.estadoDeSalud(estadoDeSalud)
        # estadoDeSalud.notificarEstadoA(notificado)

        # actualizamos el estado de la planta y notificamos a sus
        # observadores.
        self._estadoPlanta.temperatura(temperatura)
        self._estadoPlanta.humedad(humedad)
        self._estadoPlanta.acidez(acidez)
        self._estadoPlanta.notificarObservers()


# este bicho es casi trivial porque el GPS hace todo el laburo
class ActualizadorDeProgramaDeSuministro(ActualizadorDeObjectos):

    def _inicializar(self, generadorDeProgramaDeSuministro):
        self._GPS = generadorDeProgramaDeSuministro

    def _actualizar(self):
        self._GPS.generar()     # esto notifica a los observadores


class ActualizadorDeEjecucion(ActualizadorDeObjectos):
    def _inicializar(self, centralMeteorologica, planificadorEjecucion):
        self._PE = planificadorEjecucion
        self._CM = centralMeteorologica

    def _actualizar(self):
        ahora = self._CM.obtenerFechaYHora()
        self._PE.planificarAcciones(ahora)  # esto notifica a los observadores
