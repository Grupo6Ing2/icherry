# ====================================================================
#                          ESTADO DE SALUD
# ====================================================================

from icherry.observer import Observable
from icherry.plan_maestro import EstadioGerminacion
from icherry.magnitudes import Porcentaje
from icherry.magnitudes import LongitudEnCentimetros
from icherry.magnitudes import TemperaturaEnCelsius
from icherry.magnitudes import HumedadRelativa
from icherry.magnitudes import AcidezEnPH

# ====================================================================
# EstadoDePlanta
class EstadoDePlanta(Observable):

    def __init__(self):
        self._estadoFenologico = EstadoFenologico()
        self._temperatura = TemperaturaEnCelsius(0)
        self._humedad = HumedadRelativa(Porcentaje(0))
        self._acidez = AcidezEnPH(0)
        self._estadoDeSalud = EstadoDeSaludBueno

    def estadoFenologico(self):
        """Retorna el estado fenológico de la planta."""
        return self._estadoFenologico

    def estadoDeSalud(self, nuevoValor=None):
        """Retorna o modifica el estado de salud de la planta."""
        if nuevoValor is not None:
            self._estadoSalud = nuevoValor
            return self
        else:
            return self._estadoSalud

    # definimos ahora getters/setters para T/H/PH. Cada método puede
    # usarse tanto como getter (sin argumentos) o setter (con
    # argumento para modificar el valor actual). Los métodos retornan
    # 'self' al usarse como setters.

    def temperatura(self, nuevoValor=None):
        if nuevoValor is not None:
            self._temperatura = nuevoValor
            return self
        else:
            return self._temperatura

    def humedad(self, nuevoValor=None):
        if nuevoValor is not None:
            self._humedad = nuevoValor
            return self
        else:
            return self._humedad

    def acidez(self, nuevoValor=None):
        if nuevoValor is not None:
            self._acidez = nuevoValor
            return self
        else:
            return self._acidez


# ====================================================================
# EstadoDeSalud

class EstadoDeSalud:
    def __init__(self):
        raise NotImplementedError("Clase abstracta")
    def nombre(self):
        raise NotImplementedError("Método abstracto")
    def notificarEstadoA():
        raise NotImplementedError("Método abstracto")

class EstadoDeSaludBueno(EstadoDeSalud):
    def nombre():
        return 'BUENO'
    def notificarEstadoA(notificado):
        notificado.notificarseEstadoBueno()

class EstadoDeSaludMalo(EstadoDeSalud):
    def nombre():
        return 'MALO'
    def notificarEstadoA(notificado):
        notificado.notificarseEstadoMalo()

# ====================================================================
# EstadoFenologico
class EstadoFenologico:
    def __init__(self):
        """inicializa un estado fenologico a partir de valores por defecto
        (todos cero).
        """

        self._cantidadBrotes = 0
        self._cantidadFlores = 0
        self._cantidadFrutos = 0
        self._porcentajeFrutasMaduras = Porcentaje(0)
        self._estadioDeCultivo = EstadioGerminacion
        self._altura = LongitudEnCentimetros(0)

    # definimos ahora getters/setters para cada cantidad, con la misma
    # convención que en EstadoDePlanta.

    def cantidadBrotes(self, nuevoValor=None):
        if nuevoValor is not None:
            self._cantidadBrotes = nuevoValor
            return self
        else:
            return self._cantidadBrotes

    def cantidadFlores(self, nuevoValor=None):
        if nuevoValor is not None:
            self._cantidadFlores = nuevoValor
            return self
        else:
            return self._cantidadFlores

    def cantidadFrutos(self, nuevoValor=None):
        if nuevoValor is not None:
            self._cantidadFrutos = nuevoValor
            return self
        else:
            return self._cantidadFrutos

    def porcentajeFrutasMaduras(self, nuevoValor=None):
        if nuevoValor is not None:
            self._porcentajeFrutasMaduras = nuevoValor
            return self
        else:
            return self._porcentajeFrutasMaduras

    def estadioDeCultivo(self, nuevoValor=None):
        if nuevoValor is not None:
            self._estadioDeCultivo = nuevoValor
            return self
        else:
            return self._estadioDeCultivo

    def altura(self, nuevoValor=None):
        if nuevoValor is not None:
            self._altura = nuevoValor
            return self
        else:
            return self._altura
