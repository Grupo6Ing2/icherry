# ====================================================================
#                            PLAN MAESTRO
# ====================================================================

# Se definen los conceptos relacionados con el plan maestro : estadio
# fenológico, umbral óptimo de cultivo y plan maestro.


# ====================================================================
# Rango

# TODO: mover esto a otro lado, no debería ir en este archivo.

# NOTICE: esto es _muy_ parecido al 'Intervalo' que aparece dando
# vueltas en app.py, creo que se podría implementar/reemplazar el
# intervalo usando esto.
class Rango:
    """Un rango de valores (intervalo en el sentido de teoría de
    conjuntos), se construye a partir de un par de límites (inferior y
    superior). Lo único que se requiere es que el límite inferior sea
    menor o igual al superior (lo cual a su vez requiere que ambos
    sean comparables con '<=').

    """
    def __init__(self, desde, hasta) :
        """construye un rango a partir de límites inferior y superior"""
        assert( desde <= hasta )
        self._desde = desde
        self._hasta = hasta
    def desde(self):
        """retorna el límite inferior"""
        return self._desde
    def hasta(self):
        """retorna el límite superior"""
        return self._hasta
    def contiene(self, valor) :
        """determina si un valor está contenido en el rango"""
        return self.desde() <= valor <= self.hasta()

# ====================================================================
# EstadioFenologico

# niñooos : se dice "estadio", no "estadío" (no existe esa palabra).
# http://www.fundeu.es/recomendacion/estadio-no-estadio-1265/
# http://lema.rae.es/drae/?val=estad%C3%ADo

class EstadioFenologico:
    """Un 'EstadioFenologico' es básicamente un mero identificador de
    estadio fenológico, no tiene demasiado interés per sé, sino más
    bien para usarse como índice en un plan maestro. En esta versión
    cuenta con un identificador y un nombre (la idea es que estos
    valores sean únicos en el plan maestro en que aparezcan).

    """
    def __init__(self, id, nombre) :
        """construye un estadio fenológico a partir de un identificador y un
        nombre. El identificador puede ser un número, el nombre
        debería ser un string (usado a modo de símbolo)
        """
        self._id = id
        self._nombre = nombre
        # la función 'id' en python existe, pero no conflictúa con
        # este uso. Si 'e0' es una instancia de 'EstadioFenologico',
        # id(e0) y e0.id() son dos cosas distintas.
    def id(self):
        return self._id
    def nombre(self):
        return self._nombre
    #usamos la comparación por default, o sea, miembro a miembro (dos
    #instancias serán iguales cuando tanto el identificador como el
    #nombre sean iguales), esto sirve por ahora. A pesar de eso, en un
    #plan maestro los estadios no deberían tener identificadores
    #repetidos ni nombres repetidos.

# por practicidad, generamos todos los estadios posibles acá
estadios = {'GERMINACION' : EstadioFenologico(0,'GERMINACION'),
            'DESARROLLO'  : EstadioFenologico(1,'DESARROLLO'),
            'BROTES'      : EstadioFenologico(2,'BROTES'),
            'APARICION'   : EstadioFenologico(3,'APARICION'),
            'FLORACION'   : EstadioFenologico(4,'FLORACION'),
            'FRUTO'       : EstadioFenologico(5,'FRUTO'),
            'MADURACION'  : EstadioFenologico(6,'MADURACION'),
            'SENESCENCIA' : EstadioFenologico(7,'SENESCENCIA')}

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
    def __init__(self,estadio,rangoTemperatura,rangoHumedad,rangoAcidez) :
        self._estadio     = estadio
        self._temperatura = rangoTemperatura
        self._humedad     = rangoHumedad
        self._acidez      = rangoAcidez

    def estadio(self):
        return self._estadio
    def temperatura(self):
        return self._temperatura
    def humedad(self):
        return self._humedad
    def acidez(self):
        return self._acidez

# ====================================================================
# PlanMaestro
class PlanMaestro :
    """Un plan maestro es un diccionario de estado fenológico en umbral
    óptimo de cultivo. Con el plan maestro sabemos en qué parámetros
    de T/H/PH se debe mantener la planta en el estadio actual. Para
    construirse, requiere una lista de umbrales óptimos de cultivo
    (que no se solapen, es decir no haya dos que correspondan al mismo
    estadio).

    """
    def __init__(self, umbrales) :
        """construye un plan maestro a partir de una colección de umbrales"""
        self._umbrales = dict([(u.estadio(),u) for u in umbrales])
        #si había umbrales distintos con el mismo estadio, sólo uno de ellos
        #quedará asociado (pero no debería construirse con una lista así)
    def umbralParaEstadio(self, estadio) :
        """retorna el umbral asociado al estadio dado"""
        return self._umbrales[ estadio ]
    def umbrales(self) :
        """retorna la lista de todos los umbrales que planifica"""
        return [umbral for umbral in self._umbrales.values()]



# ====================================================================
# mini demo (para correr en la repl)

# Lo que hace es construir un plan maestro con un par de estadios,
# luego imprime todos los datos en la pantalla (mostrando los umbrales
# aceptados de T/H/PH por cada estadio).

def demo():
    from magnitudes import HumedadRelativa, Porcentaje
    from magnitudes import TemperaturaEnCelsius, AcidezEnPH
    def humedadRelativa(x) :
        return HumedadRelativa(Porcentaje(x))

    e0 = estadios['GERMINACION']
    e1 = estadios['DESARROLLO']

    temperatura = Rango(TemperaturaEnCelsius(10),TemperaturaEnCelsius(30))
    humedad = Rango(humedadRelativa(40),humedadRelativa(50))
    acidez = Rango(AcidezEnPH(6.5),AcidezEnPH(7.5))

    umbral0 = UmbralOptimoDeCultivo(e0,temperatura,humedad,acidez)

    temperatura = Rango(TemperaturaEnCelsius(12),TemperaturaEnCelsius(20))
    humedad = Rango(humedadRelativa(40),humedadRelativa(70))
    acidez = Rango(AcidezEnPH(6.0),AcidezEnPH(7.5))

    umbral1 = UmbralOptimoDeCultivo(e1,temperatura,humedad,acidez)

    plan = PlanMaestro([umbral0,umbral1])

    # verifiquemos que el diccionario ande bien
    assert( plan.umbralParaEstadio(e0) == umbral0 )
    assert( plan.umbralParaEstadio(e1) == umbral1 )

    # ahora hacemos un print de todo para ver bien los datos
    print( "==== plan maestro ====")
    for umbral in plan.umbrales() :
        print("estadio : %s" % umbral.estadio().nombre())
        print("rango temperatura : %s~%s" %
              (umbral.temperatura().desde(),umbral.temperatura().hasta()))
        print("rango humedad     : %s~%s" %
              (umbral.humedad().desde(), umbral.humedad().hasta()))
        print("rango acidez (pH) : %s~%s" %
              (umbral.acidez().desde(), umbral.acidez().hasta()))
    print( "======================" )
    return plan

if __name__ == "__main__" : plan = demo() # usá 'plan' en la repl
