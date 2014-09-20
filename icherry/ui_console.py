import random
import getopt
import sys

from app import ProveedorDeDatosMeteorologicos, CentralMeteorologica
from app import Aplicacion
from magnitudes import Porcentaje,TemperaturaEnCelsius,HumedadRelativa,LuzEnLux

class ProveedorDeDatosMeteorologicosAleatorio(ProveedorDeDatosMeteorologicos):
    def __init__(self, rnd):
        self.__rnd = rnd

    def probabilidadDeLLuviaPronosticada(self, periodo):
        return Porcentaje(self.__rnd.randint(0, 100))

    def humedadPronosticada(self, periodo):
        return HumedadRelativa(Porcentaje(self.__rnd.randint(0, 100)))

    def temperaturaPronosticada(self, periodo):
        return TemperaturaEnCelsius(self.__rnd.randint(-5, 30))

    def luzAmbientePronosticada(self, periodo):
        return LuzEnLux(self.__rnd.randint(0, 1000))



comandosValidos = ['pronostico', 'sensores']

def mensajeAyuda():
    print('ui_console.py -c <comando>')
    print('<comando> = {0}'.format(' | '.join(comandosValidos)))


def main(argv):
    cmd = None

    try:
        opts, args = getopt.getopt(argv, "hc:")
    except getopt.GetoptError:
        mensajeAyuda()
        sys.exit()

    for opt, arg in opts:
        if opt == '-c' and arg in comandosValidos:
            cmd = arg
        else:
            mensajeAyuda()
            sys.exit()

    if cmd == None:
        mensajeAyuda()
        sys.exit()

    central = CentralMeteorologica(ProveedorDeDatosMeteorologicosAleatorio(random.Random()))
    app = Aplicacion(central)

    if cmd == 'pronostico':
        pronostico = app.pronosticoSiguientes24Hs()
        print(('El pronóstico para las siguientes 24hs es: \nTemperatura: {0}, Humedad: {1}, '
              'Prob. de lluvia: {2}, Luz ambiente: {3}').format(pronostico.temperatura(),
                                                                pronostico.humedad(),
                                                                pronostico.probabilidadDeLluvia(),
                                                                pronostico.luzAmbiente()))
    #TODO poner el cmd 'sensores' cuando estén los sensores.
    #por ahora no hay nada de código de sensores, así que habrá que esperar.


if __name__ == "__main__":
   main(sys.argv[1:])
