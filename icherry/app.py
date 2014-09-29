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

# construccion de la central meteorologica que lee los datos de los archivos.
predictor = demo.PredictorMeteorologicoPorArchivo(
    dispositivos.DispositivoDeLecturaArchivo("devices/pronostico"))
reloj = demo.ProveedorDeTiempoPorArchivo(
    dispositivos.DispositivoDeLecturaArchivo("devices/tiempo"))
central = central_meteorologica.CentralMeteorologica(predictor, reloj)

# proveedor de texto
proveedorDeTexto = proveedor_texto.ProveedorDeTexto('resources/textos.es')

# construcción de pantallas
# seguramente hay que generar un objeto que construya todo esto


def main(*args):
    app = ui_ncurses.ICherryCurses()

    pantallaDeInicio = ui_ncurses.PantallaDeInicio(
        proveedorDeTexto,
        archivoFondoAscii='resources/main_background_pic.txt',
    )

    pantallaDeSensores = ui_ncurses.PantallaDeSensores(
        proveedorDeTexto,
        sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez)

    pantallaDeCentral = ui_ncurses.PantallaDeCentral(proveedorDeTexto, central)

    pantallaEnConstruccion = \
        ui_ncurses.PantallaEnConstruccion(proveedorDeTexto)

    app.registerForm('MAIN', pantallaDeInicio)
    app.registerForm('SENSORES', pantallaDeSensores)
    app.registerForm('CENTRAL', pantallaDeCentral)
    app.registerForm('EN_CONSTRUCCION', pantallaEnConstruccion)

    app.run()

npyscreen.wrapper_basic(main)
