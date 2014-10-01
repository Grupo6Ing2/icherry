# coding=utf-8
import icherry.sensores as sensores
import icherry.magnitudes as magnitudes
import icherry.dispositivos as dispositivos
import icherry.parsers as parsers
import icherry.ui_ncurses as ui_ncurses
import icherry.proveedor_texto as proveedor_texto
import icherry.temporizador as temporizador
import icherry.tiempo as tiempo
import npyscreen


# construcción de sensores
def crearSensor(archivo, parser, magnitud):
    sensor = sensores.Sensor(
        dispositivos.DispositivoDeLecturaArchivo(archivo), parser, magnitud
    )
    sensor.sensar()

    timer = temporizador.Temporizador()
    timer.ejecutarCada(tiempo.DuracionEnSegundos(1), lambda: sensor.sensar())
    timer.iniciarEjecucion()

    return (sensor, timer)


(sTemperatura, tTemperatura) = crearSensor('devices/sensor_temperatura', parsers.CadenaANumero(), magnitudes.TemperaturaEnCelsius)
(sHumedad, tHumedad) = crearSensor('devices/sensor_humedad', parsers.CadenaAPorcentaje(), magnitudes.HumedadRelativa)
(sAcidez, tAcidez) = crearSensor('devices/sensor_acidez', parsers.CadenaANumero(), magnitudes.AcidezEnPH)

proveedorDeTexto = proveedor_texto.ProveedorDeTexto('resources/textos.es')


def main(*args):
    app = ui_ncurses.ICherryCurses()

    pSensores = ui_ncurses.PantallaDeSensoresMVC(proveedorDeTexto, sTemperatura, sHumedad, sAcidez)
    app.registerForm('SENSORES', pSensores)

    app.addFormClass('MAIN', ui_ncurses.PantallaDeInicio, proveedorDeTexto,
                    archivoFondoAscii='resources/main_background_pic.txt')

    app.addFormClass('EN_CONSTRUCCION', ui_ncurses.PantallaEnConstruccion, proveedorDeTexto)

    app.run()

npyscreen.wrapper_basic(main)

tTemperatura.detener()
tHumedad.detener()
tAcidez.detener()
