# coding=utf-8
# ====================================================================
#                             MAGNITUDES
# ====================================================================

# Definición de magnitud y algunas magnitudes de uso común (líquido,
# luz, temperatura, acidez, porcentaje, humedad). Además, se define un
# 'Rango' de valores. No todas las magnitudes se definen acá,
# sólamente las relacionadas a T/H/PH (a modo de ejemplo), pero otros
# archivos podrían definir sus propias magnitudes.

# En general se cuenta con una clase abstracta para cada magnitud, y
# una implementación concreta (podría haber más de una), en general
# son todas muy sencillas y más bien la idea es contar con un
# correlato del diseño que con clases que implementen mucha
# funcionalidad. Básicamente todas las magnitudes tienen un método
# 'valor' que devuelve el valor con el que se construyeron, la unidad
# debería ser conocida por el llamador.
#
# Dos instancias de magnitud son 'compatibles' si miden la misma
# magnitud física, diferenciándose tal vez en las unidades implícitas
# con las que fueron construidas, por ejemplo las magnitudes de
# volumen líquido son compatibles, pero una magnitud de volumen
# líquido es incompatible con una magnitud de temperatura.
#
# Las magnitudes compatibles pueden convertirse entre sí. Por ejemplo,
# si una función espera una temperatura, no interesa si es en celsius
# o fahrenheit, siempre puede convertirse a la unidad deseada y luego
# extraer su valor numérico con el método 'valor'.
#
# Se implementan también operadores de comparación para tipos
# compatibles, con lo cual 'LiquidoEnMililitros(1000)' es igual a
# 'LiquidoEnLitros(1)' por ejemplo.

# ====================================================================


class Magnitud:

    """Una magnitud es algo que responde al mensaje 'valor' retornando un
    número, y que soporta comparación aritmética (como facilidad
    adicional) con otros objetos compatibles.

    """

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def valor(self):
        raise NotImplementedError("Método abstracto")

    def _compatibilizar(self, otro):
        raise NotImplementedError("Método abstracto")

    def __lt__(self, otro):
        return self.valor() < self._compatibilizar(otro).valor()

    def __le__(self, otro):
        return self.valor() <= self._compatibilizar(otro).valor()

    def __eq__(self, otro):
        return self.valor() == self._compatibilizar(otro).valor()

    def __ne__(self, otro):
        return self.valor() != self._compatibilizar(otro).valor()

    def __gt__(self, otro):
        return self.valor() > self._compatibilizar(otro).valor()

    def __ge__(self, otro):
        return self.valor() >= self._compatibilizar(otro).valor()
    # NOTICE : Este esquema requiere que sólo el segundo operando se
    # convierta, pero tiene la desventaja de que cada uno de N tipos
    # compatibles debe saber convertirse a los N-1 restantes, una
    # alternativa sería hacer que haya un tipo canónico y que ambos
    # operandos se conviertan a ése (cada uno de los N tipos sólo sabe
    # convertirse al canónico). La desventaja es que se pierde la
    # independencia de unidad.

# ====================================================================
# Líquido


class Liquido(Magnitud):

    def aLitros(self):
        raise NotImplementedError("Método abstracto")

    def aMililitros(self):
        raise NotImplementedError("Método abstracto")


class LiquidoEnMililitros(Liquido):

    def __init__(self, mililitros):
        self._valor = mililitros

    def valor(self):
        return self._valor

    def __str__(self):
        return "{0}ml".format(self.valor())

    def aLitros(self):
        return LiquidoEnLitros(self.valor() / 1000)

    def aMililitros(self):
        return self

    def _compatibilizar(self, otraMagnitud):
        return otraMagnitud.aMililitros()


class LiquidoEnLitros(Liquido):

    def __init__(self, litros):
        self._valor = litros

    def valor(self):
        return self._valor

    def __str__(self):
        return "{0}l".format(self.valor())

    def aLitros(self):
        return self

    def aMililitros(self):
        return LiquidoEnMililitros(self.valor() * 1000)

    def _compatibilizar(self, otraMagnitud):
        return otraMagnitud.aLitros()

# ====================================================================
# Luz


class Luz(Magnitud):

    def aLux(self):
        raise NotImplementedError("Método abstracto")


class LuzEnLux(Luz):

    def __init__(self, lux):
        self._valor = lux

    def valor(self):
        return self._valor

    def aLux(self):
        return self

    def _compatibilizar(self, otraMagnitud):
        return otraMagnitud.aLux()

    def __str__(self):
        return '{0}lx'.format(self.valor())

# ====================================================================
# Temperatura


class Temperatura(Magnitud):

    def aCelsius(self):
        raise NotImplementedError("Método abstracto")

    def aFahrenheit(self):
        raise NotImplementedError("Método abstracto")


class TemperaturaEnCelsius(Temperatura):

    def __init__(self, celsius):
        self._valor = celsius

    def valor(self):
        return self._valor

    def __str__(self):
        return "{0}°C".format(self.valor())

    def aCelsius(self):
        return self

    def aFahrenheit(self):
        return TemperaturaEnFahrenheit(self.valor() * 1.8 + 32.0)

    def _compatibilizar(self, otraMagnitud):
        return otraMagnitud.aCelsius()


class TemperaturaEnFahrenheit(Temperatura):

    def __init__(self, celsius):
        self._valor = celsius

    def valor(self):
        return self._valor

    def __str__(self):
        return "{0}°F".format(self.valor())

    def aCelsius(self):
        return TemperaturaEnCelsius((self.valor() - 32.0) / 1.8)

    def aFahrenheit(self):
        return self

    def _compatibilizar(self, otraMagnitud):
        return otraMagnitud.aFahrenheit()

# ====================================================================
# Acidez


class Acidez(Magnitud):

    def aPH(self):
        raise NotImplementedError("Método abstracto")


class AcidezEnPH(Acidez):

    def __init__(self, numero):
        # los valores válidos de pH son en el intervalo [0..14]
        if numero < 0 or numero > 14:
            raise ValueError("el pH debe estar entre 0 y 14")

        self._valor = numero

    def valor(self):
        return self._valor

    def aPH(self):
        return self

    def __str__(self):
        # el pH es adimensional
        return str(self.valor())

    def _compatibilizar(self, otraMagnitud):
        return otraMagnitud.aPH()

# ====================================================================
# Ratio (Porcentaje)


class Ratio(Magnitud):

    def aPorcentaje(self):
        raise NotImplementedError("Método abstracto")


class Porcentaje(Ratio):

    def __init__(self, numero):
        if numero < 0 or numero > 100:
            raise ValueError("el número debe estar entre 0 y 100")
        self._valor = numero

    def valor(self):
        return self._valor

    def aPorcentaje(self):
        return self

    def _compatibilizar(self, otraMagnitud):
        return otraMagnitud.aPorcentaje()

    def __str__(self):
        return '{0}%'.format(self.valor())

# ====================================================================
# Humedad

# Nota: la humedad se construye con un ratio (porcentaje) en esta
# versión.


class Humedad(Magnitud):

    def aHumedadRelativa(self):
        raise NotImplementedError("Método abstracto")


class HumedadRelativa(Humedad):
    # el valor de la humedad relativa es un ratio. Sin embargo lo
    # canonizamos a porcentaje internamente. Contamos con esto por
    # ejemplo para el método de conversión a string, que le delegamos
    # al porcentaje (o sea, la humedad y el porcentaje hacen 'str'
    # igual). Otra opción es pedir el valor() y hacerle 'str' a eso.

    def __init__(self, unRatio):
        self._valor = unRatio.aPorcentaje()  # canonizamos a porcentaje

    def valor(self):
        return self._valor

    def aHumedadRelativa(self):
        return self

    def _compatibilizar(self, otraMagnitud):
        return otraMagnitud.aHumedadRelativa()

    def __str__(self):
        return str(self.valor())

# ====================================================================
# Longitud


class Longitud(Magnitud):

    def aCentimetros(self):
        raise NotImplementedError("Método abstracto")


class LongitudEnCentimetros(Longitud):

    def __init__(self, centimetros):
        self._valor = centimetros

    def valor(self):
        return self._valor

    def _compatibilizar(self, otraMagnitud):
        return otraMagnitud.aCentimetros()

    def aCentimetros(self):
        return self

    def __str__(self):
        return str(self.valor()) + "cm"

# ====================================================================
# Rango

# NOTICE: Un rango no es una magnitud ni necesariamente tiene límites
# de tipo magnitud, pero en muchos casos vamos a usar rangos de
# magnitudes, por ejemplo un rango de temperaturas o un rango de
# humedades, y por eso esta clase se aloja en este archivo que define
# a la 'Magnitud' y a otras magnitudes comunes. El concepto de
# 'Lapso', que apareció varias veces en el diseño, no es otra cosa que
# un rango de tiempos (fecha/hora). Ver el docstring de la clase para
# más detalles.


class Rango:

    """Un rango de valores (intervalo en el sentido de teoría de
    conjuntos), se construye a partir de un par de límites (inferior y
    superior). Lo único que se requiere es que el límite inferior sea
    menor o igual al superior (lo cual a su vez requiere que ambos
    sean comparables con '<=').

    """

    def __init__(self, desde, hasta):
        """construye un rango a partir de límites inferior y superior"""
        assert(desde <= hasta)
        self._tupla = (desde,hasta)

    def desde(self):
        """retorna el límite inferior"""
        return self._tupla[0]

    def hasta(self):
        """retorna el límite superior"""
        return self._tupla[1]

    def contiene(self, valor):
        """determina si un valor está contenido en el rango"""
        return self.desde() <= valor <= self.hasta()

    def interseca(self, otro):
        """determina si el rango se interseca con otro rango. Es una relación
        reflexiva y simétrica (pero no necesariamente transitiva).

        """
        if otro.contiene(self.desde()): return True
        if self.contiene(otro.desde()): return True
        return False

    def __eq__(self, otroRango):
        return self.desde() == otroRango.desde() and \
            self.hasta() == otroRango.hasta()

    def __ne__(self, otroRango):
        return not self.__eq__(otroRango)

    def __hash__(self):
        return self._tupla.__hash__()

    def __str__(self):
        return "[{0} - {1}]".format(self.desde(), self.hasta())
