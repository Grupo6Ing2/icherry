# coding=utf-8
import npyscreen
import icherry.builders as builders
import icherry.tiempo as tiempo

builder = builders.ContructorDemo()
segundosDeActualizacionSensores = 1
segundosDeActualizacionDeCentral = 1
segundosDeActualizacionDePlanta = 1
segundosDeActualizacionGenerador = 10
segundosDeActualizacionEjecucion = 5
duracionDePlanificacion = tiempo.DuracionEnHoras(1)

actualizadores = []

# Construccion de sensores
(sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez) = builder.construirSensores()
actualizadorDeSensores = builder.construirActualizadorDeSensores(
    segundosDeActualizacionSensores, sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez)
actualizadores.append(actualizadorDeSensores)

# Construccion de central meteorológica
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

# Programa de Suministro (PS). Notar que estará vacío.
programaDeSuministro = builder.construirProgramaDeSuministro(centralMeteorologica)

# Generador de Programa de Suministro
generadorDePrograma = builder.construirGeneradorDeProgramaDeSuministro(
    planMaestro, estadoDePlanta, centralMeteorologica, programaDeSuministro)

# NOTICE: Poblamos el Programa de Suministro (si no, hay que esperar
# hasta el primer heartbeat del APS para que haya algo en el PS)
generadorDePrograma.generar()  # anda esto?

# Actualizador de Programa de Suministro (APS)
actualizadorDeProgramaDeSuministro = \
builder.construirActualizadorDeProgramaDeSuministro(
    segundosDeActualizacionGenerador, generadorDePrograma)
actualizadores.append(actualizadorDeProgramaDeSuministro)

# Construcción de actuadores (R,A,L,F)
(actuadorRegado, actuadorAntibiotico,
 actuadorLuz, actuadorFertilizante ) = builder.construirActuadores()

# Actualizador de Ejecución
actualizadorDeEjecucion = builder.construirActualizadorDeEjecucion(
    segundosDeActualizacionEjecucion,
    duracionDePlanificacion, centralMeteorologica, programaDeSuministro,
    actuadorRegado, actuadorAntibiotico, actuadorLuz, actuadorFertilizante)
actualizadores.append(actualizadorDeEjecucion)


# Activo todos los timers
for actualizador in actualizadores:
    actualizador.iniciarActualizacion()

# Función principal que va a correr en el entorno ncurses
def main(*args):
    # Las pantallas tengo que construirlas con el enterno ncurses activo

    # Aplicación principal
    aplicacion = builder.construirAplicacion()

    # Pantalla sensores
    pantallaSensor = builder.construirPantallaSensores(
        proveedorDeTexto,
        sensorDeTemperatura,
        sensorDeHumedad,
        sensorDeAcidez
    )
    aplicacion.registerForm('SENSORES', pantallaSensor)

    # Pantalla de la central meteorológica
    pantallaCentralMeteorologica = builder.construirPantallaCentralMeteorologica(
        proveedorDeTexto,
        centralMeteorologica
    )
    aplicacion.registerForm('CENTRAL', pantallaCentralMeteorologica)

    # Pantalla del programa de suministro
    pantallaProgramaSuministro = builder.construirPantallaProgramaDeSuministro(
        proveedorDeTexto,
        programaDeSuministro
    )
    aplicacion.registerForm('PROGRAMA', pantallaProgramaSuministro)

    # Pantalla inicio
    pantallaInicio = builder.contruirPantallaInicio(proveedorDeTexto)
    aplicacion.registerForm('MAIN', pantallaInicio)

    # Pantalla en construcción
    pantallaEnConstruccion = builder.construirPantallaEnConstruccion(proveedorDeTexto)
    aplicacion.registerForm('EN_CONSTRUCCION', pantallaEnConstruccion)

    # Pantalla de estado de planta
    pantallaEstadoDePlanta = builder.construirPantallaEstadoDePlanta(proveedorDeTexto, estadoDePlanta)
    aplicacion.registerForm('ESTADO', pantallaEstadoDePlanta)

    # Pantalla de edicion de estado fenológico
    pantallaDeEdicionDeEstadoFenologico = builder.construirPantallaDeEdicionDeEstadoFenologico(
        proveedorDeTexto, estadoDePlanta)
    aplicacion.registerForm('EDICION_ESTADO_FENOLOGICO', pantallaDeEdicionDeEstadoFenologico)

    # Pantalla de visualizacion de plan maestro
    pantallaDeVisualizacionDePlanMaestro = builder.construirPantallaDeVisualizacionDePlanMaestro(
        proveedorDeTexto, planMaestro)
    aplicacion.registerForm('VER_PLAN_MAESTRO', pantallaDeVisualizacionDePlanMaestro)
    planMaestro.notificarObservers()

    # Pantalla de edicion de plan maestro
    pantallaDeEdicionDePlanMaestro = builder.construirPantallaDeEdicionDePlanMaestro(
        proveedorDeTexto, planMaestro)
    aplicacion.registerForm('EDITAR_PLAN_MAESTRO', pantallaDeEdicionDePlanMaestro)

    # Inicio la aplicación ncurses
    aplicacion.run()

# Inicio el entorno ncurses
npyscreen.wrapper_basic(main)

# Detengo todos los temporizadores
for actualizador in actualizadores:
    actualizador.detenerActualizacion()
