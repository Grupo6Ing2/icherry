from icherry.observer import Observable


class ConstructorDeProgramaDeSuministro():

    def __init__(self, unPlanMaestro):
        self.__planMaestro = unPlanMaestro


    # Modifica el ProgramaDeSuministro
    def construir(self, unProgramaDeSuministro, unaPlanta, unaCentralMeteorologica,
                  recomendacionesDeCultivo):
        self.__construirUnProgramaInicial(
            unProgramaDeSuministro,
            unaPlanta.estadioFenologico(),
            unaCentralMeteorologica.obtenerFechaYHora(),
            unaCentralMeteorologica.ultimoPronostico(),
            unaPlanta.sensorDeTemperatura().ultimoValorSensado(),
            unaPlanta.sensorDeHumedad().ultimoValorSensado(),
            unaPlanta.sensorDeAcidez().ultimoValorSensado(),
            self.__planMaestro)

        self.__aplicarReglasDeCultivo(unProgramaDeSuministro, reglasDeCultivo)

        return programa

    # Modifica unProgramaDeSuministro en base a todos los parametros:
    def __construirUnProgramaInicial(self, unProgramaDeSuministro, estadioFenologico,
            fechaYHoraActual, unPronostico, temperatura, humedad, acidez, unPlanMaestro):
        #TODO: aca es donde se produce la magia de generacion de un programa.
        pass


    def __aplicarRecomendacionesDeCultivo(self, unProgramaDeSuministro, recomendacionesDeCultivo):
        for recomendacion in recomendacionesDeCultivo:
            recomendacion.realiza1rAjustes(unProgramaDeSuministro)


class ActualizadorDeProgramaDeSuministro(Observable):
    def __init__(self, unProgramaDeSuministro, unConstructorDePrograma, unaPlanta,
                 unaCentralMeteorologica, recomendacionesDeCultivo):
        super().__init__()

        self.__programa = unProgramaDeSuministro
        self.__constructorDePrograma = unConstructorDePrograma
        self.__planta = unaPlanta
        self.__central = unaCentralMeteorologica
        self.__recomendaciones = recomendacionesDeCultivo


    def actualizarProgramaDeSuministro(self):
        self.__constructorDePrograma.construir(self.__programa, self.__planta,
                      self.__central, self.__recomendaciones)
        self.notificarCambios()





