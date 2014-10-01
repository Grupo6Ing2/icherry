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
import icherry.plan_maestro as plan_maestro
import icherry.programa_suministro as programa_suministro
import icherry.constructor_programa as constructor_programa
import icherry.recomendaciones as recomendaciones


import npyscreen
# bootstrap

def actualizarLosDatos(central, sensorDeAcidez, sensorDeHumedad, sensorDeTemperatura):
    central.obtenerPronostico(central.obtenerFechaYHora(), 24)
    sensorDeAcidez.sensar()
    sensorDeHumedad.sensar()
    sensorDeTemperatura.sensar()

def armarPlanMaestro():
    e0 = plan_maestro.EstadioGerminacion
    e1 = plan_maestro.EstadioDesarrollo

    temperatura = magnitudes.Rango(magnitudes.TemperaturaEnCelsius(10),
                                   magnitudes.TemperaturaEnCelsius(30))
    humedad = magnitudes.Rango(magnitudes.HumedadRelativa(magnitudes.Porcentaje(40)),
                               magnitudes.HumedadRelativa(magnitudes.Porcentaje(50)))
    acidez = magnitudes.Rango(magnitudes.AcidezEnPH(6.5), magnitudes.AcidezEnPH(7.5))
    umbral0 = plan_maestro.UmbralOptimoDeCultivo(e0, temperatura, humedad, acidez)

    temperatura = magnitudes.Rango(magnitudes.TemperaturaEnCelsius(12),
                                   magnitudes.TemperaturaEnCelsius(20))
    humedad = magnitudes.Rango(magnitudes.HumedadRelativa(magnitudes.Porcentaje(40)),
                               magnitudes.HumedadRelativa(magnitudes.Porcentaje(70)))
    acidez = magnitudes.Rango(magnitudes.AcidezEnPH(6.0), magnitudes.AcidezEnPH(7.5))

    umbral1 = plan_maestro.UmbralOptimoDeCultivo(e1, temperatura, humedad, acidez)

    plan = plan_maestro.PlanMaestro([umbral0, umbral1])
    return plan

def armarProgramaDeSuministro(central):
    ahora = central.obtenerFechaYHora()
    programaDeSuministro = programa_suministro.ProgramaDeSuministro(
        magnitudes.Rango(ahora, ahora.agregarHoras(24)))
    return programaDeSuministro

def armarActualizadorDePrograma(planMaestro, planta, central, programa):
    constructorDePrograma = constructor_programa.ConstructorDeProgramaDeSuministro(planMaestro)

    actualizador = constructor_programa.ActualizadorDeProgramaDeSuministro(
        programa, constructorDePrograma, planta, central,
        [recomendaciones.RecomendacionNoDebeHaberAltaAmplitudTermica(),
         recomendaciones.RecomendacionDeCultivoRiegosConstantes(),
         recomendaciones.RecomendacionDeCultivoSePrefierenTemperaturasModeradas()])
    return actualizador



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


estado = estado_salud.EstadoDePlanta()
estadoFenologico = estado.estadoFenologico()
estadoFenologico.cantidadBrotes(2)
estadoFenologico.cantidadFlores(10)
estadoFenologico.altura(magnitudes.LongitudEnCentimetros(15))

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

planta = None
planMaestro = armarPlanMaestro()
programaDeSuministro = armarProgramaDeSuministro(central)
actualizador = armarActualizadorDePrograma(planMaestro, planta, central, programaDeSuministro)

temporizadorDeActualizacionDePrograma = temporizador.Temporizador()
temporizadorDeActualizacionDePrograma.ejecutarCada(tiempo.DuracionEnSegundos(5),
          lambda: actualizador.actualizarProgramaDeSuministro())



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
#TODO: habilitar cuando este definida la clase Planta.
#    temporizadorDeActualizacionDePrograma.iniciarEjecucion()

    app.run()

    # Detener los temporizadores
    temporizadorDatos.detener()
    temporizadorDeActualizacionDePrograma.detener()

npyscreen.wrapper_basic(main)
