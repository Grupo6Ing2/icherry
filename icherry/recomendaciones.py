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
                        unProgramaDeSuministros):
        # TODO ver que haya riego constantes.
        pass


class RecomendacionDeCultivoSePrefierenTemperaturasModeradas(RecomendacionDeCultivo):
    def __init__(self):
        pass

    def realizarAjustes(self, unPlanMaestro, unaPlanta, unaCentralMeteorologica,
                        unProgramaDeSuministros):
        # TODO ver que la temperatura establecida por el programa sea moderada.
        pass


class RecomendacionNoDebeHaberAltaAmplitudTermica(RecomendacionDeCultivo):
    def __init__(self):
        pass

    def realizarAjustes(self, unPlanMaestro, unaPlanta, unaCentralMeteorologica,
                        unProgramaDeSuministros):
        # TODO ajustar las temperaturas para que no haya mucha amplitud.
        pass
