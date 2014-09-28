import icherry.parsers as parsers
import icherry.central_meteorologica as central_meteorologica


# Clases usadas para la demo. Leen los datos de los archivos.
class PredictorMeteorologicoPorArchivo(central_meteorologica.PredictorMeteorologico):
    def __init__(self, dispositivoDeLectura):
        parser = parsers.ParserPronosticoMeteorologico()
        pronostico = parser.parse(dispositivoDeLectura.leer())
        self.__pronostico = pronostico

    def prediccionPara(self, unLapso):
        return self.__pronostico.prediccionPara(unLapso.desde())


class ProveedorDeTiempoPorArchivo(central_meteorologica.ProveedorDeTiempo):
    def __init__(self, dispositivoDeLectura):
        self.__dispositivoDeLectura = dispositivoDeLectura

    def fechaYHoraActual(self):
        return parsers.CadenaAFechaYHora().parse(self.__dispositivoDeLectura.leer())
