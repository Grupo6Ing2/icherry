# coding=utf-8
import icherry.sensores as sensores
import icherry.magnitudes as magnitudes
import icherry.dispositivos as dispositivos
import icherry.parsers as parsers
import icherry.actuadores as actuadores
import icherry.ui_ncurses as ui_ncurses
import icherry.central_meteorologica as central_meteorologica
import icherry.tipos_para_la_demo as demo
import icherry.proveedor_texto as proveedor_texto
import icherry.estado_salud as estado_salud
import icherry.temporizador as temporizador
import icherry.tiempo as tiempo
import icherry.logging as logging

import npyscreen

# bootstrap

# construcción de sensores
sensorDeTemperatura = sensores.Sensor(
    dispositivos.DispositivoDeLecturaArchivo(
        'devices/sensor_temperatura'),
    parsers.CadenaANumero(),
    magnitudes.TemperaturaEnCelsius
)

sensorDeHumedad = sensores.Sensor(
    dispositivos.DispositivoDeLecturaArchivo(
        'devices/sensor_humedad'),
    parsers.CadenaAPorcentaje(),
    magnitudes.HumedadRelativa
)

sensorDeAcidez = sensores.Sensor(
    dispositivos.DispositivoDeLecturaArchivo(
        'devices/sensor_acidez'),
    parsers.CadenaANumero(),
    magnitudes.AcidezEnPH
)

sensorDeAcidez.sensar()

# construcción de actuadores
constructorDeActuador = actuadores.ConstructorDeActuadorEnArchivo()

actuadorDeAgua = constructorDeActuador.crear(
    'devices/actuador_agua')
actuadorDeLuz = constructorDeActuador.crear(
    'devices/actuador_lampara')
actuadorDeFertilizante = constructorDeActuador.crear(
    'devices/actuador_fertilizante')
actuadorDeAntibiotico = constructorDeActuador.crear(
    'devices/actuador_antibiotico')

# construcción de la central meteorologica que lee los datos de los archivos.
predictor = demo.PredictorMeteorologicoPorArchivo(
    dispositivos.DispositivoDeLecturaArchivo("devices/pronostico"))
reloj = demo.ProveedorDeTiempoPorArchivo(
    dispositivos.DispositivoDeLecturaArchivo("devices/tiempo"))
central = central_meteorologica.CentralMeteorologica(predictor, reloj)


# Estado de salud dummy, se usa para la demo:
estadoFenologicoDummy = estado_salud.EstadoFenologico()
estadoFenologicoDummy.cantidadBrotes(2)
estadoFenologicoDummy.cantidadFlores(10)
estadoFenologicoDummy.altura(15)

estado = estado_salud.EstadoDeSalud(estadoFenologicoDummy)
estado.temperatura(sensorDeTemperatura.sensar())
estado.humedad(sensorDeHumedad.sensar())
estado.acidez(sensorDeAcidez.sensar())

# proveedor de texto
proveedorDeTexto = proveedor_texto.ProveedorDeTexto('resources/textos.es')

# construcción de pantallas
# seguramente hay que generar un objeto que construya todo esto

temporizadorDatos = temporizador.Temporizador()
temporizadorDatos.ejecutarCada(tiempo.DuracionEnSegundos(5),
       lambda: actualizarLosDatos(central, sensorDeAcidez, sensorDeHumedad, sensorDeTemperatura))


logCentral = logging.LogCentralMeteorologica(
    dispositivos.DispositivoDeEscrituraArchivo('logs/log_central'))
central.registrarObserver(logCentral)

logSensorTemperatura = logging.LogSensor('Sensor de Temperatura',
            dispositivos.DispositivoDeEscrituraArchivo('logs/log_sensor_temperatura'))
sensorDeTemperatura.registrarObserver(logSensorTemperatura)

logSensorHumedad = logging.LogSensor('Sensor de Humedad',
            dispositivos.DispositivoDeEscrituraArchivo('logs/log_sensor_humedad'))
sensorDeHumedad.registrarObserver(logSensorHumedad)

logSensorAcidez = logging.LogSensor('Sensor de Acidez',
            dispositivos.DispositivoDeEscrituraArchivo('logs/log_sensor_acidez'))
sensorDeAcidez.registrarObserver(logSensorAcidez)




def actualizarLosDatos(central, sensorDeAcidez, sensorDeHumedad, sensorDeTemperatura):
    central.obtenerPronostico(central.obtenerFechaYHora(), 24)
    sensorDeAcidez.sensar()
    sensorDeHumedad.sensar()
    sensorDeTemperatura.sensar()


def main(*args):
    app = ui_ncurses.ICherryCurses()

    app.addFormClass('MAIN', ui_ncurses.PantallaDeInicio, proveedorDeTexto,
                     archivoFondoAscii='resources/main_background_pic.txt')

    app.addFormClass('SENSORES', ui_ncurses.PantallaDeSensores,
                     proveedorDeTexto, sensorDeTemperatura,
                     sensorDeHumedad, sensorDeAcidez)

    app.addFormClass(
        'CENTRAL', ui_ncurses.PantallaDeCentral, proveedorDeTexto, central)
    app.addFormClass(
        'SALUD', ui_ncurses.PantallaDeEstadoDeSalud, proveedorDeTexto, estado)

    app.addFormClass('EN_CONSTRUCCION', ui_ncurses.PantallaEnConstruccion, proveedorDeTexto)

    temporizadorDatos.iniciarEjecucion()

    app.run()

    # Detener los temporizadores
    temporizadorDatos.detener()

npyscreen.wrapper_basic(main)
