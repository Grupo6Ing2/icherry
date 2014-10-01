from icherry.observer import Observable


class ConstructorDeProgramaDeSuministro():

    def __init__(self, unPlanMaestro, recomendacionesDeCultivo):
        self.__planMaestro = unPlanMaestro
        self.__recomendaciones = recomendacionesDeCultivo

    # Modifica el ProgramaDeSuministro
    def construir(self, unaPlanta, unaCentralMeteorologica):
        programaDeSuministro = self.__construirUnProgramaInicial(unaPlanta, unaCentralMeteorologica)
        self.__aplicarRecomendacionesDeCultivo(programaDeSuministro, unaPlanta, unaCentralMeteorologica)

        return programaDeSuministro

    # Modifica unProgramaDeSuministros en base a todos los parametros:
    def __construirUnProgramaInicial(self, unaPlanta, unaCentralMeteorologica):
        #TODO: aca es donde se produce la magia de generacion de un programa.
        pass

    def __aplicarRecomendacionesDeCultivo(self, unProgramaDeSuministros, unaPlanta, unaCentralMeteorologica):
        for recomendacion in self.__recomendaciones:
            recomendacion.realizarAjustes(
                self.__planMaestro, unaPlanta, unaCentralMeteorologica, unProgramaDeSuministros)


class ActualizadorDeProgramaDeSuministro(Observable):
    def __init__(self, unProgramaDeSuministros, unConstructorDePrograma, unaPlanta,
                 unaCentralMeteorologica):
        super().__init__()

        self.__programa = unProgramaDeSuministros
        self.__constructorDePrograma = unConstructorDePrograma
        self.__planta = unaPlanta
        self.__central = unaCentralMeteorologica

    def actualizarProgramaDeSuministro(self):
        nuevoPrograma = self.__constructorDePrograma.construir(
            self.__programa, self.__planta, self.__central)
        self.__programa.copiar(nuevoPrograma)
        self.__programa.notificarCambios()
