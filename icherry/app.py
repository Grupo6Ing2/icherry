# coding=utf-8
import sensores
import magnitudes
import dispositivos
import parsers
import actuadores
import ui_ncurses
import npyscreen

# bootstrap

# construccion de sensores
sensorDeTemperatura = sensores.Sensor(
    dispositivos.DispositivosDeLecturaArchivo(
        'devices/sensor_temperatura'),
    parsers.CadenaANumero(),
    magnitudes.TemperaturaEnCelsius
)

sensorDeHumedad = sensores.Sensor(
    dispositivos.DispositivosDeLecturaArchivo(
        'devices/sensor_humedad'),
    parsers.CadenaAPorcentaje(),
    magnitudes.HumedadRelativa
)

sensorDeAcidez = sensores.Sensor(
    dispositivos.DispositivosDeLecturaArchivo(
        'devices/sensor_acidez'),
    parsers.CadenaANumero(),
    magnitudes.AcidezEnPH
)

sensorDeAcidez.sensar()

# construccion de actuadores
constructorDeActuador = actuadores.ConstructorDeActuadorEnArchivo()

actuadorDeAgua = constructorDeActuador.crear(
    'devices/actuador_agua')
actuadorDeLuz = constructorDeActuador.crear(
    'devices/actuador_lampara')
actuadorDeFertilizante = constructorDeActuador.crear(
    'devices/actuador_fertilizante')
actuadorDeAntibiotico = constructorDeActuador.crear(
    'devices/actuador_antibiotico')

# construccion de pantallas
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
