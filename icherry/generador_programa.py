
class GeneradorDeProgramaDeSuministro():

    def __init__(self, unPlanMaestro, recomendacionesDeCultivo):
        self.__planMaestro = unPlanMaestro
        self.__recomendaciones = recomendacionesDeCultivo

    # Modifica el ProgramaDeSuministro
    def generar(self, unaPlanta, unaCentralMeteorologica):
        programaDeSuministro = self.__generarProgramaInicial(unaPlanta,
                                                             unaCentralMeteorologica)
        self.__aplicarRecomendacionesDeCultivo(programaDeSuministro, unaPlanta,
                                               unaCentralMeteorologica)

        return programaDeSuministro

    # Modifica unProgramaDeSuministros en base a todos los parámetros:
    def __generarProgramaInicial(self, unaPlanta, unaCentralMeteorologica):
        # TODO: aca es donde se produce la magia de generación de un programa.
        pass

    def __aplicarRecomendacionesDeCultivo(self, unProgramaDeSuministros, unaPlanta,
                                          unaCentralMeteorologica):
        for recomendacion in self.__recomendaciones:
            recomendacion.realizarAjustes(
                self.__planMaestro, unaPlanta, unaCentralMeteorologica, unProgramaDeSuministros)


class ActualizadorDeProgramaDeSuministro():
    def __init__(self, unProgramaDeSuministros, unGeneradorDePrograma, unaPlanta,
                 unaCentralMeteorologica):
        super().__init__()

        self.__programa = unProgramaDeSuministros
        self.__generadorDePrograma = unGeneradorDePrograma
        self.__planta = unaPlanta
        self.__central = unaCentralMeteorologica

    def actualizarProgramaDeSuministro(self):
        nuevoPrograma = self.__generadorDePrograma.generar(
            self.__programa, self.__planta, self.__central)
        self.__programa.copiar(nuevoPrograma)
        self.__programa.notificarObservers()
