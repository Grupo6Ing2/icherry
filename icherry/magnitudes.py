# ====================================================================
#                             MAGNITUDES
# ====================================================================

# Definición de magnitudes de uso común (líquido, luz, temperatura,
# acidez, porcentaje, humedad).

# En general se cuenta con una clase abstracta para cada una, y una
# implementación concreta (podría haber más de una), en general son
# todas muy sencillas y más bien la idea es contar con un correlato
# del diseño que con clases que implementen mucha funcionalidad.
# Básicamente todas las magnitudes tienen un método 'valor' que
# devuelve el valor con el que se construyeron, la unidad debería ser
# conocida por el llamador.
#
# Se implementan también operadores de comparación para tipos
# compatibles.

# ====================================================================
class Magnitud :
    """Una magnitud es algo que responde al mensaje 'valor' retornando un
    número, y que soporta comparación aritmética (como facilidad
    adicional) con otros objetos compatibles.

    """
    def __init__(self) :
        raise NotImplementedError("Clase abstracta")
    def valor(self) :
        raise NotImplementedError("Método abstracto")
    def _compatibilizar(self, otro) :
        raise NotImplementedError("Método abstracto")
    def __lt__(self, otro) :
        return self.valor() < self._compatibilizar(otro).valor()
    def __le__(self, otro) :
        return self.valor() <= self._compatibilizar(otro).valor()
    def __eq__(self, otro) :
        return self.valor() == self._compatibilizar(otro).valor()
    def __ne__(self, otro) :
        return self.valor() != self._compatibilizar(otro).valor()
    def __gt__(self, otro) :
        return self.valor() >  self._compatibilizar(otro).valor()
    def __ge__(self, otro) :
        return self.valor() >= self._compatibilizar(otro).valor()
    # WARNING : estos comparadores sólo permiten comparar tipos
    # compatibles. Por ejemplo, si se compara una temperatura en
    # fahrenheit contra una en celcius, funciona (pues son
    # compatibles), pero falla por ejemplo al comparar litros con lux
    # (incompatibles). Este esquema requiere que sólo el segundo
    # operando se convierta, pero tiene la desventaja de que cada uno
    # de N tipos compatibles debe saber convertirse a los N-1
    # restantes, una alternativa sería hacer que haya un tipo canónico
    # y que ambos operandos se conviertan a ése (cada uno de los N
    # tipos sólo sabe convertirse al canónico).

# ====================================================================
# Líquido
class Liquido(Magnitud) :
    def aLitros(self) :
        raise NotImplementedError("Método abstracto")
    def aMililitros(self) :
        raise NotImplementedError("Método abstracto")

class LiquidoEnMililitros(Liquido) :
    def __init__(self, mililitros) :
        self._valor = mililitros

    def valor(self) :
        return self._valor

    def __str__(self) :
        return "{0}ml".format(self.valor())

    def aLitros(self) :
        return LiquidoEnLitros(self.valor() / 1000)

    def aMililitros(self) :
        return self

    def _compatibilizar(self, otraMagnitud) :
        return otraMagnitud.aMililitros()

class LiquidoEnLitros(Liquido) :
    def __init__(self, mililitros) :
        self._valor = mililitros

    def valor(self) :
        return self._valor

    def __str__(self) :
        return "{0}l".format(self.valor())

    def aLitros(self) :
        return self

    def aMililitros(self) :
        return LiquidoEnMililitros(self.valor() * 1000)

    def _compatibilizar(self, otraMagnitud) :
        return otraMagnitud.aLitros()

# ====================================================================
# Luz
class Luz(Magnitud) :
    def aLux(self) :
        raise NotImplementedError("Método abstracto")

class LuzEnLux(Luz) :
    def __init__(self,lux) :
        self._valor = lux

    def valor(self) :
        return self._valor

    def aLux(self) :
        return self

    def _compatibilizar(self, otraMagnitud) :
        return otraMagnitud.aLux()

    def __str__(self):
        return '{0}lx'.format(self.valor())

# ====================================================================
# Temperatura

class Temperatura(Magnitud) :
    def aCelsius(self) :
        raise NotImplementedError("Método abstracto")
    def aFahrenheit(self) :
        raise NotImplementedError("Método abstracto")

class TemperaturaEnCelsius(Temperatura) :
    def __init__(self,celsius) :
        self._valor = celsius

    def valor(self) :
        return self._valor

    def __str__(self) :
        return "{0}°C".format(self.valor())

    def aCelsius(self) :
        return self

    def aFahrenheit(self) :
        return TemperaturaEnFahrenheit(self.valor() * 1.8 + 32.0)

    def _compatibilizar(self, otraMagnitud) :
        return otraMagnitud.aCelsius()

class TemperaturaEnFahrenheit(Temperatura) :
    def __init__(self,celsius) :
        self._valor = celsius

    def valor(self) :
        return self._valor

    def __str__(self) :
        return "{0}°F".format(self.valor())

    def aCelsius(self) :
        return TemperaturaEnCelsius((self.valor() - 32.0) / 1.8)

    def aFahrenheit(self) :
        return self

    def _compatibilizar(self, otraMagnitud) :
        return otraMagnitud.aFahrenheit()

# ====================================================================
# Acidez
class Acidez(Magnitud) :
    def aPH(self) :
        raise NotImplementedError("Método abstracto")

class AcidezEnPH(Acidez) :
    def __init__(self,numero) :
        # los valores válidos de pH son en el intervalo [0..14]
        if numero < 0 or numero > 14:
            raise ValueError("el pH debe estar entre 0 y 14")

        self._valor = numero

    def valor(self) :
        return self._valor

    def aPH(self) :
        return self

    def __str__(self) :
        #el pH es adimensional
        return str(self.valor())

    def _compatibilizar(self, otraMagnitud) :
        return otraMagnitud.aPH()

# ====================================================================
# Ratio (Porcentaje)

class Ratio(Magnitud) :
    def aPorcentaje(self) :
        raise NotImplementedError("Método abstracto")

class Porcentaje(Ratio) :
    def __init__(self, numero):
        if numero < 0 or numero > 100:
            raise ValueError("el número debe estar entre 0 y 100")
        self._valor = numero

    def valor(self) :
        return self._valor

    def aPorcentaje(self) :
        return self

    def _compatibilizar(self, otraMagnitud) :
        return otraMagnitud.aPorcentaje()

    def __str__(self):
        return '{0}%'.format(self.valor())

# ====================================================================
# Humedad

# Nota: la humedad se construye con un ratio (porcentaje) en esta
# versión.

class Humedad(Magnitud) :
    def aHumedadRelativa(self) :
        raise NotImplementedError("Método abstracto")

class HumedadRelativa(Humedad) :
    # el valor de la humedad relativa es un ratio. Sin embargo lo
    # canonizamos a porcentaje internamente. Contamos con esto por
    # ejemplo para el método de conversión a string, que le delegamos
    # al porcentaje (o sea, la humedad y el porcentaje hacen 'str'
    # igual). Otra opción es pedir el valor() y hacerle 'str' a eso.
    def __init__(self,unRatio) :
        self._valor = unRatio.aPorcentaje() #canonizamos a porcentaje
    def valor(self) :
        return self._valor
    def aHumedadRelativa(self) :
        return self
    def _compatibilizar(self, otraMagnitud) :
        return otraMagnitud.aHumedadRelativa()
    def __str__(self) :
        return str(self.valor())
