# coding=utf-8
import sensores
import magnitudes
import dispositivos
import parsers
import actuadores

# bootstrap

# construccion de sensores
sensor_de_temperatura = sensores.Sensor(
    dispositivos.DispositivosDeLecturaArchivo(
        '../devices/sensor_temperatura'),
    parsers.CadenaANumero(),
    magnitudes.TemperaturaEnCelsius
)

sensor_de_humedad = sensores.Sensor(
    dispositivos.DispositivosDeLecturaArchivo(
        '../devices/sensor_humedad'),
    parsers.CadenaAPorcentaje(),
    magnitudes.HumedadRelativa
)

sensor_de_acidez = sensores.Sensor(
    dispositivos.DispositivosDeLecturaArchivo(
        '../devices/sensor_acidez'),
    parsers.CadenaANumero(),
    magnitudes.AcidezEnPH
)

# construccion de actuadores
constructor_de_actuador = actuadores.ConstructorDeActuadorEnArchivo()

actuador_de_agua = constructor_de_actuador.crear(
    '../devices/actuador_agua')
actuador_de_luz = constructor_de_actuador.crear(
    '../devices/actuador_lampara')
actuador_de_fertilizante = constructor_de_actuador.crear(
    '../devices/actuador_fertilizante')
actuador_de_antibiotico = constructor_de_actuador.crear(
    '../devices/actuador_antibiotico')

# construccion de pantallas
# TODO