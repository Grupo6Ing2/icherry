import getopt
import sys
import datetime

from icherry.tiempo import FechaYHora
from icherry.central_meteorologica import CentralMeteorologica, PredictorMeteorologicoPorArchivo, ProveedorDeTiempoPorArchivo
from icherry.central_meteorologica import ProveedorDeTiempo
from icherry.central_meteorologica import PredictorMeteorologico
from icherry.dispositivos import DispositivoDeLecturaArchivo
from icherry.parsers import ParserPronosticoMeteorologico, CadenaAFechaYHora


comandosValidos = ['pronostico', 'sensores', 'tiempo']


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

    if cmd is None:
        mensajeAyuda()
        sys.exit()

    predictor = PredictorMeteorologicoPorArchivo(
        DispositivoDeLecturaArchivo("devices/pronostico"))
    reloj = ProveedorDeTiempoPorArchivo(
        DispositivoDeLecturaArchivo("devices/tiempo"))
    central = CentralMeteorologica(predictor, reloj)

    if cmd == 'pronostico':
        horas = 24
        desdeFechaYHora = FechaYHora(datetime.date(2014, 9, 27),
                                     datetime.time(11, 0, 0))
        pronostico = central.obtenerPronostico(desdeFechaYHora, horas)
        t = desdeFechaYHora
        for _ in range(0, horas):
            p = pronostico.prediccionPara(t)
            print(('El pronóstico para {4} es: \n'
                   'Temperatura: {0}, Humedad: {1}, '
                  'Prob. de lluvia: {2}, Luz ambiente: {3}')
                  .format(p.temperatura(),
                          p.humedad(),
                          p.probabilidadDeLluvia(),
                          p.luzAmbiente(), p.lapso()))
            t = t.agregarHoras(1)
    elif cmd == 'sensores':     # TODO
        print("No implementado.")
    elif cmd == 'tiempo':
        t = central.obtenerFechaYHora()
        print(t)

if __name__ == "__main__":
    main(sys.argv[1:])
