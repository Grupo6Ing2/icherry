#Un período temporal
#TODO completar
class Periodo():

    def __init__(self, desde, hasta):
        pass


class Pronostico():

    def __init__(self, periodo, probabilidadDeLLuvia, humedad, temperatura,
                 luzAmbiente):
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
        return Pronostico(periodo,
                          self.__proveedor.probabilidadDeLLuviaPronosticada(periodo),
                          self.__proveedor.humedadPronosticada(periodo),
                          self.__proveedor.temperaturaPronosticada(periodo),
                          self.__proveedor.luzAmbientePronosticada(periodo))


class ProveedorDeDatosMeteorologicos():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def probabilidadDeLLuviaPronosticada(self, periodo):
        raise NotImplementedError("Método abstracto")

    def humedadPronosticada(self, periodo):
        raise NotImplementedError("Método abstracto")

    def temperaturaPronosticada(self, periodo):
        raise NotImplementedError("Método abstracto")

    def luzAmbientePronosticada(self, periodo):
        raise NotImplementedError("Método abstracto")


class Aplicacion():
    def __init__(self, centralMeteorologica):
        self.__centralMeteorologica = centralMeteorologica

    def pronosticoSiguientes24Hs(self):
        #TODO: pasar parametros correctos a Periodo
        return self.__centralMeteorologica.armarPronostico(Periodo(None, None))
