# coding=utf-8
import npyscreen
import icherry.builders as builders
import icherry.tiempo as tiempo

builder = builders.ContructorDemo()
duracionDeActualizacionSensores = tiempo.DuracionEnSegundos(1)
duracionDeActualizacionDeCentral = tiempo.DuracionEnSegundos(1)
duracionDeActualizacionDePlanta = tiempo.DuracionEnSegundos(1)
duracionDeActualizacionGenerador = tiempo.DuracionEnSegundos(10)
duracionDeActualizacionEjecucion = tiempo.DuracionEnSegundos(5)
duracionDePlanificacion = tiempo.DuracionEnHoras(1)

actualizadores = []

# Construcción de sensores
(sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez) = builder.construirSensores()
actualizadorDeSensores = builder.construirActualizadorDeSensores(
    duracionDeActualizacionSensores, sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez)
actualizadores.append(actualizadorDeSensores)

# Construcción de central meteorológica
centralMeteorologica = builder.construirCentralMeterologica()
actualizadorDeCentral = builder.construirActualizadorDeCentral(
    duracionDeActualizacionDeCentral, centralMeteorologica)
actualizadores.append(actualizadorDeCentral)

# Proveedor de Texto
proveedorDeTexto = builder.construirProveedorDeTexto()

# Plan Maestro
planMaestro = builder.construirPlanMaestro()

# Estado de Planta
estadoDePlanta = builder.construirEstadoDePlanta()
actualizadorDeEstadoPlanta = builder.construirActualizadorDeEstadoDePlanta(
    duracionDeActualizacionDePlanta, estadoDePlanta,
    sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez, planMaestro)
actualizadores.append(actualizadorDeEstadoPlanta)

# Programa de Suministro (PS). Notar que estará vacío.
programaDeSuministro = builder.construirProgramaDeSuministro(centralMeteorologica)

# Generador de Programa de Suministro
generadorDePrograma = builder.construirGeneradorDeProgramaDeSuministro(
    planMaestro, estadoDePlanta, centralMeteorologica, programaDeSuministro)

# Actualizador de Programa de Suministro (APS)
actualizadorDeProgramaDeSuministro \
    = builder.construirActualizadorDeProgramaDeSuministro(
        duracionDeActualizacionGenerador, generadorDePrograma)
actualizadores.append(actualizadorDeProgramaDeSuministro)

# Construcción de actuadores (R,A,L,F)
(actuadorRegado, actuadorAntibiotico,
 actuadorLuz, actuadorFertilizante) = builder.construirActuadores()

# Actualizador de Ejecución
actualizadorDeEjecucion = builder.construirActualizadorDeEjecucion(
    duracionDeActualizacionEjecucion,
    duracionDePlanificacion, centralMeteorologica, programaDeSuministro,
    actuadorRegado, actuadorAntibiotico, actuadorLuz, actuadorFertilizante)
actualizadores.append(actualizadorDeEjecucion)


# Función principal que va a correr en el entorno npyscreen
def npyscreen_main(*args):
    # Las pantallas tengo que construirlas con el entorno npyscreen activo

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
    pantallaEstadoDePlanta = builder.construirPantallaEstadoDePlanta(
        proveedorDeTexto, estadoDePlanta)
    aplicacion.registerForm('ESTADO', pantallaEstadoDePlanta)

    # Pantalla de edición de estado fenológico
    pantallaDeEdicionDeEstadoFenologico = builder.construirPantallaDeEdicionDeEstadoFenologico(
        proveedorDeTexto, estadoDePlanta)
    aplicacion.registerForm('EDICION_ESTADO_FENOLOGICO', pantallaDeEdicionDeEstadoFenologico)

    # Pantalla de visualizacion de plan maestro
    pantallaDeVisualizacionDePlanMaestro = builder.construirPantallaDeVisualizacionDePlanMaestro(
        proveedorDeTexto, planMaestro)
    aplicacion.registerForm('VER_PLAN_MAESTRO', pantallaDeVisualizacionDePlanMaestro)
    planMaestro.notificarObservers()

    # Pantalla de edición de plan maestro
    pantallaDeEdicionDePlanMaestro = builder.construirPantallaDeEdicionDePlanMaestro(
        proveedorDeTexto, planMaestro)
    aplicacion.registerForm('EDITAR_PLAN_MAESTRO', pantallaDeEdicionDePlanMaestro)

    # Inicio la aplicación npyscreen
    aplicacion.run()


# ====================================================================
# Función principal de la demo. Ejecuta todos los actualizadores y la
# interfaz gráfica.

def demo():

    # Poblamos el Programa de Suministro
    generadorDePrograma.generar()

    # Activamos todos los actualizadores
    for actualizador in actualizadores:
        actualizador.iniciarActualizacion()

    # Iniciamos el entorno npyscreen
    npyscreen.wrapper_basic(npyscreen_main)

    # Detenemos todos los actualizadores
    for actualizador in actualizadores:
        actualizador.detenerActualizacion()

if __name__ == "__main__":
    demo()
