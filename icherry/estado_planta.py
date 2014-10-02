# ====================================================================
#                          ESTADO DE PLANTA
# ====================================================================

# En este módulo se definen las clases relacionadas al estado de
# planta. Eso incluye las clases EstadoDePlanta, EstadoFenologico y
# EstadoDeSalud (y subclases).


from icherry.observer import Observable
from icherry.plan_maestro import EstadioGerminacion
from icherry.magnitudes import Porcentaje
from icherry.magnitudes import LongitudEnCentimetros
from icherry.magnitudes import TemperaturaEnCelsius
from icherry.magnitudes import HumedadRelativa
from icherry.magnitudes import AcidezEnPH


# ====================================================================
# EstadoDePlanta

# El estado de la planta consiste en los valores de T/H/PH, el estado
# fenológico y el estado de salud. Todos estos valores internos pueden
# modificarse en cualquier instante. Al instanciarse, se crea un
# estado fenológico por defecto, y las magnitudes T/H/PH con algunos
# valores arbitrarios (recomendamos fuertemente no depender de esto y
# modificarlos ni bien se crea una instancia).

class EstadoDePlanta(Observable):

    def __init__(self):
        super().__init__()

        self._estadoFenologico = EstadoFenologico()
        self._temperatura = TemperaturaEnCelsius(16)
        self._humedad = HumedadRelativa(Porcentaje(0))
        self._acidez = AcidezEnPH(7)
        self._estadoDeSalud = EstadoDeSaludBueno

    def estadoFenologico(self):
        # Si se quiere modificar el estado fenológico, puede
        # obtenérselo primero y luego modificárselo a través de sus
        # setters.
        """Retorna el estado fenológico de la planta."""
        return self._estadoFenologico

    def estadoDeSalud(self, nuevoValor=None):
        """Retorna o modifica el estado de salud de la planta."""
        if nuevoValor is not None:
            self._estadoDeSalud = nuevoValor
            return self
        else:
            return self._estadoDeSalud

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

# El estado de salud básicamente es un identificador utilizado para
# determinar el estado de salud de la planta. Cada estado de salud
# implementa el mensaje 'notificarEstadoA()' que notifica a algún
# objeto que pueda responder a mensajes de respuesta de notificación
# por estado de salud (doble dispatch). Este mecanismo puede servir
# para implementar una alerta si el estado de salud de la planta se
# vuelve crítico.

# La versión actual tiene sólo estados de salud posibles: bueno y
# malo. En versiones futuras se puede expandir. Quienquiera que
# actualice el estado de la planta deberá determinar en base al plan
# maestro y los valores de T/H/PH cuál es el nuevo estado de salud, y
# notificar a los interesados de monitorear esta variable.


class EstadoDeSalud:

    def __init__(self):
        raise NotImplementedError("Clase abstracta y estatica!")

    def nombre():
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

# El estado fenológico consiste en el siguiente conjunto de valores:
#
# * cantidad de brotes
# * cantidad de flores
# * cantidad de frutos
# * porcentaje de frutas maduras
# * estadio de cultivo
# * altura
#
# Todos estos parámetros pueden obtenerse y modificarse en cualquier
# momento. Cuando se inicializa una instancia, el constructor asigna
# valores por defecto a todos los parámetros, lo más parecidos a
# "cero" posibles (las cantidades todas en cero, la altura en 0
# centímetros, etc).

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
