class RecomendacionDeCultivo():
    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    # Analiza las acciones programadas del programa de suministro y realiza los
    # ajustes necesarios. Se agregan o se eliminan acciones.
    def realizarAjustes(self, unProgramaDeSuministro):
        raise NotImplementedError("Método abstracto")


class RecomendacionDeCultivoRiegosConstantes(RecomendacionDeCultivo):
    def __init__(self):
        pass

    def realizarAjustes(self, unPlanMaestro, unaPlanta, unaCentralMeteorologica,
                        unProgramaDeSuministro):
        # TODO ver que haya riegos constantes.
        pass


class RecomendacionDeCultivoSePrefierenTemperaturasModeradas(RecomendacionDeCultivo):
    def __init__(self):
        pass

    def realizarAjustes(self, unPlanMaestro, unaPlanta, unaCentralMeteorologica,
                        unProgramaDeSuministro):
        # TODO ver que la temperatura establecida por el programa sea moderada.
        pass


class RecomendacionNoDebeHaberAltaAmplitudTermica(RecomendacionDeCultivo):
    def __init__(self):
        pass

    def realizarAjustes(self, unPlanMaestro, unaPlanta, unaCentralMeteorologica,
                        unProgramaDeSuministro):
        # TODO ajustar las temperaturas para que no haya mucha amplitud.
        pass
