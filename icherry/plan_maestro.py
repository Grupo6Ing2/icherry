# encoding: utf-8
# ====================================================================
#                            PLAN MAESTRO
# ====================================================================

# Se definen los conceptos relacionados con el plan maestro : estadios
# de cultivo, umbral óptimo de cultivo y plan maestro.


# ====================================================================
# plan maestro
class PlanMaestro():
    """Un plan maestro es un diccionario de estado fenológico en umbral
    óptimo de cultivo. Con el plan maestro sabemos en qué parámetros
    de T/H/PH se debe mantener la planta en el estadio actual. Para
    construirse, requiere una lista de umbrales óptimos de cultivo
    (que no se solapen, es decir no haya dos que correspondan al mismo
    estadio).

    """
    def __init__(self, umbrales=None):
        """Crea un nuevo plan maestro vacío, sin ningún umbral definido, o
        bien a partir de una lista de umbrales.

        """
        self._umbralGerminacion = None
        self._umbralDesarrollo = None
        self._umbralBrotes = None
        self._umbralAparicion = None
        self._umbralFloracion = None
        self._umbralFruto = None
        self._umbralMaduracion = None
        self._umbralSenescencia = None
        if umbrales is not None:
            for u in umbrales:
                self.definirUmbralParaEstadio(u.estadio(), u)

    def umbralParaEstadio(self, claseEstadio):
        """Retorna el umbral para el estadio de cultivo indicado. Se
        debe pasar como argumento una clase (o instancia) de estadio
        de cultivo.

        """
        return claseEstadio.umbral(self)

    def definirUmbralParaEstadio(self, claseEstadio, umbral):
        """Define el umbral para el estadio de cultivo indicado. El argumento
        'claseEstadio' funciona como en 'umbralParaEstadio'

        """
        return claseEstadio.umbral(self, umbral)

    def umbrales(self):
        """Retorna la lista de todos los umbrales que planifica"""
        estadios = CicloDeVida.estadios()
        umbrales = [self.umbralParaEstadio(estadio) for estadio in estadios]
        return [umbral for umbral in umbrales if umbral is not None]

    # los dos siguientes son para aprovechar la sintaxis de acceso por
    # corchetes.

    def __getitem__(self, estadio):
        return self.umbralParaEstadio(estadio)

    def __setitem__(self, estadio, umbral):
        return self.definirUmbralParaEstadio(estadio, umbral)

    # los siguientes métodos son de uso interno para doble-dispatch
    # contra los estadios de cultivo. No deben ser usados
    # externamente.

    def umbralGerminacion(self, umbralGerminacion=None):
        if umbralGerminacion is None:
            return self._umbralGerminacion
        else:
            self._umbralGerminacion = umbralGerminacion
            return self

    def umbralDesarrollo(self, umbralDesarrollo=None):
        if umbralDesarrollo is None:
            return self._umbralDesarrollo
        else:
            self._umbralDesarrollo = umbralDesarrollo
            return self

    def umbralBrotes(self, umbralBrotes=None):
        if umbralBrotes is None:
            return self._umbralBrotes
        else:
            self._umbralBrotes = umbralBrotes
            return self

    def umbralAparicion(self, umbralAparicion=None):
        if umbralAparicion is None:
            return self._umbralAparicion
        else:
            self._umbralAparicion = umbralAparicion
            return self

    def umbralFloracion(self, umbralFloracion=None):
        if umbralFloracion is None:
            return self._umbralFloracion
        else:
            self._umbralFloracion = umbralFloracion
            return self

    def umbralFruto(self, umbralFruto=None):
        if umbralFruto is None:
            return self._umbralFruto
        else:
            self._umbralFruto = umbralFruto
            return self

    def umbralMaduracion(self, umbralMaduracion=None):
        if umbralMaduracion is None:
            return self._umbralMaduracion
        else:
            self._umbralMaduracion = umbralMaduracion
            return self

    def umbralSenescencia(self, umbralSenescencia=None):
        if umbralSenescencia is None:
            return self._umbralSenescencia
        else:
            self._umbralSenescencia = umbralSenescencia
            return self


# ====================================================================
# Estadios de cultivo

class EstadioDeCultivo():
    def __init__():
        raise NotImplementedError("Clase abstracta y estática")

    def umbral(planMaestro, *args):
        raise NotImplementedError("Método abstracto")

    def nombre():
        raise NotImplementedError("Método abstracto")


class EstadioGerminacion(EstadioDeCultivo):

    def umbral(planMaestro, *args):
        return planMaestro.umbralGerminacion(*args)

    def nombre():
        return 'GERMINACION'


class EstadioDesarrollo(EstadioDeCultivo):

    def umbral(planMaestro, *args):
        return planMaestro.umbralDesarrollo(*args)

    def nombre():
        return 'DESARROLLO'


class EstadioBrotes(EstadioDeCultivo):

    def umbral(planMaestro, *args):
        return planMaestro.umbralBrotes(*args)

    def nombre():
        return 'BROTES'


class EstadioAparicion(EstadioDeCultivo):

    def umbral(planMaestro, *args):
        return planMaestro.umbralAparicion(*args)

    def nombre():
        return 'APARICION'


class EstadioFloracion(EstadioDeCultivo):

    def umbral(planMaestro, *args):
        return planMaestro.umbralFloracion(*args)

    def nombre():
        return 'FLORACION'


class EstadioFruto(EstadioDeCultivo):

    def umbral(planMaestro, *args):
        return planMaestro.umbralFruto(*args)

    def nombre():
        return 'FRUTO'


class EstadioMaduracion(EstadioDeCultivo):

    def umbral(planMaestro, *args):
        return planMaestro.umbralMaduracion(*args)

    def nombre():
        return 'MADURACION'


class EstadioSenescencia(EstadioDeCultivo):

    def umbral(planMaestro, *args):
        return planMaestro.umbralSenescencia(*args)

    def nombre():
        return 'SENESCENCIA'


# ============================================================
# CicloDeVida

# El ciclo de vida define la secuencia de todos los estadios de
# cultivo.

class CicloDeVida():
    def estadios():
        """Retorna una lista de los estadios del ciclo de vida de la planta,
        en orden

        """
        return [
            EstadioGerminacion,
            EstadioDesarrollo,
            EstadioBrotes,
            EstadioAparicion,
            EstadioFloracion,
            EstadioFruto,
            EstadioMaduracion,
            EstadioSenescencia
        ]


# ====================================================================
# UmbralOptimoDeCultivo

class UmbralOptimoDeCultivo:
    """Un umbral óptimo de cultivo básicamente es una tripla de rangos
    aceptables de T/H/PH para un estadio fenológico dado, que indica
    los umbrales óptimos para estos tres parámetros de la planta
    cuando ésta se encuentra en el estadio fenológico dado. Para
    construirse, requiere un estadio fenológico (una instancia de
    'EstadioFenologico') y tres rangos (instancias de 'Rango'), todos
    estos valores pueden reobtenerse con los métodos estadio(),
    temperatura(), humedad() y acidez().

    """
    def __init__(self, estadio, rangoTemperatura, rangoHumedad, rangoAcidez):
        self._estadio = estadio
        self._temperatura = rangoTemperatura
        self._humedad = rangoHumedad
        self._acidez = rangoAcidez

    def estadio(self):
        return self._estadio

    def temperatura(self):
        return self._temperatura

    def humedad(self):
        return self._humedad

    def acidez(self):
        return self._acidez


# ====================================================================
# mini demo (para correr en la repl)

# Lo que hace es construir un plan maestro con un par de estadios,
# luego imprime todos los datos en la pantalla (mostrando los umbrales
# aceptados de T/H/PH por cada estadio).

def demo():
    from magnitudes import Rango
    from magnitudes import HumedadRelativa, Porcentaje
    from magnitudes import TemperaturaEnCelsius, AcidezEnPH

    def humedadRelativa(x):
        return HumedadRelativa(Porcentaje(x))

    estadio0 = EstadioGerminacion
    estadio1 = EstadioDesarrollo

    temperatura = Rango(TemperaturaEnCelsius(10), TemperaturaEnCelsius(30))
    humedad = Rango(humedadRelativa(40), humedadRelativa(50))
    acidez = Rango(AcidezEnPH(6.5), AcidezEnPH(7.5))

    umbral0 = UmbralOptimoDeCultivo(estadio0, temperatura, humedad, acidez)

    temperatura = Rango(TemperaturaEnCelsius(12), TemperaturaEnCelsius(20))
    humedad = Rango(humedadRelativa(40), humedadRelativa(70))
    acidez = Rango(AcidezEnPH(6.0), AcidezEnPH(7.5))

    umbral1 = UmbralOptimoDeCultivo(estadio1, temperatura, humedad, acidez)

    plan = PlanMaestro([umbral0, umbral1])

    # verifiquemos que el diccionario ande bien
    assert(plan[estadio0] == umbral0)
    assert(plan[estadio1] == umbral1)

    print("los estadios fenologicos definidos son:")
    for estadio in CicloDeVida.estadios():
        print("{}".format(estadio.nombre()))

    # ahora hacemos un print de todo para ver bien los datos
    print("==== plan maestro ====")
    for umbral in plan.umbrales():
        print("estadio : %s" % umbral.estadio().nombre())
        print("rango temperatura : %s~%s" %
              (umbral.temperatura().desde(), umbral.temperatura().hasta()))
        print("rango humedad     : %s~%s" %
              (umbral.humedad().desde(), umbral.humedad().hasta()))
        print("rango acidez (pH) : %s~%s" %
              (umbral.acidez().desde(), umbral.acidez().hasta()))
    print("======================")
    return plan

if __name__ == "__main__":
    plan = demo()               # usá 'plan' en la repl
