# ====================================================================
#                          ESTADO DE SALUD
# ====================================================================
from icherry.plan_maestro import EstadiosFenologicos
from icherry.magnitudes import Porcentaje
from icherry.magnitudes import LongitudEnCentimetros
from icherry.magnitudes import TemperaturaEnCelsius
from icherry.magnitudes import HumedadRelativa
from icherry.magnitudes import AcidezEnPH


# ====================================================================
# EstadoDeSalud
class EstadoDeSalud:
    def __init__(self):
        self.estadoFenologico = EstadoFenologico()
        self._temperatura = TemperaturaEnCelsius(0)
        self._humedad = HumedadRelativa(Porcentaje(0))
        self._acidez = AcidezEnPH(0)

    def estadoFenologico(self):
        return self.estadoFenologico

    # definimos ahora getters/setters para T/H/PH. Cada método puede
    # usarse tanto como getter (sin argumentos) o setter (con
    # argumento para modificar el valor actual). Los método retornan
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
        self._estadioDeCultivo = EstadiosFenologicos.germinacion()
        self._altura = LongitudEnCentimetros(0)

    # definimos ahora getters/setters para cada cantidad, con la misma
    # convencion que en EstadoDeSalud.

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
