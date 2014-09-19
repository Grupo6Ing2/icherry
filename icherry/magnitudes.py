# ====================================================================
#                             MAGNITUDES
# ====================================================================

# Definición de magnitudes de uso común (líquido, luz, temperatura y
# acidez).

# En general se cuenta con una clase abstracta para cada una, y una
# implementación concreta (podría haber más de una), en general son
# todas muy sencillas y más bien la idea es contar con un correlato
# del diseño que con clases que implementen mucha funcionalidad.
# Básicamente todas las magnitudes tienen un método 'valor' que
# devuelve el número con el que se construyeron, la unidad debería ser
# conocida por el llamador.
#
# No se proveen funciones de {comparación,conversión,aritmética,etc},
# eso debe hacerse en forma externa con los valores obtenidos por
# 'valor'.

# ====================================================================
# Líquido
class Liquido :
    def __init__(self) :
        raise NotImplementedError("Clase abstracta")
    def valor(self) :
        raise NotImplementedError("Método abstracto")

class LiquidoEnMililitros(Liquido) :
    def __init__(self, mililitros) :
        self.valor = mililitros

    def valor(self) :
        return self.valor

    def __str__(self):
        return "{0}ml".format(self.valor)

class LiquidoEnLitros(Liquido) :
    pass #TODO, opcional

# ====================================================================
# Luz
class Luz :
    def __init__(self) :
        raise NotImplementedError("Clase abstracta")
    def valor(self) :
        raise NotImplementedError("Método abstracto")

class LuzEnLux(Luz) :
    def __init__(self,lux) :
        self.valor = lux

    def valor(self) :
        return self.valor

    def __str__(self):
        return '{0}lx'.format(self.__valor)

# ====================================================================
# Temperatura
class Temperatura() :
    def __init__(self) :
        raise NotImplementedError("Clase abstracta")
    def valor(self) :
        raise NotImplementedError("Método abstracto")

class TemperaturaEnCelsius(Temperatura) :
    def __init__(self,celsius) :
        self.valor = celsius

    def valor(self) :
        return self.valor

    def __str__(self):
        return "{0}°C".format(self.valor)

class TemperaturaEnFahrenheit(Temperatura) :
    pass #TODO, opcional

# ====================================================================
# Acidez
class Acidez() :
    def __init__(self) :
        raise NotImplementedError("Clase abstracta")
    def valor(self) :
        raise NotImplementedError("Método abstracto")

class AcidezEnPH(Acidez) :
    def __init__(self,numero) :
        # los valores válidos de pH son en el intervalo [0..14]
        if numero < 0 or numero > 14:
            raise ValueError("el pH debe estar entre 0 y 14")

        self.valor = numero

    def valor(self) :
        return self.valor

    def __str__(self) :
        #el pH es adimensional
        return str(self.valor)
