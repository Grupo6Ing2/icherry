# coding=utf-8
import npyscreen
import icherry.builders as builders

builder = builders.ContructorDemo()
segundosDeActualizacionSensores = 1
segundosDeActualizacionDeCentral = 1

actualizadores = []

# Construccion de sensores
(sensorTemperatura, sensorHumedad, sensorAcidez) = builder.construirSensores()
actualizadorDeSensores = builder.construirActualizadorDeSensores(
    segundosDeActualizacionSensores, sensorTemperatura, sensorHumedad, sensorAcidez)
actualizadores.append(actualizadorDeSensores)

# Construccion de central
centralMeteorologica = builder.construirCentralMeterologica()
actualizadorDeCentral = builder.construirActualizadorDeCentral(
    segundosDeActualizacionDeCentral, centralMeteorologica)
actualizadores.append(actualizadorDeCentral)

# Proveedor de Texto
proveedorDeTexto = builder.construirProveedorDeTexto()

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
        sensorTemperatura,
        sensorHumedad,
        sensorAcidez
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

    # Inicio la aplicacion ncurses
    aplicacion.run()

# Inicio el entorno ncurses
npyscreen.wrapper_basic(main)

# Detengo todos los temporizadores
for actualizador in actualizadores:
    actualizador.detenerActualizacion()
