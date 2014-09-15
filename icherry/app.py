class Porcentaje():

    def __init__(self, valor):
        if valor < 0 or valor > 100:
            raise ValueError

        self.__valor = valor

    def valor(self):
        return self.__valor

    def __str__(self):
        return '{0}%'.format(self.__valor)

    def __eq__(self, otro):
        return self.__valor == otro.valor()


#Medida de luz
#http://es.wikipedia.org/wiki/Lux
class Lux():

    def __init__(self, valor):
        self.__valor = valor

    def valor(self):
        return self.__valor

    def __str__(self):
        return '{0}Lx'.format(self.__valor)

    def __eq__(self, otro):
        return self.__valor == otro.valor()


#Un periodo temporal
#TODO completar
class Periodo():

    def __init__(self, desde, hasta):
        pass


class Pronostico():

    def __init__(self, periodo, probabilidadDeLLuvia, humedad, temperatura, luzAmbiente):
        self.__periodo = periodo
        self.__probabilidadDeLLuvia = probabilidadDeLLuvia
        self.__humedad = humedad
        self.__temperatura = temperatura
        self.__luzAmbiente = luzAmbiente

    def periodo(self):
        return self.__periodo

    def probabilidadDeLluvia(self):
        return self.__probabilidadDeLLuvia

    def humedad(self):
        return self.__humedad

    def temperatura(self):
        return self.__temperatura

    def luzAmbiente(self):
        return self.__luzAmbiente


class CentralMeteorologica():
    def __init__(self, proveedorDeDatosMeteorologicos):
        self.__proveedor = proveedorDeDatosMeteorologicos

    def armarPronostico(self, periodo):
        return Pronostico(periodo, self.__proveedor.probabilidadDeLLuviaPronosticada(periodo),
                     self.__proveedor.humedadPronosticada(periodo),
                     self.__proveedor.temperaturaPronosticada(periodo),
                     self.__proveedor.luzAmbientePronosticada(periodo))


class ProveedorDeDatosMeteorologicos():

    def __init__(self):
        raise NotImplementedError('Clase abstracta')

    def probabilidadDeLLuviaPronosticada(self, periodo):
        raise NotImplementedError('Metodo abstracto')

    def humedadPronosticada(self, periodo):
        raise NotImplementedError('Metodo abstracto')

    def temperaturaPronosticada(self, periodo):
        raise NotImplementedError('Metodo abstracto')

    def luzAmbientePronosticada(self, periodo):
        raise NotImplementedError('Metodo abstracto')


class Applicacion():
    def __init__(self, centralMeteorologica):
        self.__centralMeteorologica = centralMeteorologica

    def pronosticoSiguientes24Hs(self):
        #TODO: pasar parametros correctos a Periodo
        return self.__centralMeteorologica.armarPronostico(Periodo(None, None))
