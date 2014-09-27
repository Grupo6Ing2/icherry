class DispositivoDeLectura():

    def __init__(self):
        raise NotImplementedError

    def leer(self):
        raise NotImplementedError


class DispositivosDeLecturaArchivo(DispositivoDeLectura):

    def __init__(self, unNombreArchivo):
        self.archivo = open(unNombreArchivo, 'r')

    def leer(self):
        self.archivo.seek(0)
        return self.archivo.read()


class DispositivoDeEscritura():

    def __init__(self):
        raise NotImplementedError

    def leer(self):
        raise NotImplementedError


class DispositivoDeEscrituraArchivo(DispositivoDeEscritura):

    def __init__(self, unNombreArchivo):
        self.archivo = open(unNombreArchivo, 'w')

    def escribir(self, unaCadena):
        return self.archivo.write(unaCadena)
