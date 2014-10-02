# coding=utf-8
import npyscreen
import icherry.builders as builders

builder = builders.ContructorDemo()
segundosDeActualizacionSensores = 1
segundosDeActualizacionDeCentral = 1
segundosDeActualizacionDePlanta = 1

actualizadores = []

# Construccion de sensores
(sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez) = builder.construirSensores()
actualizadorDeSensores = builder.construirActualizadorDeSensores(
    segundosDeActualizacionSensores, sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez)
actualizadores.append(actualizadorDeSensores)

# Construccion de central
centralMeteorologica = builder.construirCentralMeterologica()
actualizadorDeCentral = builder.construirActualizadorDeCentral(
    segundosDeActualizacionDeCentral, centralMeteorologica)
actualizadores.append(actualizadorDeCentral)

# Proveedor de Texto
proveedorDeTexto = builder.construirProveedorDeTexto()

# Plan Maestro
planMaestro = builder.construirPlanMaestro()

# Estado de Planta
estadoDePlanta = builder.construirEstadoDePlanta()
actualizadorDeEstadoPlanta = builder.construirActualizadorDeEstadoDePlanta(
    segundosDeActualizacionDePlanta, estadoDePlanta, sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez, planMaestro)
actualizadores.append(actualizadorDeEstadoPlanta)

# Activo todos los timers
for actualizador in actualizadores:
    actualizador.iniciarActualizacion()


# Funcion principal que va a correr en el entorno ncurses
def main(*args):
    # Las pantallas tengo que construirlas con el enterno ncurses activo

    # Aplicacion principal
    aplicacion = builder.construirAplicacion()

    # Pantalla sensores
    pantallaSensor = builder.construirPantallaSensores(
        proveedorDeTexto,
        sensorDeTemperatura,
        sensorDeHumedad,
        sensorDeAcidez
    )
    aplicacion.registerForm('SENSORES', pantallaSensor)

    # Pantalla de la central meteorologica
    pantallaCentralMeteorologica = builder.construirPantallaCentralMeteorologica(
        proveedorDeTexto,
        centralMeteorologica
    )
    aplicacion.registerForm('CENTRAL', pantallaCentralMeteorologica)

    # Pantalla inicio
    pantallaInicio = builder.contruirPantallaInicio(proveedorDeTexto)
    aplicacion.registerForm('MAIN', pantallaInicio)

    # Pantalla en construccion
    pantallaEnConstruccion = builder.construirPantallaEnConstruccion(proveedorDeTexto)
    aplicacion.registerForm('EN_CONSTRUCCION', pantallaEnConstruccion)

    # Pantalla de estado de planta
    pantallaEstadoDePlanta = builder.construirPantallaEstadoDePlanta(proveedorDeTexto, estadoDePlanta)
    aplicacion.registerForm('ESTADO', pantallaEstadoDePlanta)

    # Pantalla de edicion de estado fenologico
    pantallaDeEdicionDeEstadoFenologico = builder.construirPantallaDeEdicionDeEstadoFenologico(
        proveedorDeTexto, estadoDePlanta)
    aplicacion.registerForm('EDICION_ESTADO_FENOLOGICO', pantallaDeEdicionDeEstadoFenologico)

    # Pantalla de visualizacion plan maestro
    pantallaDeVisualizacionDePlanMaestro = builder.construirPantallaDeVisualizacionDePlanMaestro(
        proveedorDeTexto, planMaestro)
    aplicacion.registerForm('VER_PLAN_MAESTRO', pantallaDeVisualizacionDePlanMaestro)
    planMaestro.notificarObservers()

    # Inicio la aplicacion ncurses
    aplicacion.run()

# Inicio el entorno ncurses
npyscreen.wrapper_basic(main)

# Detengo todos los temporizadores
for actualizador in actualizadores:
    actualizador.detenerActualizacion()
