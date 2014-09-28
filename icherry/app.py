# coding=utf-8
import icherry.sensores as sensores
import icherry.magnitudes as magnitudes
import icherry.dispositivos as dispositivos
import icherry.parsers as parsers
import icherry.actuadores as actuadores
import icherry.ui_ncurses as ui_ncurses

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

# construcción de pantallas
# seguramente hay que generar un objeto que construya todo esto


def main(*args):
    app = ui_ncurses.ICherryCurses()

    pantallaDeInicio = ui_ncurses.PantallaDeInicio()

    pantallaDeSensores = ui_ncurses.PantallaDeSensores(
        sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez)

    pantallaEnConstruccion = ui_ncurses.PantallaEnConstruccion()

    app.registerForm('MAIN', pantallaDeInicio)
    app.registerForm('SENSORES', pantallaDeSensores)
    app.registerForm('EN_CONSTRUCCION', pantallaEnConstruccion)
    app.run()

npyscreen.wrapper_basic(main)
