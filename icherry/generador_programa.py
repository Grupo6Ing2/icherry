# ====================================================================
#                 GENERADOR DE PROGRAMA DE SUMINISTRO
# ====================================================================

from icherry.tiempo import FechaYHora, DuracionEnMinutos, DuracionEnHoras
from icherry.magnitudes import Rango, LiquidoEnMililitros, LuzEnLux
from icherry.programa_suministro import ProgramaDeSuministro, AccionRegado, AccionLuz
from icherry.programa_suministro import AccionFertilizante, AccionAntibiotico

from datetime import date, time


# ====================================================================
# GeneradorDeProgramaDeSuministro

# El generador de programa de suministro (aka 'GPS') es lo que genera
# un nuevo programa de suministro a partir del estado de salud de la
# planta, el umbral óptimo de cultivo según el plan maestro, etcétera.

class GeneradorDeProgramaDeSuministro():
    def __init__(self, planMaestro, recomendacionesDeCultivo):
        self.__planMaestro = planMaestro
        self.__recomendaciones = recomendacionesDeCultivo

    # Modifica el ProgramaDeSuministro
    def generar(self, estadoDePlanta, centralMeteorologica):
        programaDeSuministro = self.__generarProgramaInicial(
            estadoDePlanta, centralMeteorologica)
        self.__aplicarRecomendacionesDeCultivo(
            programaDeSuministro, estadoDePlanta, centralMeteorologica)

        return programaDeSuministro

    # Modifica el programa de suministro en base a todos los parámetros:
    def __generarProgramaInicial(self, estadoDePlanta, centralMeteorologica):
        # TODO: aca es donde se produce la magia de generación de un programa.
        pass

    def __aplicarRecomendacionesDeCultivo(
            self, programaDeSuministro, estadoDePlanta, centralMeteorologica):
        for recomendacion in self.__recomendaciones:
            recomendacion.realizarAjustes(
                self.__planMaestro, estadoDePlanta,
                centralMeteorologica, programaDeSuministro)


# ====================================================================
# GeneradorDeProgramaDeSuministroEjemploFijo24

# Mi muy querido GPS "Fijo24", que rota siempre el mismo programa. Se
# asignan acciones fijas a distintos horarios del día, en forma
# arbitraria. El período es de 24 horas, de ahí el nombre. O sea que a
# cada 24 horas repite todo otra vez.
#
# Se pueden cambiar a gusto las acciones que caen en cada momento para
# probar distintos efectos.

class GeneradorDeProgramaDeSuministroFijo24(GeneradorDeProgramaDeSuministro):
    """Genera un programa de suministro hardcodeado con valores fijos para
    distintos horarios del día, cubriendo un rango de 24 horas. Los valores son
    totalmente arbitrarios, esta instancia es útil para pruebas y
    experimentos.

    """

    def __init__(self, planMaestro, estadoDePlanta,
                 centralMeteorologica, programaDeSuministro):
        # descartamos PM y EP
        self._centralMeteorologica = centralMeteorologica
        self._programaDeSuministro = programaDeSuministro

    def _ahora(self):
        return self._centralMeteorologica.obtenerFechaYHora()

    # Esto es tal vez lo único interesante de todo esto. Necesitamos
    # este algoritmo para lograr independencia de la hora del día
    # reportada por la CM.
    def _shift(self, duracionRelativaCero, ahora):
        """computa una fechaYHora a partir de una duración relativa a las cero
        horas del día indicado por 'ahora', pero asegurando que
        si el resultado cayera el día anterior, se desplaza para la
        misma hora pero del día siguiente.

        """
        cero = FechaYHora(ahora.fecha(), time(0, 0, 0))
        ajustada = cero.agregarDuracion(duracionRelativaCero)
        if ajustada < ahora:
            ajustada = ajustada.agregarDuracion(DuracionEnHoras(24))
        return ajustada

    def generar(self):
        ahora = self._ahora()

        programa = ProgramaDeSuministro(
            Rango(ahora, ahora.agregarDuracion(DuracionEnHoras(24))))

        # regar 100 mililitros una vez por hora
        for i in range(24):
            programa.programarAccion(self._shift(DuracionEnHoras(i), ahora),
                                     AccionRegado(LiquidoEnMililitros(100)))

        # poner la lámpara a 800 lux a las 5:15  y en 1000 lux a las 10:15
        programa.programarAccion(self._shift(DuracionEnMinutos(60 * 5 + 15), ahora),
                                 AccionLuz(LuzEnLux(800)))
        programa.programarAccion(self._shift(DuracionEnMinutos(60 * 10 + 15), ahora),
                                 AccionLuz(LuzEnLux(1000)))

        # aplicar fertilizante a cada 4 horas
        for i in range(6):
            programa.programarAccion(self._shift(DuracionEnMinutos(60 * i * 4 + 25), ahora),
                                     AccionFertilizante(LiquidoEnMililitros(50)))

        # aplicar antibiótico a las 12
        programa.programarAccion(self._shift(DuracionEnHoras(12), ahora),
                                 AccionAntibiotico(LiquidoEnMililitros(10)))

        self._programaDeSuministro.copiar(programa)
        self._programaDeSuministro.notificarObservers()


# ====================================================================
# mini demo (para correr en la repl)

# En esta demo probamos el algoritmo de _shift del GPS "Fijo24"


def demo():
    ahora = FechaYHora(date(1998, 7, 10), time(17, 0, 0))  # modificar a gusto!

    class CentralMeteorologicaMock:

        def __init__(self, fechaYHora=ahora):
            self.redefinirFechaYHora(fechaYHora)

        def redefinirFechaYHora(self, FechaYHora):
            self._ahora = FechaYHora

        def obtenerFechaYHora(self):
            return self._ahora

    def mostrar(gps, cm):
        print("==== Programa de Suministro ====")
        print("A partir de fecha/hora : %s" % cm.obtenerFechaYHora())
        aps = programa.accionesProgramadas()
        for ap in aps:
            fh = ap.fechaYHora()
            print("%s : %s %s" % (fh.fecha(), fh.hora(), ap.accion().nombre()))
        print("%d acciones en total" % len(aps))

    cm = CentralMeteorologicaMock()

    programa = ProgramaDeSuministro(
        Rango(ahora, ahora.agregarDuracion(DuracionEnHoras(24))))

    gps = GeneradorDeProgramaDeSuministroFijo24(
        planMaestro=None, estadoDePlanta=None,
        centralMeteorologica=cm,
        programaDeSuministro=programa)

    gps.generar()
    mostrar(gps, cm)
    cm.redefinirFechaYHora(ahora.agregarDuracion(DuracionEnMinutos(60 * 10 + 15)))
    gps.generar()
    mostrar(gps, cm)


if __name__ == "__main__":
    demo()
