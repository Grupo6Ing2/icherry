import icherry.sensores as sensores
import icherry.dispositivos as dispositivos
import icherry.magnitudes as magnitudes
import icherry.parsers as parsers
import icherry.proveedor_texto as proveedor_texto
import icherry.ui_ncurses as ui_ncurses
import icherry.central_meteorologica as central_meteorologica
import icherry.actualizadores as actualizadores
import icherry.estado_planta as estado_planta
import icherry.plan_maestro as plan_maestro


class ContructorDemo():

    def construirSensor(self, unNombreDeArchivo, unParser, unaMagnitud):

        sensor = sensores.SensorDesdeArchivo(
            dispositivos.DispositivoDeLecturaArchivo(unNombreDeArchivo),
            unParser,
            unaMagnitud
        )
        sensor.sensar()

        return sensor

    def construirSensorDeTemperatura(self):

        return self.construirSensor(
            'devices/sensor_temperatura',
            parsers.CadenaANumero(),
            magnitudes.TemperaturaEnCelsius
        )

    def construirSensorDeHumedad(self):

        return self.construirSensor(
            'devices/sensor_humedad',
            parsers.CadenaAPorcentaje(),
            magnitudes.HumedadRelativa,
        )

    def construirSensorDeAcidez(self):

        return self.construirSensor(
            'devices/sensor_acidez',
            parsers.CadenaANumero(),
            magnitudes.AcidezEnPH,
        )

    def construirSensores(self):

        sensorTemperatura = self.construirSensorDeTemperatura()
        sensorAcidez = self.construirSensorDeAcidez()
        sensorHumedad = self.construirSensorDeHumedad()

        return (sensorTemperatura, sensorHumedad, sensorAcidez)

    def construirActualizadorDeSensores(self, segundosDeActualizacion, sensorTemperatura, sensorHumedad, sensorAcidez):

        return actualizadores.ActualizadorDeSensores(
            segundosDeActualizacion,
            sensorTemperatura,
            sensorHumedad,
            sensorAcidez
        )

    def construirProveedorDeTexto(self):

        return proveedor_texto.ProveedorDeTexto('resources/textos.es')

    def construirCentralMeterologica(self):

        predictor = central_meteorologica.PredictorMeteorologicoPorArchivo(
            dispositivos.DispositivoDeLecturaArchivo("devices/pronostico")
        )
        reloj = central_meteorologica.ProveedorDeTiempoPorArchivo(
            dispositivos.DispositivoDeLecturaArchivo("devices/tiempo")
        )

        central = central_meteorologica.CentralMeteorologica(predictor, reloj)
        central.obtenerPronostico(central.obtenerFechaYHora(), 24)

        return central

    def construirActualizadorDeCentral(self, segundosDeActualizacion, centralMeteorologica):

        return actualizadores.ActualizadorDeCentralMeteorologica(
            segundosDeActualizacion, centralMeteorologica)

    def construirPlanMaestro(self):

        def rangoT(desde, hasta):
            return magnitudes.Rango(magnitudes.TemperaturaEnCelsius(desde),
                                    magnitudes.TemperaturaEnCelsius(hasta))

        def rangoH(desde, hasta):
            return magnitudes.Rango(magnitudes.HumedadRelativa(magnitudes.Porcentaje(desde)),
                                    magnitudes.HumedadRelativa(magnitudes.Porcentaje(hasta)))

        def rangoPH(desde, hasta):
            return magnitudes.Rango(magnitudes.AcidezEnPH(desde),
                                    magnitudes.AcidezEnPH(hasta))

        def definirUmbral(planMaestro, estadio,
                          desdeT, hastaT,
                          desdeH, hastaH,
                          desdePH, hastaPH):
            umbral = plan_maestro.UmbralOptimoDeCultivo(
                estadio,
                rangoTemperatura=rangoT(desdeT, hastaT),
                rangoHumedad=rangoH(desdeH, hastaH),
                rangoAcidez=rangoPH(desdePH, hastaPH))
            planMaestro[estadio] = umbral

        # construimos un plan maestro con algunos valores arbitrarios por defacto.
        planMaestro = plan_maestro.PlanMaestro()
        definirUmbral(planMaestro, plan_maestro.EstadioGerminacion, 12, 40, 40, 70, 5, 8)
        definirUmbral(planMaestro, plan_maestro.EstadioDesarrollo, 14, 35, 40, 70, 5, 8)
        definirUmbral(planMaestro, plan_maestro.EstadioBrotes, 12, 35, 40, 70, 5, 8)
        definirUmbral(planMaestro, plan_maestro.EstadioAparicion, 12, 35, 40, 70, 5, 8)
        definirUmbral(planMaestro, plan_maestro.EstadioFloracion, 15, 36, 40, 70, 5, 8)
        definirUmbral(planMaestro, plan_maestro.EstadioFruto, 18, 40, 50, 90, 5, 8)
        definirUmbral(planMaestro, plan_maestro.EstadioMaduracion, 18, 45, 45, 60, 5, 8)
        definirUmbral(planMaestro, plan_maestro.EstadioSenescencia, 16, 32, 40, 60, 5, 8)

        return planMaestro

    def construirEstadoDePlanta(self):

        return estado_planta.EstadoDePlanta()

    def construirActualizadorDeEstadoDePlanta(self, segundosDeActualizacion,
            estadoPlanta,
            sensorDeTemperatura,
            sensorDeHumedad,
            sensorDeAcidez,
            planMaestro):

        return actualizadores.ActualizadorDeEstadoDePlanta(segundosDeActualizacion,
            estadoPlanta,
            sensorDeTemperatura,
            sensorDeHumedad,
            sensorDeAcidez,
            planMaestro)

    def construirAplicacion(self):

        return ui_ncurses.ICherryCurses()

    def construirPantallaSensores(self, proveedorDeTexto, sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez):

        return ui_ncurses.PantallaDeSensoresMVC(
            proveedorDeTexto,
            sensorDeTemperatura,
            sensorDeHumedad,
            sensorDeAcidez
        )

    def contruirPantallaInicio(self, proveedorDeTexto):

        return ui_ncurses.PantallaDeInicio(
            proveedorDeTexto,
            archivoFondoAscii='resources/main_background_pic.txt'
        )

    def construirPantallaEnConstruccion(self, proveedorDeTexto):

        return ui_ncurses.PantallaEnConstruccion(proveedorDeTexto)

    def construirPantallaCentralMeteorologica(self, proveedorDeTexto, centralMeteorologica):

        return ui_ncurses.PantallaDeCentralMVC(proveedorDeTexto, centralMeteorologica)

    def construirPantallaEstadoDePlanta(self, proveedorDeTexto, estadoDePlanta):

        return ui_ncurses.PantallaDeEstadoDePlantaMVC(proveedorDeTexto, estadoDePlanta)

    def construirPantallaDeEdicionDeEstadoFenologico(self, proveedorDeTexto, estadoFenologico):

        return ui_ncurses.PantallaDeEdicionDeEstadoFenologico(proveedorDeTexto, estadoFenologico)
