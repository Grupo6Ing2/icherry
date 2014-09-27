import magnitudes


class Parser():

    def __init__(self):
        raise NotImplementedError

    def parse(unObjeto):
        raise NotImplementedError


class CadenaANumero(Parser):

    def __init__(self):
        pass

    def parse(self, unaCadena):
        return float(unaCadena)


class CadenaAPorcentaje(Parser):

    def __init__(self):
        pass

    def parse(self, unaCadena):
        return magnitudes.Porcentaje(int(unaCadena))


class MagnitudACadena(Parser):

    def __init__(self):
        pass

    def parse(self, unaMagnitud):
        return str(unaMagnitud.valor())
