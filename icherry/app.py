#coding=utf-8

from icherry.central_meteorologica import *



class Aplicacion():
    def __init__(self, centralMeteorologica):
        self.__centralMeteorologica = centralMeteorologica

    def pronosticoSiguientes24Hs(self):
        pass
        #TODO: pasar parametros correctos a Periodo
        #return self.__centralMeteorologica.armarPronostico(Periodo(None, None))
